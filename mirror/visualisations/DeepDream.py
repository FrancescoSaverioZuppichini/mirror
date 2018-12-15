from .Visualisation import Visualisation

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


class DeepDream(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trace = (None, None, None)

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
        self.handle = None


    def register_hooks(self):
        if self.handle: self.handle.remove()

        def hook(module, input, output):
            if module == self.layer:
                self.layer_output = output

                self.optimizer.zero_grad()
                loss = -torch.norm(self.layer_output)
                loss.backward()
                self.optimizer.step()

                raise Exception('Layer found!')

        return self.layer.register_forward_hook(hook)

    def toImage(self, input):
        return input * self.std + self.mean

    def step(self, image, steps=5, save=False):

        self.module.zero_grad()
        image_pre = self.transform_preprocess(image.squeeze().cpu()).to(self.device).unsqueeze(0)
        self.image_var = Variable(image_pre, requires_grad=True).to(self.device)

        self.optimizer = torch.optim.Adam([self.image_var], lr=self.params['lr']['value'])

        for i in range(steps):
            try:
                self.module(self.image_var)
            except: pass

        dreamed = self.image_var.data.squeeze()
        c, w, h = dreamed.shape

        dreamed = dreamed.view((w, h, c))
        dreamed = torch.clamp(dreamed, 0.0, 1.0)
        dreamed = dreamed * self.std + self.mean
        dreamed = dreamed.view((c, w, h))

        del self.image_var, image_pre

        return dreamed

    def deep_dream(self, image, n, top, scale_factor):
        if n > 0:
            b, c, w, h = image.shape
            # print(w,h)
            image = TF.to_pil_image(image.squeeze().cpu())
            image_down = TF.resize(image, (int(w * scale_factor), int(h * scale_factor)), Image.ANTIALIAS)
            image_down = image_down.filter(ImageFilter.GaussianBlur(0.5))

            image_down = TF.to_tensor(image_down).unsqueeze(0)
            from_down = self.deep_dream(image_down, n - 1, top, scale_factor)

            from_down = TF.to_pil_image(from_down.squeeze().cpu())
            from_down = TF.resize(from_down, (w, h), Image.ANTIALIAS)

            image = ImageChops.blend(from_down, image, 0.6)

            image = TF.to_tensor(image).to(self.device)
        n = n - 1

        return self.step(image, steps=8, save=top == n + 1)

    def __call__(self, inputs, layer, n_repeat=6, scale_factor=0.7):
        self.layer = layer
        self.handle = self.register_hooks()

        dd = self.deep_dream(inputs, self.params['octaves']['value'],
                             top=self.params['octaves']['value'],
                             scale_factor=self.params['scale']['value'])
        self.handle.remove()

        return dd.unsqueeze(0)

    @property
    def name(self):
        return 'deep dream'

    def init_params(self):
        return {'lr' : {
                 'type': 'slider',
                 'min': 0.001,
                 'max': 1,
                 'value': 0.1,
                 'step': 0.001,
                 'params': {}
                 },
                'octaves' : {
                 'type': 'slider',
                 'min': 1,
                 'max': 10,
                 'value': 4,
                 'step': 1,
                 'params': {}
                 },
              'scale' : {
                 'type': 'slider',
                 'min': 0.1,
                 'max': 1,
                 'value': 0.7,
                 'step': 0.1,
                 'params': {}
                 }
        }
