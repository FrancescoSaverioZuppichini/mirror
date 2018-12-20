import cv2
import numpy as np
import torch

from torch.nn import ReLU
from torch.autograd import Variable
from mirror.visualisations.core.Base import Base

class GradCam(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handles = []
        self.gradients = None
        self.conv_outputs = None

    def store_outputs_and_grad(self, layer):
        def store_grad(grad):
            print('GradCam')
            self.gradients = grad

        def store_outputs(module, input, outputs):
            if module == layer:
                self.conv_outputs = outputs
                self.handles.append(outputs.register_hook(store_grad))

        self.handles.append(layer.register_forward_hook(store_outputs))

    def guide(self, module):
        def guide_relu(module, grad_in, grad_out):
            return (torch.clamp(grad_in[0], min=0.0),)

        for module in module.modules():
            if isinstance(module, ReLU):
                self.handles.append(module.register_backward_hook(guide_relu))

    def clean(self):
        [h.remove() for h in self.handles]

    def __call__(self, input_image, layer, guide=False, target_class=None):
        self.clean()
        self.store_outputs_and_grad(layer)
        if guide: self.guide(self.module)

        input_var = Variable(input_image, requires_grad=True).to(self.device)
        predictions = self.module(input_var)

        if target_class == None: _, target_class = torch.max(predictions, dim=1)

        print(target_class)

        target = torch.zeros(predictions.size()).to(self.device)
        target[0][target_class] = 1

        self.module.zero_grad()
        predictions.backward(gradient=target, retain_graph=True)

        with torch.no_grad():
            avg_channel_grad = self.gradients.data.squeeze().mean(1).mean(1)
            outputs = self.conv_outputs.squeeze()

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

            original_image = input_image.squeeze().permute(1, 2, 0).cpu().numpy()

            img_with_heatmap = np.float32(activation_heatmap) + (original_image * 255)
            img_with_heatmap = img_with_heatmap / np.max(img_with_heatmap)

            img = torch.from_numpy(img_with_heatmap).permute(2, 0, 1)
        self.clean()

        return img.unsqueeze(0)


