import json
import io
import torch
import time
import logging
from flask import Flask, request, Response, send_file, jsonify
from torchvision.transforms import ToPILImage
from .visualisations.web import Weights
from .ModuleHelper import ModuleHelper
from .utils import device, add_batch


class App(Flask):
    default_visualisations = [Weights]
    MAX_LINKS_EVERY_REQUEST = 64

    def __init__(self, inputs, model, visualisations=[], device=device):
        super().__init__(__name__)
        if len(inputs) <= 0: raise ValueError('At least one input is required.')
        self.inputs, self.model = inputs, model
        self.device = device
        self.logger.setLevel(logging.INFO)
        with torch.no_grad():
            self.module = model.to(self.device).eval()
        self.outputs: torch.Tensor = torch.empty(0).to(self.device)
        self.input = add_batch(self.inputs[0]).to(self.device)  # add 1 dim for batch
        self.module = self.module
        # instantiate a ModuleHelper object 
        self.module_helper = ModuleHelper(module=self.module, device=self.device)
        self.module_helper()
        
        self.setup_visualisations(visualisations)
        self.cache = {vis.name: {} for vis in
                      self.visualisations}  # internal cache used to store the results of each visualization

        @self.route('/')
        def root():
            return self.send_static_file('index.html')

        @self.route('/api/model', methods=['GET'])
        def api_model():
            """
            Thid endpoint returns the JSON representation of the current model. 
            
            :return: A HTTP response with the JSON representation of the current model
            :rtype: [type]
            """
            model = self.module_helper.serialize()

            response = jsonify(model)

            return response

        @self.route('/api/inputs', methods=['GET', 'PUT'])
        def api_inputs():
            """
            Thid endpoint returns the current visualization outputs if the method is GET or it change the current input if PUT.
            
            :return: A HTTP response carrying the current visualization outputs
            :rtype: [type]
            """
            response = Response('404', 'Invalid Method.')

            if request.method == 'GET':
                # return the current visualization outputs
                self.outputs = self.inputs
                # by using the currenct timestamp in the reply link we ensure to not cache client side the images
                response = [f'/api/model/image/{time.time()}/{i}' for i in range(len(self.outputs))]
                response = jsonify({'links': response, 'next': False})

            elif request.method == 'PUT':
                # change the current input based on the sent id
                data = json.loads(request.data.decode())
                input_index = data['id']
                self.input = add_batch(self.inputs[input_index]).to(self.device)
                response = jsonify(data)

            return response

        @self.route('/api/model/layer/<id>')
        def api_model_layer(id):
            id = int(id)
            name = self.module_helper[id].name

            return Response(response=name)

        @self.route('/api/visualisation', methods=['GET'])
        def api_visualisations():
            """
            This endpoint returns a list of visualisations. They are serialised (converted to JSON).
            
            :return: A HTTP response containing the serialised list of visualisations
            :rtype: [type]
            """
            serialised = [v.to_JSON() for v in self.visualisations]
            response = jsonify({'visualisations': serialised,
                                'current': self.visualization.to_JSON()})

            return response

        @self.route('/api/visualisation', methods=['PUT'])
        def api_visualisation():
            """
            This endpoint set the params to the a visualisation.
            
            :return: A HTTP response containing the serialized updated visualization.
            :rtype: [type]
            """
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
                self.module = self.module_helper[id].layer
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
            """This endpoint returns a single image from a specific visualization output 
            defined by the parameter output_dir
            
            :param time: [description]
            :type time: [type]
            :param output_id: [description]
            :type output_id: [type]
            :return: [description]
            :rtype: [type]
            """
            output_id = int(output_id)
            try:
                output = self.outputs[output_id]
                image = self.make_image(output)
                return send_file(image, mimetype='image/jpeg')
            except KeyError:
                return Response(status=500, response='Index not found.')

    def make_image(self, image: torch.Tensor) -> io.BytesIO:
        """
        Create an image in memory from a tensor.
        
        :param output_id: [description]
        :type output_id: [type]
        :return: [description]
        :rtype: [type]
        """
        output = image.detach().cpu()
        pil_img = ToPILImage()(output)
        img_io = io.BytesIO()
        pil_img.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return img_io

    def get_outputs(self):
        vis_name = self.visualization.name
        vis_cache = self.cache[vis_name]
        if (self.module, self.input) not in vis_cache:
            vis_cache[(self.module, self.input)] = self.visualization(self.input.clone(),
                                                                     self.module)
            self.logger.info('Computing Visualisation')
        else:
            self.logger.debug('Cached')

        outputs, _ = vis_cache[(self.module, self.input)]
        return outputs

    def setup_visualisations(self, visualisations):
        visualisations = [*self.default_visualisations, *visualisations]
        self.visualisations = [v(self.module, self.device) for v in visualisations]
        self.name2visualisations = {v.name: v for v in self.visualisations}
        self.visualization = self.visualisations[0]
