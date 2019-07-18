from mirror.visualisations.WebVisualisation import WebInterface
from functools import partial
from .core import *

class WebClassInterface(WebInterface):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_class = None
        self.guide = False

    def __call__(self, input_image, layer):
        try:
            self.target_class = int(self.target_class)
        except:
            self.target_class = None

        return self.visualisation(input_image, None,
                        self.guide,
                        target_class=self.target_class)
    @property
    def params(self):
        return {'guide': {'type': 'radio',
                          'value': self.guide
                          },
                'target_class': {
                    'type': 'textfield',
                    'label': 'id',
                    'value': self.target_class
                }
            }

class WebBackProp(WebClassInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visualisation = SaliencyMap(self.module, self.device)

    @property
    def name(self):
        return 'Back Prop'


class WebGradCam(WebClassInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visualisation = GradCam(self.module, self.device)

    @property
    def name(self):
        return 'Grad Cam'

class WebDeepDream(WebInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visualisation = DeepDream(self.module, self.device)
        self.octaves = 4
        self.lr = 0.1
        self.scale = 0.7

    @property
    def name(self):
        return 'Deep dream'

    @property
    def params(self):
        return {'lr': {
            'type': 'slider',
            'min': 0.001,
            'max': 1,
            'value': self.lr,
            'step': 0.001,
            'params': {}
        },
            'octaves': {
                'type': 'slider',
                'min': 1,
                'max': 10,
                'value': self.octaves,
                'step': 1,
                'params': {}
            },
            'scale': {
                'type': 'slider',
                'min': 0.1,
                'max': 1,
                'value': self.scale,
                'step': 0.1,
                'params': {}
            }
        }


class WebWeights(WebInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vis = Weights(self.module, self.device)

    def __call__(self, inputs, layer):
        return self.vis(inputs, layer)

    @property
    def name(self):
        return 'Weights'
