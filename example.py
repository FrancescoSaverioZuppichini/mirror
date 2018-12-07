from mirror import mirror

from PIL import Image

from torchvision.models import resnet101, resnet18
from torchvision.transforms import ToTensor, Resize, Compose

# model = resnet101(True)
model = resnet18(True)

cat = Image.open("cat.jpg")

input = Compose([Resize((224,224)), ToTensor()])(cat)

input = input.view(1,3,224,224)

mirror(input, model)