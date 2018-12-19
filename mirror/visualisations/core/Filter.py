from mirror.visualisations.Visualisation import Visualisation

from mirror.visualisations.Visualisation import Visualisation

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import SGD
from torchvision import models
from torch.autograd import Variable
import scipy.ndimage as nd
import numpy as np
from skimage.util import view_as_blocks, view_as_windows, montage

from torchvision import transforms
import torchvision.transforms.functional as TF
from PIL import Image, ImageFilter, ImageChops


class Filter(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.transformMean = [0.485, 0.456, 0.406]
        self.transformStd = [0.229, 0.224, 0.225]

        self.transform_preprocess = transforms.Compose([
            transforms.Normalize(
                mean=self.transformMean,
                std=self.transformStd
            )
        ])

        self.mean = torch.Tensor(self.transformStd).to(self.device)
        self.std = torch.Tensor(self.transformMean).to(self.device)

        self.out = None

    def toImage(self, input):
        return input * self.std + self.mean


    def __call__(self, inputs, layer, n_repeat=6, scale_factor=0.7):
        inputs = self.transform_preprocess(inputs.squeeze().cpu()).to(self.device).unsqueeze(0)

        self.image_var = Variable(inputs.to(self.device), requires_grad=True).to(self.device)

        self.optimizer = torch.optim.Adam([self.image_var], lr=self.params['lr']['value'])

        def hook(module, input, output):
            if module == layer:
                self.layer_output = output
                self.optimizer.zero_grad()

                loss = -torch.norm(self.layer_output[0,2])
                loss.backward()
                self.optimizer.step()


        handle = layer.register_forward_hook(hook)

        for i in range(4):
            try:
                self.module(self.image_var)
            except:
                pass

        handle.remove()

        dreamed = self.image_var.grad.data.squeeze()
        c, w, h = dreamed.shape

        dreamed = dreamed.view((w, h, c))
        # dreamed = torch.clamp(dreamed, 0.0, 1.0)
        dreamed = dreamed * self.std + self.mean
        dreamed = dreamed.view((c, w, h))

        return dreamed.unsqueeze(0)

    @property
    def name(self):
        return 'filter'

    def init_params(self):
        return {'lr' : {
                 'type': 'slider',
                 'min': 0.001,
                 'max': 1,
                 'value': 0.1,
                 'step': 0.001,
                 'params': {}
                 }
        }
