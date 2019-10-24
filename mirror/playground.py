import json
import io
import torch
import time

from dataclasses import dataclass, field
# from flask import Flask, request, Response, send_file, jsonify
# from torchvision.transforms import ToPILImage
# from .visualisations.web import Weights
# from .ModuleTracer import ModuleTracer
# from .utils import device, add_batch
from collections.abc import Iterable


@dataclass
class Cache:
    _state: dict = field(default_factory=dict)
    _operations : dict = field(default_factory=dict)

    def __setitem__(self, keys, value):
        if len(keys) == 1: self._state[keys[0]] = value
        else:
            self._state[keys[0]] = Cache()
            self._state[keys[0]].__setitem__(keys[1:], value)

    def __getitem__(self, keys):
        if not isinstance(keys, Iterable): state = self._state[keys]
        elif len(keys) == 1: state = self._state[keys[0]]
        elif isinstance(self._state[keys[0]], Cache):
            state = self._state[keys[0]][keys[1:]]
        return state

    def contains(self, keys):
        return keys in self._state

    def clean(self, keys=None):
        if not isinstance(keys, Iterable):
            del self._state[keys]
        elif len(keys) == 1:
            del self._state[keys[0]]
        elif isinstance(self._state[keys[0]], Cache):
            state = self._state[keys[0]].clean(keys[1:])

cache = Cache()
cache[('weights', 0, 'module')] = 'test'
print(cache)
print(cache[('weights', 0)])
cache.clean(('weights', 0))
print(cache[('weights', 0)])


# print(cache.contains(('weights', 0)))#
# class Mirror():
#     default_visualisations = [Weights]
#     MAX_LINKS_EVERY_REQUEST = 64
#
#     def __init__(self, inputs, model, visualisations=None, device=device):
#         super().__init__(__name__)
#         self.inputs, self.model = inputs, model
#         self.device = device
#         self.cache = {}  # internal cache used to store the results
#         self.outputs = None  # holds the current output from a visualisation
#         if len(inputs) <= 0: raise ValueError('At least one input is required.')
#         self.current_input = add_batch(self.inputs[0])  # add 1 dim for batch
#         self.module = model.to(self.device).eval()
#         # instantiate a Tracer object and trace one input
#         self.tracer = ModuleTracer(module=self.module)(self.current_input)
#         # store the traced graph as a dictionary
#         self.traced = self.tracer.__dict__()
#         visualisations = [*self.default_visualisations, *visualisations]
#         self.visualisations = [v(self.module, self.device) for v in visualisations]
#         self.name2visualisations = {v.name: v for v in self.visualisations}
#         self.current_vis = self.visualisations[0]
#
#         @property
#         def traced_graph(self):
#             return self.tracer.to_JSON()
#
#         def model_layer(self, id):
#             return self.tracer[id].name
#
#         @self.route('/api/inputs', methods=['GET', 'PUT'])
#         def api_inputs():
#             if request.method == 'GET':
#                 self.outputs = self.inputs
#
#                 response = ['/api/model/image/{}/{}/{}/{}/{}'.format(hash(None),
#                                                                      hash(None),
#                                                                      hash(time.time()),
#                                                                      id,
#                                                                      i) for i in range(len(self.inputs))]
#
#                 response = jsonify({'links': response, 'next': False})
#
#             elif request.method == 'PUT':
#                 data = json.loads(request.data.decode())
#                 input_index = data['id']
#                 self.current_input = add_batch(self.inputs[input_index]).to(self.device)
#                 response = jsonify(data)
#
#             return response
#
#         @self.route('/api/visualisation', methods=['PUT'])
#         def api_visualisation():
#             data = json.loads(request.data.decode())
#             vis_name = data['name']
#
#             self.current_vis = self.name2visualisations[vis_name]
#             self.current_vis.from_JSON(data['params'])
#             self.cache.clean(vis_name)
#             response = jsonify(self.current_vis.to_JSON())
#
#             return response
#
#         @self.route('/api/model/layer/output/<id>')
#         def api_model_layer_output(id):
#             try:
#
#                 layer = self.traced[id].module
#                 self.current_input = self.current_input.to(self.device)
#                 if self.current_input not in self.current_vis.cache: self.current_vis.cache[self.current_input] = {}
#
#                 layer_cache = self.current_vis.cache[self.current_input]
#                 # always clone the input to avoid being modified
#                 input_clone = self.current_input.clone()
#
#                 if layer not in layer_cache:
#                     layer_cache[layer] = self.current_vis(input_clone, layer)
#                     del input_clone
#                 else:
#                     print('[INFO] cached')
#
#                 self.outputs, _ = layer_cache[layer]
#
#                 if len(self.outputs.shape) < 3:  raise ValueError
#
#                 last = int(request.args['last'])
#                 max = min((last + self.MAX_LINKS_EVERY_REQUEST), self.outputs.shape[0])
#
#                 response = ['/api/model/image/{}/{}/{}/{}/{}'.format(hash(self.current_input),
#                                                                      hash(self.current_vis),
#                                                                      hash(time.time()),
#                                                                      id,
#                                                                      i) for i in range(last, max)]
#
#                 response = jsonify({'links': response, 'next': last + 1 < max})
#
#
#             except KeyError:
#                 response = Response(status=500, response='Index not found.')
#             except ValueError:
#                 response = Response(status=404, response='Outputs must be an array of images')
#             except StopIteration:
#                 response = jsonify({'links': [], 'next': False})
#
#             return response
#
#         @self.route('/api/model/image/<input_id>/<vis_id>/<layer_id>/<time>/<output_id>')
#         def api_model_layer_output_image(input_id, vis_id, layer_id, time, output_id):
#             output_id = int(output_id)
#             try:
#                 output = self.outputs[output_id]
#                 output = output.detach().cpu()
#                 pil_img = ToPILImage()(output)
#                 img_io = io.BytesIO()
#                 pil_img.save(img_io, 'JPEG', quality=70)
#                 img_io.seek(0)
#                 return send_file(img_io, mimetype='image/jpeg')
#             except KeyError:
#                 return Response(status=500, response='Index not found.')
