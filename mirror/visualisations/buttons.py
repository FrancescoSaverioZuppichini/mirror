class Radio():
    def __init__(self, value=False):
        self.value = value
        self.type = 'radio'


class TextField():
    def __init__(self, value=None, label=''):
        self.value = value
        self.label = label
        self.type = 'textfield'


class Slider():
    def __init__(self, value=None, min = 0, max = 1, step=0.1):
        self.value = min if value is None else value
        self.min, self.max, self.step = min, max, step
        self.type = 'slider'
