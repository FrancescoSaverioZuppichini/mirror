from mirror.visualisations.WebVisualisation import WebInterface
from mirror.visualisations.core import Base


def dummy(inputs, layer, repeat=1):
    return inputs.repeat(repeat, 1, 1, 1), None

class DummyVisualisation(WebInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visualisation = dummy
        self.repeat = 1
    @property
    def name(self):
        return 'dummy'

    @property
    def params(self):
        return {'repeat' : {
                     'type' : 'slider',
                     'min' : 1,
                     'max' : 100,
                     'value' : self.repeat,
                     'step': 1,
                     'params': {}
                 }
        }




vis = DummyVisualisation(None, None)

print(vis.params)

print(vis.update_params( {'repeat' : {
                     'type' : 'slider',
                     'min' : 1,
                     'max' : 100,
                     'value' : 2,
                     'step': 1,
                     'params': {}
                 }}))
print(vis.params)
