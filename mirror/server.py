import json
import io
import numpy as np
import torch
import time

from flask import Flask, request, Response, send_file, jsonify
from .visualisations import WeightsVis
from PIL import Image
import pprint
from torchvision.transforms import ToPILImage
from .tree import Tracer
from .utils import module2traced

class Builder:
    default_visualisations = [WeightsVis]
    MAX_LINKS_EVERY_REQUEST = 64

    def __init__(self):
        self.cache = {} # internal cache used to store the results
        self.outputs = None # holds the current output from a visualisation
        self.current_vis = None
        self.current_input = None
        self.inputs= []
        self.device  = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    def build(self, inputs, model, visualisations=[]):
        if len(inputs) <= 0: raise ValueError('At least one input is required.')

        self.inputs, self.model = inputs, model

        self.current_input = self.inputs[0].unsqueeze(0).to(self.device) # add 1 dim for batch
        model = model.to(self.device)
        model.eval()
        # instantiate a Tracer object to create a graph from the model
        self.tracer = Tracer(module=model)
        self.tracer(self.current_input)
        # instantiate visualisations
        visualisations = [*self.default_visualisations, *visualisations]

        self.visualisations= [v(model, self.device) for v in visualisations]
        self.name2visualisations = { v.name : v for v in self.visualisations}
        self.current_vis =  self.visualisations[0]

        app = Flask(__name__)

        @app.route('/')
        def root():
            return app.send_static_file('index.html')

        @app.route('/api/model', methods=['GET'])
        def api_model():
            model = self.tracer.serialized

            response = jsonify(model)

            return response

        @app.route('/api/inputs', methods=['GET', 'PUT'])
        def api_inputs():
            if request.method == 'GET':
                self.outputs = self.inputs

                response = ['/api/model/image/{}/{}/{}/{}/{}'.format(hash(None),
                                                                     hash(None),
                                                                     hash(time.time()),
                                                                     id,
                                                                     i) for i in range(len(self.inputs))]

                response = jsonify({'links': response, 'next': False })

            elif request.method == 'PUT':
                data = json.loads(request.data.decode())

                input_index = data['id']

                self.current_input = self.inputs[input_index].unsqueeze(0).to(self.device)

                response = jsonify(data)

            return response


        @app.route('/api/model/layer/<id>')
        def api_model_layer(id):
            id = int(id)
            name = str(self.tracer.idx_to_value[id])

            return Response(response=name)

        @app.route('/api/visualisation', methods=['GET'])
        def api_visualisations():
            serialised = [v.properties for v in self.visualisations]

            response = jsonify({ 'visualisations': serialised,
                                   'current': self.current_vis.properties})

            return response

        @app.route('/api/visualisation', methods=['PUT'])
        def api_visualisation():
            data = json.loads(request.data.decode())

            vis_key = data['name']

            if vis_key not in self.name2visualisations:
                response = Response(status=500, response='Visualisation {} not supported or does not exist'.format(vis_key))
            else:
                self.current_vis = self.name2visualisations[vis_key]
                # TODO I should think on a cleaver way to update properties and params
                self.current_vis.properties = data
                self.current_vis.params = self.current_vis.properties['params']
                self.current_vis.cache = {}

                response = jsonify(self.current_vis.properties)

            return response

        @app.route('/api/model/layer/output/<id>')
        def api_model_layer_output(id):
            try:

                layer = self.tracer.idx_to_value[id].v

                if self.current_input not in self.current_vis.cache: self.current_vis.cache[self.current_input] = {}

                layer_cache = self.current_vis.cache[self.current_input]
                # always clone the input to avoid being modified
                input_clone = self.current_input.clone()

                if layer not in layer_cache:
                    layer_cache[layer] = self.current_vis(input_clone, layer)
                    del input_clone
                else: print('cached')

                self.outputs, _ = layer_cache[layer]

                if len(self.outputs.shape) < 3:  raise ValueError

                last = int(request.args['last'])
                max = min((last + self.MAX_LINKS_EVERY_REQUEST), self.outputs.shape[0])

                response = ['/api/model/image/{}/{}/{}/{}/{}'.format(hash(self.current_input),
                                                                  hash(self.current_vis),
                                                                  hash(time.time()),
                                                                  id,
                                                                  i) for i in range(last, max)]

                response = jsonify({ 'links' : response, 'next': last + 1< max})


            except KeyError:
                response = Response(status=500, response='Index not found.')
            except ValueError:
                response = Response(status=404, response='Outputs must be an array of images')
            except StopIteration:
                response = jsonify({ 'links' : [], 'next': False})

            return response

        @app.route('/api/model/image/<input_id>/<vis_id>/<layer_id>/<time>/<output_id>')
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

        return app