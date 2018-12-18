import torch

from torch.nn import ReLU
from torch.autograd import Variable

from .Visualisation import Visualisation

from .misc_functions import (get_params,
                             convert_to_grayscale,
                             save_gradient_images,
                             get_positive_negative_saliency)

class Backprop():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gradients = None
        self.handles = []

    def store_first_layer_grad(self, first_layer):
        def store_grad(module, grad_in, grad_out):
            print('Backprop')
            self.gradients = grad_in[0]

        self.handles.append(first_layer.register_backward_hook(store_grad))

    def guide(self, module):
        def guide_relu(module, grad_in, grad_out):
            return (torch.clamp(grad_in[0], min=0.0),)

        for module in module.modules():
            if isinstance(module, ReLU):
                self.handles.append(module.register_backward_hook(guide_relu))

    def clean(self):
        [h.remove() for h in self.handles]

    def __call__(self, input_image, layer, module, device, first_layer, guide=False, target_class=None):
        self.clean()
        input_image = Variable(input_image, requires_grad=True).to(device)

        if guide: self.guide(module)
        self.store_first_layer_grad(first_layer)

        predictions = module(input_image)

        if target_class == None: _, target_class = torch.max(predictions, dim=1)

        one_hot_output = torch.zeros(predictions.size()).to(device)
        one_hot_output[0][target_class] = 1

        module.zero_grad()

        predictions.backward(gradient=one_hot_output)

        gradients_as_arr = self.gradients.data.cpu().numpy()[0]

        image = convert_to_grayscale(gradients_as_arr)
        image = torch.from_numpy(image).to(device)

        self.clean()

        return image.unsqueeze(0)


class BackPropVis(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vis = Backprop()

    @property
    def name(self):
        return 'Backprop'

    def __call__(self, input_image, layer):
        first_layer = self.tracer.operations[0][0]
        target_class = self.params['class']['value']
        if target_class is not None: target_class = int(target_class)
        return self.vis(input_image, layer, self.module, self.device, first_layer,
                        self.params['guide']['value'],
                        target_class)

    def init_params(self):
        return {'guide': {'type': 'radio',
                          'value': True
                          },
                'class': {
                    'type': 'textfield',
                    'label': 'id',
                    'value': None
                }
            }
