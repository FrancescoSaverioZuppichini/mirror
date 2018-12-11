from .Visualisation import Visualisation

class DummyVisualisation(Visualisation):

    def __call__(self, inputs, layer):
        return inputs.repeat(self.params['repeat']['value'],1, 1, 1)

    @property
    def name(self):
        return 'dummy'

    def init_params(self):
        return {'repeat' : {
                 'type' : 'slider',
                 'min' : 1,
                 'max' : 100,
                 'value' : 3,
                 'step': 1,
                 'params': {}
                 }}
