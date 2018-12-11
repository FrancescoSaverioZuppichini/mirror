import json
import io
import numpy as np
import torch
import time

from flask import Flask, request, Response, send_file, jsonify
from .visualisations import WeightsVisualisation
from PIL import Image
import pprint
from torchvision.transforms import ToPILImage

class Builder:
    def __init__(self):
        self.outputs = None
        self.cache = {}
        self.visualisations = {}
        self.current_vis = None
        self.device  = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    def build(self, input, model, tracer, visualisations=[]):
        input = input.to(self.device)
        model = model.to(self.device)

        visualisations = [v(model, tracer, self.device) for v in visualisations]
        self.visualisations = [WeightsVisualisation(model, tracer, self.device), *visualisations]

        self.name2visualisations = { v.name : v for v in self.visualisations}
        self.current_vis =  self.visualisations[0]

        app = Flask(__name__)
        MAX_LINKS_EVERY_REQUEST = 64


        @app.route('/')
        def root():
            return app.send_static_file('index.html')

        @app.route('/api/model', methods=['GET'])
        def api_model():
            model = tracer.serialized

            response = jsonify(model)

            return response

        @app.route('/api/model/layer/<id>')
        def api_model_layer(id):
            id = int(id)
            name = str(tracer.idx_to_value[id])

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
                # TODO I should think on a cleaver way to update properties and params
                self.name2visualisations[vis_key].properties = data
                self.name2visualisations[vis_key].params = self.name2visualisations[vis_key].properties['params']
                self.current_vis = self.name2visualisations[vis_key]
                self.name2visualisations[vis_key].cache = {}

                response = jsonify(self.name2visualisations[vis_key].properties)

            return response

        @app.route('/api/model/layer/output/<id>')
        def api_model_layer_output(id):
            try:
                layer = tracer.idx_to_value[id].v

                if input not in self.current_vis.cache: self.current_vis.cache[input] = {}
                # TODO need to cache for vis
                layer_cache = self.current_vis.cache[input]

                # layer_cache[layer] = self.current_vis(input, layer)
                input_clone = input.clone()
                if layer not in layer_cache:
                    layer_cache[layer] = self.current_vis(input_clone, layer)
                    del input_clone
                else: print('cached')
                self.outputs = layer_cache[layer]

                outputs = self.outputs

                if len(outputs.shape) < 3:  raise ValueError

                last = int(request.args['last'])
                max = min((last + MAX_LINKS_EVERY_REQUEST), outputs.shape[0])

                response = ['/api/model/image/{}/{}/{}/{}/{}'.format(hash(input),
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