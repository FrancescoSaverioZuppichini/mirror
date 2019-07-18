class WebInterface():
    """
    Basic Web interface. It maps the visualisation to the web application in order to dynamically update its parameters.
    Also, it keeps an internal cache used to store the results.
    """
    def __init__(self, module, device):
        self.module, self.device = module, device
        self.outputs = []
        self.cache = {}
        self.visualisation = None

    @property
    def name(self):
        return 'visualisation'

    def __call__(self, input_image, layer):
        if self.visualisation is None: raise ValueError(
            'You need to override this class and provide a visualisation in the field .visualisation.')
        params = {k: v['value'] for k, v in self.params.items()}
        return self.visualisation(input_image, layer, **params)

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
        return {'name': self.name,
                'params': self.params}
