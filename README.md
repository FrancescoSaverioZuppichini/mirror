# Mirror
## Pytorch cnn visualisation

This is a raw beta so expect lots of things to change and improve over time.

![alt](https://raw.githubusercontent.com/FrancescoSaverioZuppichini/mirror/master/mirror/resources/mirror.gif)

### Getting started

To install mirror run

```
pip install git+https://github.com/FrancescoSaverioZuppichini/mirror.git
```

Basic example:

```python
from mirror import mirror

from PIL import Image

from torchvision.models import resnet101
from torchvision.transforms import ToTensor, Resize, Compose
# create a model 
model = resnet101(True)

cat = Image.open("cat.jpg")
# resize the image and make it a tensor
input = Compose([Resize((224,224)), ToTensor()])(cat)
# add 1 dim for batch 
input = input.view(1,3,224,224)
# call mirror with the input and the model 
mirror(input, model)
```

It will automatic open a new tab in your browser


### TODO
- Support multiple inputs and cache them
- Make a generic abstraction of a visualisation in order to add more features 
- Add all visualisation present here https://github.com/utkuozbulak/pytorch-cnn-visualizations
    * [Gradient visualization with vanilla backpropagation](#gradient-visualization)
    * [Gradient visualization with guided backpropagation](#gradient-visualization) [1]
    * [Gradient visualization with saliency maps](#gradient-visualization) [4]
    * [Gradient-weighted [3] class activation mapping](#gradient-visualization) [2] 
    * [Guided, gradient-weighted class activation mapping](#gradient-visualization) [3]
    * [Smooth grad](#smooth-grad) [8]
    * [CNN filter visualization](#convolutional-neural-network-filter-visualization) [9]
    * [Inverted image representations](#inverted-image-representations) [5]
    * [Deep dream](#deep-dream) [10]
    * [Class specific image generation](#class-specific-image-generation) [4]
