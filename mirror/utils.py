from collections import OrderedDict
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

add_batch = lambda x : x.unsqueeze(0)

class EnsureType(OrderedDict):
    def __init__(self, *args, type=str, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = type

    def __getitem__(self, item):
        val = self.get(item)
        if item is 'value':
            val = self.type(self.get(item))
        return val