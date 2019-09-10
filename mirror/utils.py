from collections import OrderedDict
class EnsureType(OrderedDict):
    def __init__(self, *args, type=str, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = type

    def __getitem__(self, item):
        val = self.get(item)
        if item is 'value':
            val = self.type(self.get(item))
        return val