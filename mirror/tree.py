from pprint import pprint
import sys

class Node:
    def __init__(self, p, v):
        self.p = p
        self.v = v
        self.c = []
        self.id = str(hash(v) % ((sys.maxsize + 1) * 2))
        self.traced = None

    def __str__(self):
        return str(self.v)

    def apply(self, func):
        for c in self.c:
            c.apply(func)

    def __str__(self):
        return str(self.v)

    def __call__(self, module, input, output):
        self.traced = (module, input, output)

    def to_dict(self):
        return { 'id': self.id, 'name' : str(self.v), 'children' : [] }

def traverse(node, func):
    for c in node.c:
        func(node, c)
        traverse(c, func)

def make_tree(model):
    root = Node(p=None, v=model)
    return root

def build(node, module):
    for m in module.children():
        if m not in node.c:
            child = Node(p=node, v=m)
            node.c.append(child)
            build(child, m)

def serialise(root):

    dict = root.to_dict()

    def inner(node, dict):
        for c in node.c:
            dict['children'].append(inner(c, c.to_dict()))
        return dict
    inner(root, dict)

    return dict

def make_map(node, map):
    map[node.id] = node
    for c in node.c:
        make_map(c, map)

class Tracer:
    def __init__(self, module):
        self.root = Node(p=None, v=module)
        self.module = module
        self.operations = []
        self.serialized = {}
        self.idx_to_value = {}

    def register_forward_hooks(self, node):
        node.v.register_forward_hook(node)
        for c in node.c:
            self.register_forward_hooks(c)

    def register_forward_hook(self, p, c):
        c.v.register_forward_hook(c)

    def get_operations(self, node):
        #     leaf
        if len(node.c) == 0:
            self.operations.append(node.traced)
        for c in node.c:
            self.get_operations(c)


    def __call__(self, input):
        build(self.root, self.module)
        # traverse(self.root, self.register_forward_hook)
        self.register_forward_hooks(self.root)
        output = self.root.v(input)

        self.get_operations(self.root)

        self.serialized = serialise(self.root)
        make_map(self.root, self.idx_to_value)

        return output





