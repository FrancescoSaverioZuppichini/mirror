from mirror.visualisations.WebVisualisation import WebVisualisation
from functools import partial
from .core import *

class WebClassVisualisation(WebVisualisation):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_class = None
        self.guide = False

    def __call__(self, input_image, layer):
        try:
            self.target_class = int(self.target_class)
        except:
            self.target_class = None

        return self.vis(input_image, None,
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

class BackPropVis(WebClassVisualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vis = SaliencyMap(self.module, self.device)

    @property
    def name(self):
        return 'Back Prop'


class GradCamVis(WebClassVisualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vis = GradCam(self.module, self.device)

    @property
    def name(self):
        return 'Grad Cam'

class DeepDreamVis(WebVisualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vis = DeepDream(self.module, self.device)
        self.octaves = 4
        self.lr = 0.1
        self.scale = 0.7

    @property
    def name(self):
        return 'Deep dream'

    def __call__(self, input_image, layer):
        return self.vis(input_image, layer,
                        self.octaves,
                        self.scale,
                        self.lr)
    @property
    def params(self):
        return {
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
            },
            'lr': {
                'type': 'slider',
                'min': 0.001,
                'max': 1,
                'value': self.lr,
                'step': 0.001,
                'params': {}
            }
        }


class WeightsVis(WebVisualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vis = Weights(self.module, self.device)

    def __call__(self, inputs, layer):
        return self.vis(inputs, layer)

    @property
    def name(self):
        return 'Weights'
