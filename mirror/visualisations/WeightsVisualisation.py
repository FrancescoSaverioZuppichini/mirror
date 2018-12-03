from .Visualisation import Visualisation

class WeightsVisualisation(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.layer2values = {}

    def hook(self, module, input, output):
        self.layer2values[module] = input, output

    def __call__(self, inputs, layer):
        for m in self.module.modules():
            m.register_forward_hook(self.hook)

        if layer not in self.layer2values: self.module(inputs)

        return self.layer2values[layer][1]

