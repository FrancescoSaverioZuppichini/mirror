from .Visualisation import Visualisation

class DummyVisualisation(Visualisation):

    def __call__(self, inputs, layer):
        return inputs.repeat(self.properties['params'][0]['value'],1, 1, 1)

    @property
    def name(self):
        return 'dummy'

    def init_params(self):
        return [{ 'name' : 'repeat',
                 'type' : 'slider',
                 'min' : 1,
                 'max' : 100,
                 'value' : 3,
                 'step': 1,
                 'params': []
                 }]
