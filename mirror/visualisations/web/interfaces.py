from mirror.visualisations.web.WebInterface import WebInterface
from mirror.visualisations.core import *
from functools import partial

class_parameters = lambda: {'guide': {'type': 'radio',
                                      'value': False
                                      },
                            'target_class': {
                                'type': 'textfield',
                                'label': 'id',
                                'value': None}
                            }

Weights = partial(WebInterface.from_visualisation, Weights, params={}, name='Weights')
BackProp = partial(WebInterface.from_visualisation, SaliencyMap, params=class_parameters(), name='Back Prop')
GradCam = partial(WebInterface.from_visualisation, GradCam, params=class_parameters(), name='Grad CAM')

deep_dream_params = {'lr':
    {
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

DeepDream = partial(WebInterface.from_visualisation, DeepDream, params=deep_dream_params, name='Deep Dream')
