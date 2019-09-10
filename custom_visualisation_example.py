from mirror import mirror
from PIL import Image
from torchvision.models import vgg16
from torchvision.transforms import ToTensor, Resize, Compose
from mirror.visualisations.core import Visualisation
from mirror.visualisations.web import WebInterface
from functools import partial

class RepeatInput(Visualisation):

    def __call__(self, inputs, layer, repeat=1):
        return inputs.repeat(repeat, 1, 1, 1), None

params = {'repeat' : {
                     'type' : 'slider',
                     'min' : 1,
                     'max' : 100,
                     'value' : 2,
                     'step': 1,
                     'params': {}
                 }
        }

visualisation = partial(WebInterface.from_visualisation, RepeatInput, params=params, name='Visualisation')
# create a model
model = vgg16(pretrained=True)
# open some images
cat = Image.open("./cat.jpg")
dog_and_cat = Image.open("./dog_and_cat.jpg")
# resize the image and make it a tensor
to_input = Compose([Resize((224, 224)), ToTensor()])
# call mirror with the inputs and the model
mirror([to_input(cat), to_input(dog_and_cat)], model,
       visualisations=[visualisation])
