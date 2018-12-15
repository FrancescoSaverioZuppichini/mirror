import torch
from torch.nn import ReLU
from .Visualisation import Visualisation

from .misc_functions import (get_params,
                            convert_to_grayscale,
                            save_gradient_images,
                            get_positive_negative_saliency)

from torch.autograd import Variable
from torchvision import transforms

class Backprop(Visualisation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gradients = None
        # Put model in evaluation mode
        self.model = self.module #TODO
        self.model.eval()

        self.transformMean = [0.485, 0.456, 0.406]
        self.transformStd = [0.229, 0.224, 0.225]

        self.transform_preprocess = transforms.Compose([
            transforms.Normalize(
                mean=self.transformMean,
                std=self.transformStd
            )
        ])

        self.handles = []
        self.target_class = 56

    @property
    def name(self):
        return 'backprop'

    def register_hooks(self):
        [h.remove() for h in self.handles]

        handles = []

        def store_grad(module, grad_in, grad_out):
            self.gradients = grad_in[0]

        first_layer = self.tracer.operations[0][0]
        handles.append(first_layer.register_backward_hook(store_grad))

        return handles

    def __call__(self, input_image, layer):
        input_image = self.transform_preprocess(input_image[0]).unsqueeze(0)
        input_image = Variable(input_image, requires_grad=True).to(self.device)

        predictions = self.model(input_image)

        self.handles = self.register_hooks()

        one_hot_output = torch.zeros(predictions.size()).to(self.device)
        one_hot_output[0][self.target_class] = 1

        predictions.backward(gradient=one_hot_output)

        gradients_as_arr = self.gradients.data.cpu().numpy()[0]

        image = convert_to_grayscale(gradients_as_arr)

        image = torch.from_numpy(image).to(self.device)

        [h.remove() for h in self.handles]

        self.model.zero_grad()

        return image.unsqueeze(0)

class GuidedBackprop(Backprop):

    @property
    def name(self):
        return 'guided backprop'

    def register_hooks(self):
        handles = super().register_hooks()

        def guide_relu(module, grad_in, grad_out):
            return (torch.clamp(grad_in[0], min=0.0),)

        for module in self.model.modules():
            if isinstance(module, ReLU):
                handles.append(module.register_backward_hook(guide_relu))

        return handles
