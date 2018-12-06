class Visualisation:
    def __init__(self, module, tracer):
        self.module, self.tracer = module, tracer
        self.outputs = []
        self.params = self.init_params()
        self.properties = self.init_properties()


    @property
    def name(self):
        return 'weights'

    def init_params(self):
        return [{ 'name' : 'lr',
                  'type' : 'slider',
                  'min': 0,
                  'max': 10,
                  'value': 0,
                  'params' : []
                  }]


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
