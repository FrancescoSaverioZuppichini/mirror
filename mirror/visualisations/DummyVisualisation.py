from .Visualisation import Visualisation


class DummyVisualisation(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def __call__(self, inputs, layer):

        return inputs

    @property
    def name(self):
        return 'dummy'

    def init_properties(self):
        return {'name': self.name,
                'type': 'radio',
                'value': False,
                'params': self.params
                }