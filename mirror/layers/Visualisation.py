class Visualisation:
    def __init__(self, module, layer, tracer):
        self.module, self.layer, self.tracer = module, layer, tracer
        self.outputs = []

    def __call__(self, inputs):
        """
        Do something with the inputs
        :param inputs:
        :return:
        """
        pass

