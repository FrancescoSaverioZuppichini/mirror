from .Visualisation import Visualisation


class DummyVisualisation(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def __call__(self, inputs, layer):
        return inputs

    @property
    def name(self):
        return 'dummy'
