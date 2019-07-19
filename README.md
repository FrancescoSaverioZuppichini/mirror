
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
from mirror.visualisations.web import *
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

It will automatic open a new tab in your browser

![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/mirror.png?raw=true)

On the left you can see your model tree structure, by clicking on one layer all his children are showed. On the right there are the visualisation settings. You can select your input by clicking on the bottom tab.

![alt](https://raw.githubusercontent.com/FrancescoSaverioZuppichini/mirror/master/resources/inputs.png)


## Available Visualisations
All visualisation available for the web app are inside `.mirror.visualisations.web`.
### Weights
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/weights.png?raw=true)
### Deep Dream
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/deepdream.png?raw=true)
### Back Prop / Guide Back Prop
By clicking on the radio button 'guide', all the relus negative output will be set to zero producing a nicer looking image
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/backprop.png?raw=true)
## Grad Cam / Guide Grad Cam
![alt](https://github.com/FrancescoSaverioZuppichini/mirror/blob/master/resources/grad_cam.png?raw=true)

### Using with Tensors
If you want, you can use the vanilla version of each visualisation by importing them from  `.mirror.visualisation.core`. 


```python
from mirror.visualisations.core import GradCam

# create a model
model = vgg16(pretrained=True)
# open some images
cat = Image.open("./cat.jpg")
dog_and_cat = Image.open("./dog_and_cat.jpg")
# resize the image and make it a tensor
to_input = Compose([Resize((224, 224)), ToTensor()])

cam = GradCam(model, device='cpu')
cam(to_input(cat).unsqueeze(0), None) # will return the output image and some additional information
```




    (tensor([[[[0.4851, 0.4911, 0.4950,  ..., 0.4592, 0.4612, 0.4612],
               [0.4831, 0.4911, 0.4970,  ..., 0.4632, 0.4652, 0.4652],
               [0.4831, 0.4891, 0.4950,  ..., 0.4692, 0.4692, 0.4692],
               ...,
               [0.3738, 0.3797, 0.3718,  ..., 0.4791, 0.4791, 0.4771],
               [0.3738, 0.3777, 0.3738,  ..., 0.4851, 0.4851, 0.4851],
               [0.3718, 0.3718, 0.3718,  ..., 0.4871, 0.4891, 0.4911]],
     
              [[0.9225, 0.9284, 0.9344,  ..., 0.8907, 0.8887, 0.8867],
               [0.9205, 0.9284, 0.9364,  ..., 0.8926, 0.8907, 0.8867],
               [0.9245, 0.9284, 0.9384,  ..., 0.8887, 0.8847, 0.8787],
               ...,
               [0.3678, 0.3718, 0.3658,  ..., 0.9165, 0.9185, 0.9185],
               [0.3698, 0.3738, 0.3698,  ..., 0.9245, 0.9245, 0.9225],
               [0.3638, 0.3678, 0.3678,  ..., 0.9264, 0.9284, 0.9304]],
     
              [[0.8111, 0.8171, 0.8330,  ..., 0.9264, 0.9245, 0.9245],
               [0.8052, 0.8171, 0.8330,  ..., 0.9284, 0.9264, 0.9245],
               [0.8032, 0.8171, 0.8290,  ..., 0.9304, 0.9245, 0.9205],
               ...,
               [0.7455, 0.7515, 0.7455,  ..., 0.8449, 0.8449, 0.8429],
               [0.7515, 0.7575, 0.7515,  ..., 0.8509, 0.8509, 0.8489],
               [0.7475, 0.7515, 0.7515,  ..., 0.8529, 0.8549, 0.8569]]]]),
     {'prediction': tensor([285]),
      'cam': tensor([[0.4018, 0.2273, 0.3181, 0.3394, 0.3576, 0.3860, 0.3549, 0.2843, 0.3375,
               0.3635, 0.3597, 0.4068, 0.3265, 0.3453],
              [0.1224, 0.0331, 0.1392, 0.1965, 0.1660, 0.2145, 0.3302, 0.4260, 0.5503,
               0.4859, 0.2776, 0.3724, 0.3339, 0.3459],
              [0.2829, 0.0903, 0.3179, 0.3343, 0.3149, 0.3856, 0.5954, 0.8654, 1.0000,
               0.9591, 0.5861, 0.4429, 0.3494, 0.3650],
              [0.4101, 0.1648, 0.7469, 0.8419, 0.6816, 0.4950, 0.4598, 0.5734, 0.6599,
               0.6918, 0.4082, 0.3602, 0.4526, 0.3900],
              [0.4446, 0.1970, 0.8610, 0.9558, 0.8703, 0.5969, 0.3578, 0.3639, 0.3836,
               0.2696, 0.2457, 0.0940, 0.2466, 0.2645],
              [0.4661, 0.2916, 0.5460, 0.6298, 0.6865, 0.4947, 0.3344, 0.3180, 0.3113,
               0.2919, 0.2191, 0.0688, 0.1556, 0.2535],
              [0.2896, 0.1955, 0.2195, 0.4146, 0.4831, 0.5808, 0.5027, 0.4044, 0.3637,
               0.4110, 0.4081, 0.2570, 0.1484, 0.2467],
              [0.1489, 0.1317, 0.1994, 0.4677, 0.4953, 0.5647, 0.5311, 0.4122, 0.3317,
               0.3378, 0.4336, 0.3150, 0.2032, 0.2380],
              [0.1098, 0.1077, 0.1492, 0.3742, 0.3192, 0.3921, 0.4096, 0.3779, 0.3289,
               0.3332, 0.3778, 0.2641, 0.1875, 0.1976],
              [0.1065, 0.1065, 0.1437, 0.3091, 0.2134, 0.2284, 0.2599, 0.2399, 0.3141,
               0.3549, 0.3406, 0.2375, 0.1182, 0.1587],
              [0.0900, 0.0759, 0.1104, 0.1690, 0.1489, 0.1046, 0.1206, 0.2289, 0.3569,
               0.4056, 0.3637, 0.2550, 0.0722, 0.1328],
              [0.0634, 0.0381, 0.0820, 0.0876, 0.0807, 0.0729, 0.1159, 0.2247, 0.3249,
               0.4661, 0.4900, 0.3804, 0.0775, 0.1526],
              [0.0019, 0.0000, 0.0034, 0.0394, 0.0688, 0.0706, 0.0744, 0.0738, 0.0743,
               0.2720, 0.2767, 0.2766, 0.1200, 0.1786],
              [0.1545, 0.1182, 0.1631, 0.1559, 0.1374, 0.1143, 0.1377, 0.1393, 0.2544,
               0.3703, 0.3653, 0.4016, 0.2678, 0.3975]])})



## Create a Visualisation
To create a visualisation you first have to subclass the `Visualisation` class by just define the `__call__` method to return an image and additional informations. The following example creates a custom visualisation that just repeat the input. We first define a custom Visualisation


```python
from mirror.visualisations.core import Visualisation

class RepeatInput(Visualisation):

    def __call__(self, inputs, layer, repeat=1):
        return inputs.repeat(repeat, 1, 1, 1), None

```

This class just repeat the input for `repeat` times. Now we have to create a `WebInterface` to make this class communicate with the application. Be careful to the next step.


```python
from mirror.visualisations.web import WebInterface

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
