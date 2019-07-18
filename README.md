

```python
%load_ext autoreload
%autoreload 2

```

# Mirror
## Pytorch CNN Visualisation Tool

This is a raw beta so expect lots of things to change and improve over time.

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/mirror.gif?raw=true)

### Getting started

To install mirror run

```
pip install git+https://github.com/FrancescoSaverioZuppichini/mirror.git
```

## Getting Started

A basic example


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
dog_and_cat = Image.open("./dog_and_cat.jpg")
# resize the image and make it a tensor
to_input = Compose([Resize((224, 224)), ToTensor()])
# call mirror with the inputs and the model
mirror([to_input(cat), to_input(dog_and_cat)], model, visualisations=[WebBackProp, WebGradCam, WebDeepDream])
```

     * Serving Flask app "mirror.App" (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off


     * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    127.0.0.1 - - [18/Jul/2019 15:48:10] "GET /static/css/main.fd8c6979.chunk.css HTTP/1.1" 200 -
    127.0.0.1 - - [18/Jul/2019 15:48:10] "GET /api/inputs HTTP/1.1" 200 -
    127.0.0.1 - - [18/Jul/2019 15:48:10] "GET /api/model HTTP/1.1" 200 -
    127.0.0.1 - - [18/Jul/2019 15:48:10] "GET /api/visualisation HTTP/1.1" 200 -
    127.0.0.1 - - [18/Jul/2019 15:48:10] "GET /api/model/image/5875341241359/5875341241359/1647183868692822170/%3Cbuilt-in%20function%20id%3E/0 HTTP/1.1" 200 -
    127.0.0.1 - - [18/Jul/2019 15:48:10] "GET /api/model/image/5875341241359/5875341241359/1647205858925377690/%3Cbuilt-in%20function%20id%3E/1 HTTP/1.1" 200 -


It will automatic open a new tab in your browser

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/mirror.png?raw=true)

On the left you can see your model tree structure, by clicking on one layer all his children are showed. On the right there are the visualisation settings. You can select your input by clicking on the bottom tab.

![alt](https://raw.githubusercontent.com/FrancescoSaverioZuppichini/mirror/master/resources/inputs.png)


## Available Visualisations
### Weights
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/weights.png?raw=true)
### Deep Dream
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/deepdream.png?raw=true)
### Back Prop / Guide Back Prop
By clicking on the radio button 'guide', all the relus negative output will be set to zero producing a nicer looking image
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/backprop.png?raw=true)
## Grad Cam / Guide Grad Cam
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/grad_cam.png?raw=true)


## Create a Visualisation
To create a visualisation you first have to subclass the `Visualisation` class by just define the `__call__` method to return an image and additional informations. The following example creates a custom visualisation that just repeat the input. We first define a custom Visualisation


```python
from mirror.visualisations import Visualisation

class RepeatInput(Visualisation):

    def __call__(self, inputs, layer, repeat=1):
        return inputs.repeat(repeat, 1, 1, 1), None

```

This class just repeat the input for `repeat` times. Now we have to create a `WebInterface` to make this class communicate with the application. Be careful to the next step.


```python
from mirror.visualisations import WebInterface

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

```

In the `__init__` method we instantiate our custom visualisation by passing `self.module` and `self.device`. Then, **we decleare each argument to the visualisation as a field of this class**. So, since `RepeatInput` takes as argument `repeat` we create a field `repeat` in `WebRepeatInput`. Then, we defined the name by overriding the property `name`. Finally, we override the property `params` to create the corresponding UI. `params` must return a dictionary where **each key are the names of the visualisations arguments**, in our case `repeat`, and the value is a dictionary where there is a key `value` mapped to the class field. This will allows `mirror` to dynamically update your fields based on the UI. In this example, we create a slider and it looks like

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/repeat_slider.jpg?raw=true)
The final result is 

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/repeat_example.jpg?raw=true)


![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/dummy.jpg?raw=true)


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
- [x] Support multiple models
- Add all visualisation present here https://github.com/utkuozbulak/pytorch-cnn-visualizations
    * [x] [Gradient visualization with vanilla backpropagation](#gradient-visualization)
    * [x] [Gradient visualization with guided backpropagation](#gradient-visualization) [1]
    * [x] [Gradient visualization with saliency maps](#gradient-visualization) [4]
    * [x] [CNN filter visualization](#convolutional-neural-network-filter-visualization) [9]
    * [x] [Deep dream](#deep-dream) [10]
    * [ ] [Class specific image generation](#class-specific-image-generation) [4]
    * [x] [Grad Cam](https://arxiv.org/abs/1610.02391)

- [ ] Add a `output_transformation` params for each visualisation to allow better customisation 
- [ ] Add a `input_transformation` params for each visualisation to allow better customisation 


```python

```
