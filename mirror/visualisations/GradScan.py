from .Visualisation import Visualisation

import torch
from torch.nn import ReLU
from .Visualisation import Visualisation

from .misc_functions import (get_params,
                             convert_to_grayscale,
                             save_gradient_images,
                             get_positive_negative_saliency)

from torch.autograd import Variable
from torchvision import transforms
import numpy as np
import cv2

class GradScan(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gradients = None
        self.handles = []
        self.target_class = None

    @property
    def name(self):
        return 'grad scan'


    def register_hooks(self, layer):
        def store_grad(grad):
            print('************')
            self.gradients = grad
        handles = []

        def forward_hook(module, input, outputs):
            if module == self.layer:
                self.outputs = outputs
                outputs.register_hook(store_grad)

        handles.append(layer.register_forward_hook(forward_hook))
        #
        def guide_relu(module, grad_in, grad_out):
            return (torch.clamp(grad_in[0], min=0.0),)

        for module in self.module.modules():
            if isinstance(module, ReLU):
                handles.append(module.register_backward_hook(guide_relu))

        return handles


    def __call__(self, input_image, layer):
        self.layer = layer
        input_image = Variable(input_image, requires_grad=True).to(self.device)

        self.register_hooks(layer)
        # predictions = self.scan(input_image)
        predictions = self.module(input_image)

        if self.target_class is None:
            _, self.target_class = torch.max(predictions, dim=1)
        print('target class', self.target_class)
        one_hot_output = torch.zeros(predictions.size()).to(self.device)
        one_hot_output[0][self.target_class] = 1

        predictions.backward(gradient=one_hot_output, retain_graph=True)

        with torch.no_grad():
            gradients_np = self.gradients.data.cpu().numpy()[0]
            # Get convolution outputs
            outputs_np = self.outputs.detach().cpu().numpy()[0]
            # Get weights from gradients
            weights = np.mean(gradients_np, axis=(1, 2))  # Take averages for each gradient
            # Create empty numpy array for cam
            cam = np.ones(outputs_np.shape[1:], dtype=np.float32)
            # Multiply each weight with its conv output and then, sum
            for i, w in enumerate(weights):
                cam += w * outputs_np[i, :, :]
            cam = cv2.resize(cam, (224, 224))
            cam = np.maximum(cam, 0)
            cam = (cam - np.min(cam)) / (np.max(cam) - np.min(cam))  # Normalize between 0-1
            cam = np.uint8(cam * 255)  # Scale between 0-255 to visualize

            activation_heatmap = cv2.applyColorMap(cam, cv2.COLORMAP_HSV)

            original_image = input_image.squeeze().permute(1,2,0).cpu().numpy()

            img_with_heatmap = np.float32(activation_heatmap) + original_image
            img_with_heatmap = img_with_heatmap / np.max(img_with_heatmap)

        # img = img.permute(2,0,1)

            img = torch.from_numpy(img_with_heatmap).permute(2,0,1)
            print(img.shape)
        [h.remove() for h in self.handles]

        return img.unsqueeze(0)

    def init_params(self):
        return {'lr': {
            'type': 'menu',
            'items' : ['sgd', 'adam'],
            'value' : 'sgd'
            }
        }