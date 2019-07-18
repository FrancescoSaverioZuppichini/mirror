class WebVisualisation:
    def __init__(self, module, device):
        self.module, self.device = module, device
        self.outputs = []
        self.cache = {}

    @property
    def name(self):
        return 'visualisation'

    def __call__(self, inputs, layer):
        """
        Do something with the inputs
        :param inputs:
        :return:
        """
        pass

    def clean_cache(self):
        self.cache = {}

    @property
    def params(self):
        return {}

    def update_params(self, params: dict):
        for k, v in params.items():
            if 'value' not in v: raise ValueError('params should contains a value.')
            setattr(self, k, v['value'])

    def to_JSON(self):
        return { 'name': self.name,
                'params': self.params }
