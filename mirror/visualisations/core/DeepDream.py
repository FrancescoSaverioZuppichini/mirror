import torch
import torchvision.transforms.functional as TF

from torch.autograd import Variable
from torchvision import transforms

from PIL import Image, ImageFilter, ImageChops
from .Base import Base

class DeepDream(Base):
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

        self.optimizer = torch.optim.Adam([self.image_var], lr=self.lr)

        for i in range(steps):
            try:
                self.module(self.image_var)
            except:
                pass

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

    def __call__(self, inputs, layer, octaves=6, scale_factor=0.7, lr=0.1):
        self.layer, self.lr = layer, lr
        self.handle = self.register_hooks()
        self.module.zero_grad()
        dd = self.deep_dream(inputs, octaves,
                             top=octaves,
                             scale_factor=scale_factor)
        self.handle.remove()

        return dd.unsqueeze(0)
