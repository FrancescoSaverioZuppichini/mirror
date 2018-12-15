import torch

from mirror import mirror
from mirror.visualisations.Filter import Filter

from PIL import Image

from torchvision.models import resnet101, resnet18, vgg16, alexnet
from torchvision.transforms import ToTensor, Resize, Compose

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# create a model
model = resnet18(pretrained=True)

cat = Image.open("/home/francesco/Documents/mirror/cat.jpg")
# resize the image and make it a tensor
input = Compose([Resize((224,224)), ToTensor()])(cat)
# add 1 dim for batch
input = input.unsqueeze(0)
# call mirror with the input and the model
layers = list(model.modules())
layer = layers[1]
print(layer)

vis = Filter(model.to(device), None, device=device)

vis(input, layer)