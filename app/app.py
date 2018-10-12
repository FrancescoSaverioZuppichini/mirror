from flask import Flask, request, Response, send_file
import jsonpickle
import numpy as np
import cv2
from PIL import Image
from io import StringIO
import matplotlib.pyplot as plt

from torchvision.models import resnet18
import torch.nn as nn

from torchvision.transforms import ToTensor, Resize, Compose
import torch
# Initialize the Flask application
app = Flask(__name__)

model = resnet18(True)

layer = model.layer1

cat = Image.open("cat.jpg")

input = Compose([Resize((224,224)), ToTensor()])(cat)

input = input.view(1,3,224,224)

output = model(input)

print(model)

class Node:
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value
        self.children = []

    def __str__(self):
        return str(self.value)

def traverse(module, node):
    for m in module.children():
        if m not in node.children:
            child = Node(parent=node, value=m)
            node.children.append(child)
            # module.child.append(m)
            traverse(m, child)

root = Node(parent=None, value=model)

traverse(model, root)
print(model.child[1].child)

# x = input
# for l in model.children():
#     print(l)
#     x = l(x)
#     out = x.squeeze()
#     print(out.shape)
#
#     f, w, h = out.shape
#
#     for img in out:
#         img = img.detach().numpy()
#         plt.title(l)
#         plt.imshow(img)
#         plt.show()

# img = weights[0][0][0]
# b, c, w,h = input.shape
#
# img = input.detach().numpy()
#
# img = img.reshape([w,h,3])
#
# print(img.shape)
# img = np.uint8(img * 255)
#
# pil_img = Image.fromarray(img, 'RGB')
# print('k')
# pil_img.save('test.jpg')
# route http posts to this method
# @app.route('/api/test', methods=['POST'])
# def test():
#     r = request
#
#     # img = weights[0][0]
#
#     pil_img = Image.fromarray(img)
#
#     img_io = StringIO()
#     pil_img.save(img_io, 'JPEG', quality=70)
#     img_io.seek(0)
#
#     return send_file(img_io, mimetype='image/jpeg')
#
#
# # start flask app
# app.run(host="0.0.0.0", port=5000)