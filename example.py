from mirror import mirror
from mirror.visualisations import *
from PIL import Image
from torchvision.models import resnet101, resnet18, vgg16, alexnet
from torchvision.transforms import ToTensor, Resize, Compose

# create a model
model = alexnet(pretrained=True)
# get an image
cat = Image.open("./cat.jpg")
# resize the image and make it a tensor
input = Compose([Resize((224,224)), ToTensor()])(cat)
# add 1 dim for batch
input = input.unsqueeze(0)
# call mirror with the input and the model
mirror(input, model, visualisations=[DeepDreamVis, BackPropVis, GradCamVis])