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
        # additional cache, we won't have to run again the input through the model
        if layer not in self.layer2values: self.module(inputs)

        output = self.layer2values[layer][1]

        b, c, h, w = output.shape
        # reshape to make an array of images 1-Channel
        output = output.view(c, b, h, w)

        return output

    @property
    def name(self):
        return 'weights'

