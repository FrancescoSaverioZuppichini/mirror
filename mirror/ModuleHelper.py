import sys


class LayerNode():
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []

    @property
    def id(self):
        return str(id(self.layer))

    @property
    def name(self):
        return str(self.layer)

    def __dict__(self):
        """
        Recursively add items with not children to flat the dictionary.
        :return:
        """
        v = {self.id: self}
        for child in self.children:
            v = {**v, **child.__dict__()}
        return v

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'children': [child.to_JSON() for child in self.children]
        }


class ModuleHelper():
    """
    This class is able to serialize a given module and to create a graph of LayerNode in order
    to look for a specific layer given an id
    """

    def __init__(self, module, device):
        super().__init__()
        self.module = module
        self.root = LayerNode(parent=None)
        self.name2layers = {}
        self.device = device

    def trace(self, module, root=None):
        """
        Recursively creates a tree of TracedLayer
        :param module: Current module
        :param root: Parent Node
        :return: New Node
        """
        root.layer = module
        for child in module.children():
            root.children.append(self.trace(child, LayerNode(parent=root)))
        return root

    def __call__(self):
        self.root = self.trace(self.module, self.root)
        self.name2layers = self.root.__dict__()
        return self

    def __repr__(self):
        return self.to_JSON().__repr__()
    
    def clean(self):
        [h.remove() for h in self.handles]

    def __getitem__(self, idx):
        return self.name2layers[idx]

    def serialize(self):
        return self.to_JSON()

    def to_JSON(self):
        return self.root.to_JSON()
