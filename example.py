from mirror import mirror

from PIL import Image

from torchvision.models import resnet101
from torchvision.transforms import ToTensor, Resize, Compose

model = resnet101(True)

cat = Image.open("cat.jpg")

input = Compose([Resize((224,224)), ToTensor()])(cat)

input = input.view(1,3,224,224)

mirror(input, model)