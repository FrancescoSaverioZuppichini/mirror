from mirror import mirror

from PIL import Image

from torchvision.models import resnet101, resnet18, vgg16
from torchvision.transforms import ToTensor, Resize, Compose

# model = resnet101(True)
model = vgg16(True)

# cat = Image.open("/home/francesco/Documents/mirror/mirror/resources/sky-dd.jpeg")

cat = Image.open("./cat.jpg")

#
# cat = Image.open("/home/francesco/Documents/mirror/mirror/resources/the_starry_night-wallpaper-1920x1200.jpg")

input = Compose([Resize((224,224)), ToTensor()])(cat)
#
# input = Compose([ToTensor()])(cat)

input = input.unsqueeze(0)

mirror(input, model)