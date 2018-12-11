# Mirror
## Pytorch cnn visualisation

This is a raw beta so expect lots of things to change and improve over time.

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/develop/resources/mirror.gif?raw=true)

### Getting started

To install mirror run

```
pip install git+https://github.com/FrancescoSaverioZuppichini/mirror.git
```

Basic example:

```python
from mirror import mirror
from mirror.visualisations import DeepDream

from PIL import Image

from torchvision.models import resnet101, resnet18, vgg16
from torchvision.transforms import ToTensor, Resize, Compose

# create a model
model = vgg16(pretrained=True)

cat = Image.open("./cat.jpg")
# resize the image and make it a tensor
input = Compose([Resize((224,224)), ToTensor()])(cat)
# add 1 dim for batch 
input = input.unsqueeze(0)
# call mirror with the input and the model 
mirror(input, model, visualisations=[DeepDream])
```

It will automatic open a new tab in your browser

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/develop/resources/mirror.jpg?raw=true)

### Create a Visualisation

You can find an example below

```python
from mirror.visualisations.Visualisation import Visualisation

class DummyVisualisation(Visualisation):

    def __call__(self, inputs, layer):
        return inputs.repeat(self.params['repeat']['value'],1, 1, 1)

    @property
    def name(self):
        return 'dummy'

    def init_params(self):
        return {'repeat' : {
                 'type' : 'slider',
                 'min' : 1,
                 'max' : 100,
                 'value' : 3,
                 'step': 1,
                 'params': {}
                 }}

```

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/develop/resources/dummy.jpg?raw=true)

The `__call__` function is called each time you click a layer or change a value in the options on the right.

The `init_params` parameters function returns a dictionary of options that will be showed on the rigth drawer of the application. For know only `slider` and `radio` is supported

### TODO
- [x] Cache reused layer 
- [x] Make a generic abstraction of a visualisation in order to add more features  
- [ ] Add more options for the parameters (dropdown, text)
- [ ] Support multiple inputs
- [ ] Support multiple models
- Add all visualisation present here https://github.com/utkuozbulak/pytorch-cnn-visualizations
    * [ ] [Gradient visualization with vanilla backpropagation](#gradient-visualization)
    * [ ] [Gradient visualization with guided backpropagation](#gradient-visualization) [1]
    * [ ] [Gradient visualization with saliency maps](#gradient-visualization) [4]
    * [ ] [Gradient-weighted [3] class activation mapping](#gradient-visualization) [2] 
    * [ ] [Guided, gradient-weighted class activation mapping](#gradient-visualization) [3]
    * [ ] [Smooth grad](#smooth-grad) [8]
    * [x] [CNN filter visualization](#convolutional-neural-network-filter-visualization) [9]
    * [ ] [Inverted image representations](#inverted-image-representations) [5]
    * [x] [Deep dream](#deep-dream) [10]
    * [ ] [Class specific image generation](#class-specific-image-generation) [4]
