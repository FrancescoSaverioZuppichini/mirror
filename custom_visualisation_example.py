from mirror.visualisations.WebInterface import WebInterface
from mirror.visualisations import Visualisation

class RepeatInput(Visualisation):

    def __call__(self, inputs, layer, repeat=1):
        return inputs.repeat(repeat, 1, 1, 1), None

class WebRepeatInput(WebInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visualisation = RepeatInput(self.module, self.device) # create your visualisation
        self.repeat = 1 # define your parameters

    @property
    def name(self):
        return 'Repeat'

    @property
    def params(self):
        # maps the parameters to the UI
        return {'repeat' : {
                     'type' : 'slider',
                     'min' : 1,
                     'max' : 100,
                     'value' : self.repeat,
                     'step': 1,
                     'params': {}
                 }
        }



from mirror import mirror
from mirror.visualisations import *
from PIL import Image
from torchvision.models import resnet101, resnet18, vgg16, alexnet
from torchvision.transforms import ToTensor, Resize, Compose

# create a model
model = vgg16(pretrained=True)
# open some images
cat = Image.open("./cat.jpg")
dog_and_cat = Image.open("./dog_and_cat.jpg")
# resize the image and make it a tensor
to_input = Compose([Resize((224, 224)), ToTensor()])
# call mirror with the inputs and the model
mirror([to_input(cat), to_input(dog_and_cat)], model, visualisations=[WebRepeatInput])
