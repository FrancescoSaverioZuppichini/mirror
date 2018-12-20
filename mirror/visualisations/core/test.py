import torch

from mirror.visualisations.core import *

from PIL import Image

from torchvision.models import resnet18, alexnet
from torchvision.transforms import ToTensor, Resize, Compose

import matplotlib.pyplot as plt

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# create a model
model = alexnet(pretrained=True)

cat = Image.open("/home/francesco/Documents/mirror/cat.jpg")
# resize the image and make it a tensor
input = Compose([Resize((224,224)), ToTensor()])(cat)
# add 1 dim for batch
input = input.unsqueeze(0)
# call mirror with the input and the model
layers = list(model.modules())
layer = layers[1][2]
print(layer)

def imshow(tensor):
    tensor = tensor.squeeze()
    print(tensor.shape)
    if len(tensor.shape) > 2: tensor = tensor.permute(1, 2, 0)
    img = tensor.cpu().numpy()
    plt.imshow(img, cmap='gray')
    plt.show()


vis = DeepDream(model.to(device), device)
img = vis(input.to(device), layer, octaves=4)

print(img.shape)
with torch.no_grad():
    imshow(img[0])