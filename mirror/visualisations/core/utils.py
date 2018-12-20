import torch

from torchvision.transforms import Compose, Normalize

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

image_net_mean = torch.Tensor([0.485, 0.456, 0.406])
image_net_std = torch.Tensor([0.229, 0.224, 0.225])

class NormalizeInverse(Normalize):
    """
    Undoes the normalization and returns the reconstructed images in the input domain.
    """
    def __init__(self, mean, std):
        mean = torch.Tensor(mean)
        std = torch.Tensor(std)
        std_inv = 1 / (std + 1e-7)
        mean_inv = -mean * std_inv
        super().__init__(mean=mean_inv, std=std_inv)

    def __call__(self, tensor):
        return super().__call__(tensor.clone())

image_net_preprocessing = Compose([
    Normalize(
        mean=image_net_mean,
        std=image_net_std
    )
])

image_net_postprocessing = Compose([
    NormalizeInverse(
        mean=image_net_mean,
        std=image_net_std)
])

