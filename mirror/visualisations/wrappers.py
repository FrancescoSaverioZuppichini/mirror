from mirror.visualisations.Visualisation import Visualisation

from .core import *

class BackPropVis(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vis = SaliencyMap(self.module, self.device)

    @property
    def name(self):
        return 'Backprop'

    def __call__(self, input_image, layer):
        target_class = self.params['class']['value']
        if target_class is not None: target_class = int(target_class)
        return self.vis(input_image, None,
                        self.params['guide']['value'],
                        target_class=target_class)

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


class GradCamVis(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vis = GradCam(self.module, self.device)

    @property
    def name(self):
        return 'Grad cam'

    def __call__(self, input_image, layer):
        target_class = self.params['class']['value']
        if target_class is not None: target_class = int(target_class)
        return self.vis(input_image, layer,
                        self.params['guide']['value'],
                        target_class)

    def init_params(self):
        return {'guide': {'type': 'radio',
                          'value': False
                          },
                'class': {
                    'type': 'textfield',
                    'label': 'id',
                    'value': None
                          }
                }

class DeepDreamVis(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vis = DeepDream(self.module, self.device)

    @property
    def name(self):
        return 'Deep dream'

    def __call__(self, input_image, layer):
        return self.vis(input_image, layer,
                        self.params['octaves']['value'],
                        self.params['scale']['value'],
                        self.params['lr']['value'])

    def init_params(self):
        return {'lr': {
            'type': 'slider',
            'min': 0.001,
            'max': 1,
            'value': 0.1,
            'step': 0.001,
            'params': {}
        },
            'octaves': {
                'type': 'slider',
                'min': 1,
                'max': 10,
                'value': 4,
                'step': 1,
                'params': {}
            },
            'scale': {
                'type': 'slider',
                'min': 0.1,
                'max': 1,
                'value': 0.7,
                'step': 0.1,
                'params': {}
            }
        }

class WeightsVis(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vis = Weights(self.module, self.device)

    def __call__(self, inputs, layer):
        return self.vis(inputs, layer)

    @property
    def name(self):
        return 'weights'

