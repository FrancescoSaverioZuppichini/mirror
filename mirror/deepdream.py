#!/usr/bin/env python
# coding: utf-8

# In[16]:


import os
import cv2

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import SGD
from torchvision import models
from torch.autograd import Variable
import scipy.ndimage as nd
import numpy as np

from torchvision import transforms
import torchvision.transforms.functional as TF
from PIL import Image, ImageFilter, ImageChops

# In[26]:


# IMG_PATH = './pytorch-cnn-visualizations/input_images/dd_tree.jpg'
IMG_PATH = './the_starry_night-wallpaper-1920x1200.jpg'
# IMG_PATH = './the_starry_night-wallpaper-2560x1600.jpg'
# IMG_PATH = './sky-dd.jpeg'

# In[27]:


pil_img = Image.open(IMG_PATH)

# In[28]:


img_transform = transforms.Compose([
    # transforms.Resize((224, 224)),
    transforms.ToTensor(),
    #     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# In[5]:


# x = img_transform(pil_img).cuda()

# In[6]:


model = models.vgg16(pretrained=True).cuda()

import time
# In[37]:


class DeepDream:
    def __init__(self, module, layer):
        self.module = module
        self.trace = (None, None, None)
        self.layer = layer

        self.transformMean = [0.485, 0.456, 0.406]
        self.transformStd = [0.229, 0.224, 0.225]

        # self.transform_preprocess = transforms.Normalize(
        #     mean=self.transformMean,
        #     std=self.transformStd
        # )

        self.transform_preprocess = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=self.transformMean,
                std=self.transformStd
            )
        ])

        self.mean = torch.Tensor(self.transformStd).cuda()
        self.std = torch.Tensor(self.transformMean).cuda()
        self.lr = 0.2

        self.out = None
        self.register_hooks()

    def register_hooks(self):
        def hook(module, input, output):
            if module == self.layer:
                loss = output.norm()
                loss.backward()

                grad = self.image_var.grad.data
                self.image_var.data = self.image_var.data + (self.lr * grad)

                raise Exception('Layer found!')

        self.layer.register_forward_hook(hook)

    def toImage(self, input):
        return input * self.std + self.mean

    def step(self, image, steps=5, save=False):

        self.module.zero_grad()

        image_pre = self.transform_preprocess(image.squeeze().cpu()).cuda().unsqueeze(0)
        self.image_var = Variable(image_pre, requires_grad=True).cuda()

        for i in range(steps):
            try:
                self.module(self.image_var)
            except:
                pass

            # if save:
            #     dreamed = self.image_var.data.squeeze()
            #     c, w, h = dreamed.shape
            #
            #     dreamed = dreamed.view((w, h, c))
            #     dreamed = torch.clamp(dreamed, 0.0, 1.0)
            #     dreamed = dreamed * self.std + self.mean
            #     dreamed = dreamed.view((c, w, h))
            #     dreamed_pil = TF.to_pil_image(dreamed.squeeze().cpu())
            #
            #     dreamed_pil.save('./dream-' + str(i) + ".jpg", "JPEG")

        dreamed = self.image_var.data.squeeze()
        c, w, h = dreamed.shape

        dreamed = dreamed.view((w, h, c))
        dreamed = torch.clamp(dreamed, 0.0, 1.0)
        dreamed = dreamed * self.std + self.mean
        dreamed = dreamed.view((c, w, h))

        del self.image_var,  image_pre

        return dreamed


    def deep_dream(self, image, n, top, scale_factor):
        if n > 0:
            b, c, w, h = image.shape
            print(w,h)
            image = TF.to_pil_image(image.squeeze().cpu())
            image_down = TF.resize(image, (int(w *scale_factor), int(h * scale_factor)), Image.ANTIALIAS)
            image_down = image_down.filter(ImageFilter.GaussianBlur(0.5))

            image_down = TF.to_tensor(image_down).unsqueeze(0)
            from_down = self.deep_dream(image_down, n - 1, top, scale_factor)

            from_down = TF.to_pil_image(from_down.squeeze().cpu())
            from_down = TF.resize(from_down, (w, h), Image.ANTIALIAS)

            # from_down = torch.nn.functional.interpolate(from_down, size=(w, h))

            # down, image = TF.to_pil_image(from_down.cpu().squeeze()), TF.to_pil_image(image.cpu().squeeze())

            image = ImageChops.blend(from_down, image, 0.6)

            image = TF.to_tensor(image).cuda()
        n = n - 1

        return self.step(image, steps=3, save=top == n + 1)


    def __call__(self, image, n_repeat=6, scale_factor=0.7):
        return self.deep_dream(image, n_repeat, top=n_repeat, scale_factor=scale_factor)



# In[9]:


print(model)
start = time.time()
dd = DeepDream(model, model.features[28])
dreamed = dd(img_transform(pil_img).unsqueeze(0))
end = time.time()
print('{:.4f}'.format(end - start))


# In[35]:


def plot_tensor(tensor):
    tensor = torch.nn.functional.interpolate(tensor, scale_factor=0.7)
    img = transforms.ToPILImage()(tensor.squeeze().cpu())

    return img

img = plot_tensor(dreamed)
# img.show()
img.save('dream' + ".jpg", "JPEG")

# In[36]:

# In[ ]:



