from mirror import mirror
from mirror.visualisations import *
from PIL import Image
from torchvision.models import resnet101, resnet18, vgg16, alexnet
from torchvision.transforms import ToTensor, Resize, Compose
# from DummyVisualisation import DummyVisualisation
# create a model
model = vgg16(pretrained=True)
# open some images
cat = Image.open("./cat.jpg")
dog_and_cat = Image.open("./dog_and_cat.jpg")
# resize the image and make it a tensor
to_input = Compose([Resize((224, 224)), ToTensor()])

# call mirror with the inputs and the model
mirror([to_input(cat), to_input(dog_and_cat)], model, visualisations=[WebWeights, WebBackProp, WebGradCam, WebDeepDream])
