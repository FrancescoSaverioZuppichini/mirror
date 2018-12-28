class Base:
    def __init__(self, module, device):
        self.module, self.device = module, device
        self.handles = []

    def clean(self):
        [h.remove() for h in self.handles]


    def __call__(self, inputs, layer, *args, **kwargs):
        return inputs, {}

class LayerFeatures(Base):
    def __init__(self, layer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grads, self.outputs = None, None
        self.layer = layer

    def store_grads(self):
        def hook(module, grad_in, grad_out):
            self.clean()
            self.grads = grad_in[0]

        self.handles.append(self.layer.register_backward_hook(hook))

    def store_outputs(self):
        def hook(module, inputs, outputs):
            self.clean()
            self.outputs = outputs

        self.handles.append(self.layer.register_backward_hook(hook))

    @property
    def has_grads(self):
        return self.grads is not None

    @property
    def has_outputs(self):
        return self.outputs is not None

class Visualisation(Base):

    def trace(self, module, inputs):
        self.modules = []

        def trace(module, inputs, outputs):
            self.modules.append(module)

        def traverse(module):
            for m in module.children():
                traverse(m)
            is_leaf = len(list(module.children())) == 0
            if is_leaf: self.handles.append(module.register_forward_hook(trace))

        traverse(module)

        _ = module(inputs)

        self.clean()