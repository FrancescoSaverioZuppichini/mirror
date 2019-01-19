# Mirror
## Pytorch CNN Visualisation Tool

This is a raw beta so expect lots of things to change and improve over time.

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/mirror.gif?raw=true)

### Getting started

To install mirror run

```
pip install git+https://github.com/FrancescoSaverioZuppichini/mirror.git
```

Basic example:

```python
from mirror import mirror
from mirror.visualisations import *
from PIL import Image
from torchvision.models import resnet101, resnet18, vgg16, alexnet
from torchvision.transforms import ToTensor, Resize, Compose

# create a model
model = vgg16(pretrained=True)
# open some images
cat = Image.open("./cat.jpg")
dog_and_cat  = Image.open("./dog_and_cat.jpg")
# resize the image and make it a tensor
to_input = Compose([Resize((224,224)), ToTensor()])
# call mirror with the inputs and the model
mirror([to_input(cat), to_input(dog_and_cat)], model, visualisations=[DeepDreamVis, BackPropVis, GradCamVis]
```

It will automatic open a new tab in your browser

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/develop/resources/mirror.png?raw=true)

On the left you can see your model tree structure, by clicking on one layer all his children are showed. On the right there are the visualisation settings. You can select your input by clicking on the bottom tab.

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/develop/resources/inputs.png?raw=true)

### Available Visualisations
#### Weights
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/develop/resources/weights.png?raw=true)
### Deep Dream
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/develop/resources/deepdream.png?raw=true)
#### Back Prop / Guide Back Prop
By clicking on the radio button 'guide', all the relus negative output will be set to zero producing a nicer looking image
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/develop/resources/backprop.png?raw=true)
### Grad Cam / Guide Grad Cam
- [ ] Add text field for class
- [ ] 
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/develop/resources/grad_cam.png?raw=true)
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

The `init_params`  function returns a dictionary of options that will be showed on the right drawer of the application. For now only `slider` , `textfield` and `radio` are supported. For example, the `GradCamVis` `__init_params__` looks like:

```python
class GradCamVis(Visualisation):
    ...
    def init_params(self):
        return {'guide': {'type': 'radio',
                          'value': False
                          },
                'class': {
                    'type': 'textfield',
                    'label': 'id',
                    'value': None
                          }
                }
```

## Change the front-end
All the front-end is developed usin [React](https://reactjs.org/) and [Material-UI](https://material-ui.com/), two very known frameworks, making easier for anybody to contribuite.

You can customise the front-end by changing the source code in `mirror/client`. After that, you need to build the react app and move the file to the server static folder.

**I was not able to serve the static file directly from the /mirror/client/build folder** if you know how to do it any pull request is welcome :)

```
cd ./mirror/mirror/client // assuming the root folder is called mirror
npm run build
```
Then you need to move the fiels from the `mirror/mirror/client/build` folder to `mirror/mirror`. You can remove all the files in `mirror/mirro/static`
```
mv ./build/static ../ && cp ./build/* ../static/
```

### TODO
- [x] Cache reused layer 
- [x] Make a generic abstraction of a visualisation in order to add more features  
- [x] Add dropdown as parameter
- [x] Add text field
- [x] Support multiple inputs
- [ ] Support multiple models
- Add all visualisation present here https://github.com/utkuozbulak/pytorch-cnn-visualizations
    * [x] [Gradient visualization with vanilla backpropagation](#gradient-visualization)
    * [x] [Gradient visualization with guided backpropagation](#gradient-visualization) [1]
    * [ ] [Gradient visualization with saliency maps](#gradient-visualization) [4]
    * [ ] [Gradient-weighted [3] class activation mapping](#gradient-visualization) [2] 
    * [ ] [Guided, gradient-weighted class activation mapping](#gradient-visualization) [3]
    * [ ] [Smooth grad](#smooth-grad) [8]
    * [x] [CNN filter visualization](#convolutional-neural-network-filter-visualization) [9]
    * [ ] [Inverted image representations](#inverted-image-representations) [5]
    * [x] [Deep dream](#deep-dream) [10]
    * [ ] [Class specific image generation](#class-specific-image-generation) [4]
    * [x] [Grad Cam](https://arxiv.org/abs/1610.02391)
- [] Add a `output_transformation` params for each visualisation to allow better customisation 
- [] Add a `input_transformation` params for each visualisation to allow better customisation 