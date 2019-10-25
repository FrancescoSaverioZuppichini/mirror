import json

class WebInterface():
    def __init__(self, callable, params, name):
        self.callable = callable
        self.params = params
        self.name = name

    def __call__(self, *args, **kwargs):
        return self.callable(*args, **self.call_params, **kwargs)

    @property
    def call_params(self):
        return {k: v['value'] for k, v in self.params.items()}

    def to_JSON(self):
        return {'name': self.name, 'params': self.params}

    def update(self, data):
        self.params = data
        return self

    @classmethod
    def from_visualisation(cls, visualisation, module, device, *args, **kwargs):
        return cls(visualisation(module, device), *args, **kwargs)

    def __repr__(self):
        return str(self.call_params)
