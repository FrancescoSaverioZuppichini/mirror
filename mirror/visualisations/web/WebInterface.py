import json

class WebInterface():
    def __init__(self, callable, params, name):
        self.callable = callable
        self.params = params
        self.name = name

    def __call__(self, input_image, layer):
        if self.callable is None: raise ValueError(
            'You need to override this class and provide a visualisation in the field .visualisation.')
        return self.callable(input_image, layer, **self.call_params)

    @property
    def call_params(self):
        return {k: v['value'] for k, v in self.params.items()}

    def to_JSON(self):
        return {'name': self.name, 'params': self.params}

    def from_JSON(self, data):
        self.params = data

    @classmethod
    def from_visualisation(cls, visualisation, module, device, *args, **kwargs):
        return cls(visualisation(module, device), *args, **kwargs)

    def __repr__(self):
        return str(self.call_params)