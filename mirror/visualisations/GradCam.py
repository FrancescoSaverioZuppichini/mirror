from .Visualisation import Visualisation

import torch
from torch.nn import ReLU
from .Visualisation import Visualisation

import torch.nn.functional as F
from .misc_functions import (get_params,
                             convert_to_grayscale,
                             save_gradient_images,
                             get_positive_negative_saliency)

from torch.autograd import Variable
from torchvision import transforms
import numpy as np
import cv2

class GradCam(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gradients = None
        self.handles = []
        self.target_class = None

    @property
    def name(self):
        return 'grad cam'


    def register_hooks(self, layer):
        [h.remove() for h in self.handles]

        def store_grad(grad):
            self.gradients = grad

        self.handles = []

        def forward_hook(module, input, outputs):
            if module == self.layer:
                self.outputs = outputs
                self.handles.append(outputs.register_hook(store_grad))

        self.handles.append(layer.register_forward_hook(forward_hook))

        def guide_relu(module, grad_in, grad_out):
            return (torch.clamp(grad_in[0], min=0.0),)

        for module in self.module.modules():
            if isinstance(module, ReLU):
                self.handles.append(module.register_backward_hook(guide_relu))

    def __call__(self, input_image, layer):
        self.layer = layer
        input_image = Variable(input_image, requires_grad=True).to(self.device)

        self.register_hooks(layer)

        predictions = self.module(input_image)

        if self.target_class is None: _, self.target_class = torch.max(predictions, dim=1)

        print('target class', self.target_class)

        one_hot_output = torch.zeros(predictions.size()).to(self.device)
        one_hot_output[0][self.target_class] = 1
        # compute gradient w.r.t. to the target
        self.module.zero_grad()
        predictions.backward(gradient=one_hot_output, retain_graph=True)

        with torch.no_grad():
            avg_channel_grad = self.gradients.data.squeeze().mean(1).mean(1)
            outputs = self.outputs.squeeze()

            cam = torch.ones(outputs.shape[1:]).to(self.device)

            for i, w in enumerate(avg_channel_grad):
                cam += w * outputs[i, :, :]

            b, c, w, h = input_image.shape

            cam = cam.cpu().numpy()
            cam = cv2.resize(cam, (h, w))
            cam = np.maximum(cam, 0)
            cam = (cam - np.min(cam)) / (np.max(cam) - np.min(cam))  # Normalize between 0-1
            cam = np.uint8(cam * 255)  # Scale between 0-255 to visualize

            activation_heatmap = cv2.applyColorMap(cam, cv2.COLORMAP_JET)

            original_image = input_image.squeeze().permute(1,2,0).cpu().numpy()

            img_with_heatmap = np.float32(activation_heatmap) + (original_image * 255)
            img_with_heatmap = img_with_heatmap / np.max(img_with_heatmap)

            img = torch.from_numpy(img_with_heatmap).permute(2,0,1)

        [h.remove() for h in self.handles]

        return img.unsqueeze(0)
