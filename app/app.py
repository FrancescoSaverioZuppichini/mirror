from flask import Flask, request, Response, send_file, jsonify
import jsonpickle
import numpy as np
import cv2
from PIL import Image
from io import StringIO
import matplotlib.pyplot as plt
from pprint import pprint
import io
from torchvision.models import resnet18

from torchvision.transforms import ToTensor, Resize, Compose
# Initialize the Flask application
from tree import Tracer
app = Flask(__name__)

model = resnet18(True)

layer = model.layer1

cat = Image.open("cat.jpg")

input = Compose([Resize((224,224)), ToTensor()])(cat)

input = input.view(1,3,224,224)


tracer = Tracer(module=model)
tracer(input)

# pprint(tracer.serialized)

@app.route('/api/model', methods=['GET'])
def api_model():
    model = tracer.serialized

    response = jsonify(model)

    return response

@app.route('/api/model/layer/<id>')
def api_model_layer(id):
    id = int(id)
    name = str(tracer.idx_to_value[id])
    print(name)

    return Response(response=name)

@app.route('/api/model/layer/output/<id>')
def api_model_layer_output(id):
    id = int(id)
    model, inputs, outputs = tracer.idx_to_value[id].traced[0]

    mode = request.args.get('mode')

    response = []

    if mode == 'image':
       response = ['/api/model/image/{}/{}'.format(id, i) for i in range(outputs.shape[1])]

    response = jsonify(response)
    return response

@app.route('/api/model/image/<layer_id>/<output_id>')
def api_model_layer_output_image(layer_id, output_id):
    layer_id = int(layer_id)
    output_id = int(output_id)
    model, inputs, outputs = tracer.idx_to_value[layer_id].traced[0]

    output = outputs[0][output_id]
    output = output.detach().numpy() * 255

    pil_img = Image.fromarray(output)
    pil_img = pil_img.convert('L')
    img_io = io.BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')


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
app.run(host="0.0.0.0", port=5000)