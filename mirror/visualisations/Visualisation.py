class Visualisation:
    def __init__(self, module, tracer):
        self.module, self.tracer = module, tracer
        self.outputs = []
        self.params = self.init_params()
        self.properties = self.init_properties()
        self.cache = {}

    @property
    def name(self):
        pass
    def init_params(self):
        return []

    def init_properties(self):
        return {'name': self.name,
                'type': 'radio',
                'value': False,
                'params': self.params
                }

    def __call__(self, inputs, layer):
        """
        Do something with the inputs
        :param inputs:
        :return:
        """
        pass
