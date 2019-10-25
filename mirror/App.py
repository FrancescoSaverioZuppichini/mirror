import json
import io
import torch
import time
import logging
from flask import Flask, request, Response, send_file, jsonify
from torchvision.transforms import ToPILImage
from .visualisations.web import Weights
from .ModuleTracer import ModuleTracer
from .utils import device, add_batch


class App(Flask):
    default_visualisations = [Weights]
    MAX_LINKS_EVERY_REQUEST = 64

    def __init__(self, inputs, model, visualisations=[], device=device):
        super().__init__(__name__)
        if len(inputs) <= 0: raise ValueError('At least one input is required.')
        self.inputs, self.model = inputs, model
        self.device = device
        self.module = model.to(self.device).eval()
        self.logger.setLevel(logging.INFO)
        self.outputs: torch.Tensor = torch.empty(0)
        self.input = add_batch(self.inputs[0]).to(self.device)  # add 1 dim for batch
        self.layer = self.module
        self.setup_tracer()
        self.setup_visualisations(visualisations)
        self.cache = {vis.name: {} for vis in
                      self.visualisations}  # internal cache used to store the results of each visualization

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
            response = Response('404', 'Invalid Method.')

            if request.method == 'GET':
                self.outputs = self.inputs
                response = [f'/api/model/image/{time.time()}/{i}' for i in range(len(self.outputs))]
                response = jsonify({'links': response, 'next': False})

            elif request.method == 'PUT':
                data = json.loads(request.data.decode())
                input_index = data['id']
                self.input = add_batch(self.inputs[input_index]).to(self.device)
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
                                'current': self.visualization.to_JSON()})

            return response

        @self.route('/api/visualisation', methods=['PUT'])
        def api_visualisation():
            data = json.loads(request.data.decode())
            vis_name = data['name']
            try:
                self.visualization = self.name2visualisations[vis_name].update(data['params'])
                self.cache[vis_name] = {}
                response = jsonify(self.visualization.to_JSON())
            except KeyError:
                response = Response(status=500,
                                    response='Visualisation {} not supported or does not exist'.format(vis_name))
            return response

        @self.route('/api/model/layer/output/<id>')
        def api_model_layer_output(id):
            try:
                self.layer = self.traced[id].module
                self.outputs = self.get_outputs()
                if len(self.outputs.shape) < 3: raise ValueError('Outputs must be a 3-D tensor.')

                lower = int(request.args['last'])
                upper = min((lower + self.MAX_LINKS_EVERY_REQUEST), self.outputs.shape[0])
                # adding time to prevent the browser from caching the link
                response = [f'/api/model/image/{time.time()}/{i}' for i in range(lower, upper)]
                response = jsonify({'links': response, 'next': lower + 1 < upper})

            except KeyError:
                response = Response(status=500, response='Index not found.')
            except ValueError:
                response = Response(status=404, response='Outputs must be an array of images')
            except StopIteration:
                response = jsonify({'links': [], 'next': False})

            return response

        @self.route('/api/model/image/<time>/<output_id>')
        def api_model_layer_output_image(time, output_id):
            output_id = int(output_id)
            try:
                image = self.make_image(output_id)
                return send_file(image, mimetype='image/jpeg')
            except KeyError:
                return Response(status=500, response='Index not found.')

    def make_image(self, output_id):
        output = self.outputs[output_id].detach().cpu()
        pil_img = ToPILImage()(output)
        img_io = io.BytesIO()
        pil_img.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return img_io

    def get_outputs(self):
        vis_name = self.visualization.name
        vis_cache = self.cache[vis_name]
        if (self.layer, self.input) not in vis_cache:
            vis_cache[(self.layer, self.input)] = self.visualization(self.input.clone(),
                                                                     self.layer)
            self.logger.info('Computing Visualisation')
        else:
            self.logger.debug('Cached')

        outputs, _ = vis_cache[(self.layer, self.input)]
        return outputs

    def setup_tracer(self):
        # instantiate a Tracer object and trace one input
        self.tracer = ModuleTracer(module=self.module, device=self.device)
        self.tracer(self.input)
        # store the traced graph as a dictionary
        self.traced = self.tracer.__dict__()

    def setup_visualisations(self, visualisations):
        visualisations = [*self.default_visualisations, *visualisations]
        self.visualisations = [v(self.module, self.device) for v in visualisations]
        self.name2visualisations = {v.name: v for v in self.visualisations}
        self.visualization = self.visualisations[0]
