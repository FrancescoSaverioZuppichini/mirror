import json
import io
import torch
import time

from flask import Flask, request, Response, send_file, jsonify
from torchvision.transforms import ToPILImage
from .visualisations.web import Weights
from .ModuleTracer import ModuleTracer


class App(Flask):
    default_visualisations = [Weights]
    MAX_LINKS_EVERY_REQUEST = 64

    def __init__(self, inputs, model, visualisations=[]):
        super().__init__(__name__)
        self.cache = {}  # internal cache used to store the results
        self.outputs = None  # holds the current output from a visualisation
        if len(inputs) <= 0: raise ValueError('At least one input is required.')

        self.inputs, self.model = inputs, model
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.current_input = self.inputs[0].unsqueeze(0).to(self.device)  # add 1 dim for batch
        self.module = model.to(self.device).eval()
        self.setup_tracer()
        self.setup_visualisations(visualisations)

        @self.route('/')
        def root():
            return self.send_static_file('index.html')

        @self.route('/api/model', methods=['GET'])
        def api_model():
            model = self.tracer.to_JSON()

            response = jsonify(model)

            return response

        @self.route('/api/inputs', methods=['GET', 'PUT'])
        def api_inputs():
            if request.method == 'GET':
                self.outputs = self.inputs

                response = ['/api/model/image/{}/{}/{}/{}/{}'.format(hash(None),
                                                                     hash(None),
                                                                     hash(time.time()),
                                                                     id,
                                                                     i) for i in range(len(self.inputs))]

                response = jsonify({'links': response, 'next': False})

            elif request.method == 'PUT':
                data = json.loads(request.data.decode())

                input_index = data['id']

                self.current_input = self.inputs[input_index].unsqueeze(0).to(self.device)

                response = jsonify(data)

            return response

        @self.route('/api/model/layer/<id>')
        def api_model_layer(id):
            id = int(id)
            name = self.traced[id].name

            return Response(response=name)

        @self.route('/api/visualisation', methods=['GET'])
        def api_visualisations():
            serialised = [v.to_JSON() for v in self.visualisations]

            response = jsonify({'visualisations': serialised,
                                'current': self.current_vis.to_JSON()})

            return response

        @self.route('/api/visualisation', methods=['PUT'])
        def api_visualisation():
            data = json.loads(request.data.decode())

            vis_key = data['name']
            visualisations_not_exist = vis_key not in self.name2visualisations

            if visualisations_not_exist:
                response = Response(status=500,
                                    response='Visualisation {} not supported or does not exist'.format(vis_key))
            else:
                self.current_vis = self.name2visualisations[vis_key]
                self.current_vis.from_JSON(data['params'])
                self.current_vis.clean_cache()
                response = jsonify(self.current_vis.to_JSON())

            return response

        @self.route('/api/model/layer/output/<id>')
        def api_model_layer_output(id):
            try:

                layer = self.traced[id].module

                if self.current_input not in self.current_vis.cache: self.current_vis.cache[self.current_input] = {}

                layer_cache = self.current_vis.cache[self.current_input]
                # always clone the input to avoid being modified
                input_clone = self.current_input.clone()

                if layer not in layer_cache:
                    layer_cache[layer] = self.current_vis(input_clone, layer)
                    del input_clone
                else:
                    print('[INFO] cached')

                self.outputs, _ = layer_cache[layer]

                if len(self.outputs.shape) < 3:  raise ValueError

                last = int(request.args['last'])
                max = min((last + self.MAX_LINKS_EVERY_REQUEST), self.outputs.shape[0])

                response = ['/api/model/image/{}/{}/{}/{}/{}'.format(hash(self.current_input),
                                                                     hash(self.current_vis),
                                                                     hash(time.time()),
                                                                     id,
                                                                     i) for i in range(last, max)]

                response = jsonify({'links': response, 'next': last + 1 < max})


            except KeyError:
                response = Response(status=500, response='Index not found.')
            except ValueError:
                response = Response(status=404, response='Outputs must be an array of images')
            except StopIteration:
                response = jsonify({'links': [], 'next': False})

            return response

        @self.route('/api/model/image/<input_id>/<vis_id>/<layer_id>/<time>/<output_id>')
        def api_model_layer_output_image(input_id, vis_id, layer_id, time, output_id):
            output_id = int(output_id)
            try:
                output = self.outputs[output_id]
                output = output.detach().cpu()
                pil_img = ToPILImage()(output)
                img_io = io.BytesIO()
                pil_img.save(img_io, 'JPEG', quality=70)
                img_io.seek(0)
                return send_file(img_io, mimetype='image/jpeg')
            except KeyError:
                return Response(status=500, response='Index not found.')

    def setup_tracer(self):
        # instantiate a Tracer object and trace one input
        self.tracer = ModuleTracer(module=self.module)
        self.tracer(self.current_input)
        # store the traced graph as a dictionary
        self.traced = self.tracer.__dict__()

    def setup_visualisations(self, visualisations):
        visualisations = [*self.default_visualisations, *visualisations]
        self.visualisations = [v(self.module, self.device) for v in visualisations]
        self.name2visualisations = {v.name: v for v in self.visualisations}
        self.current_vis = self.visualisations[0]
