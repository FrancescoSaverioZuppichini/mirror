class Visualisation:
    def __init__(self, module, tracer):
        self.module, self.tracer = module, tracer
        self.outputs = []

    @property
    def name(self):
        return 'weights'

    @property
    def params(self):
        return [{ 'name' : 'lr',
                  'params': [ { 'name' : 'slider',
                              'params': { 'min': 0.0001, 'max': 1}} ]}
                ]

    @property
    def properties(self):
        return {'name': self.name, 'params': self.params}

    def __call__(self, inputs, layer):
        """
        Do something with the inputs
        :param inputs:
        :return:
        """
        pass
