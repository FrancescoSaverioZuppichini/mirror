import sys


class TracedNode():
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.module = None
        self.input = None
        self.output = None

    @property
    def id(self):
        return str(hash(self.module) % ((sys.maxsize + 1) * 2))

    @property
    def name(self):
        return str(self.module)

    def to_JSON(self):
        return {'id': self.id, 'name': self.name, 'children': [child.to_JSON() for child in self.children]}

    def __dict__(self):
        """
        Recursively add items with not children to flat the dictionary.
        :return:
        """
        v = {}
        if len(self.children) <= 0:
            v = {self.id: self}
        else:
            for child in self.children:
                v = {**v, **child.__dict__()}
        return v

    def __call__(self, module, input, output):
        self.module = module
        self.input = input
        self.output = output


class ModuleTracer():
    """
    Hook to each submodule of a module and create a graph of TracedNode in order to store the
    correct execution of an input through the model.
    """

    def __init__(self, module):
        super().__init__()
        self.module = module
        self.handles = []
        self.root = None

    def trace(self, module, root=None):
        """
        Recursively creates a tree of TracedNode
        :param module: Current module
        :param root: Parent Node
        :return: New Node
        """
        root = TracedNode(parent=root)
        self.handles.append(module.register_forward_hook(root))
        for child in module.children():
            root.children.append(self.trace(child, root))
        return root

    def __call__(self, x):
        self.root = self.trace(self.module, None)
        _ = self.module(x)
        self.clean()
        return self

    def __repr__(self):
        return self.to_JSON().__repr__()

    def clean(self):
        [h.remove() for h in self.handles]

    def __dict__(self):
        return self.root.__dict__()

    def to_JSON(self):
        return self.root.to_JSON()
