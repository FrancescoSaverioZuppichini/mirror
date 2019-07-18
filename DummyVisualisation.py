from mirror.visualisations.WebVisualisation import WebVisualisation
from mirror.visualisations.core import Base

class DummyVisualisation(WebVisualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_repeat = 1

    def __call__(self, inputs, layer):
        return inputs.repeat(self.n_repeat,1, 1, 1), None

    @property
    def name(self):
        return 'dummy'

    @property
    def params(self):
        return {'n_repeat' : {
                     'type' : 'slider',
                     'min' : 1,
                     'max' : 100,
                     'value' : self.n_repeat,
                     'step': 1,
                     'params': {}
                 }
        }
