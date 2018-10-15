from PIL import Image
from tree import Tracer
from server import build

from torchvision.models import resnet18, resnet101
from torchvision.transforms import ToTensor, Resize, Compose

def mirror(input, model):
    tracer = Tracer(module=model)
    tracer(input)

    app = build(input, model, tracer)
    app.run(host="0.0.0.0", port=5000)


model = resnet101(True)

cat = Image.open("cat.jpg")

input = Compose([Resize((224,224)), ToTensor()])(cat)

input = input.view(1,3,224,224)

mirror(input, model)