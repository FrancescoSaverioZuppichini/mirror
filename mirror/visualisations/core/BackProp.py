import torch

from mirror.visualisations.core.Base import Base

from torch.nn import ReLU
from torch.autograd import Variable

from torchvision.transforms import *
from mirror.visualisations.Visualisation import Visualisation

class BackProp(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gradients = None
        self.handles = []
        self.stored_grad = False
        self.transformMean = [0.485, 0.456, 0.406]
        self.transformStd = [0.229, 0.224, 0.225]

        self.transform_preprocess = transforms.Compose([
            transforms.Normalize(
                mean=self.transformMean,
                std=self.transformStd
            )
        ])

        self.mean = torch.Tensor(self.transformMean).to(self.device)
        self.std = torch.Tensor(self.transformStd).to(self.device)

    def forward_hook(self, layer, filter):
        def maxime_layer(module, inputs, outputs):
            print(module)
            self.optimizer.zero_grad()
            neuron = outputs[0, filter]
            loss = -torch.norm(neuron)
            print(loss.item())
            loss.backward()
            self.optimizer.step()

        self.handles.append(layer.register_forward_hook(maxime_layer))

    def __call__(self, input_image, layer, filter=0, guide=False, target_class=None):
        self.clean()
        out_image = torch.empty(input_image.size()).uniform_(to=0.8)
        out_image = self.transform_preprocess(out_image.squeeze())

        self.forward_hook(layer, filter)

        out_image = Variable(out_image.to(self.device), requires_grad=True)

        self.optimizer = torch.optim.Adam([out_image])

        for _ in range(50):
            _ = self.module(out_image.unsqueeze(0))

        # with torch.no_grad():
        #     pass
        #     image = torch.from_numpy(recreate_image(out_image.grad.data.cpu()))
        # c, w, h = out_image.shape
        #
        # out_image = out_image.view((w, h, c))
        #
        # out_image = out_image * self.std + self.mean
        # out_image = out_image.view((c, w, h))

        self.clean()
        # image = out_image.grad.data.cpu()

        # return image.unsqueeze(0)

