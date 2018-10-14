from flask import Flask, request, Response, send_file, jsonify
import jsonpickle
import numpy as np
import cv2
from PIL import Image
from io import StringIO
import matplotlib.pyplot as plt
from pprint import pprint
import io
from torchvision.models import resnet18, resnet101

from torchvision.transforms import ToTensor, Resize, Compose
# Initialize the Flask application
from tree import Tracer
app = Flask(__name__)

model = resnet101(True)

layer = model.layer1

cat = Image.open("cat.jpg")

input = Compose([Resize((224,224)), ToTensor()])(cat)

input = input.view(1,3,224,224)


tracer = Tracer(module=model)
tracer(input)

MAX_LINKS_EVERY_REQUEST = 25

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
    # id = int(id)
    try:

        model, inputs, outputs = tracer.idx_to_value[id].traced[0]

    except KeyError:

        return Response(status=500, response='Index not found.')

    if len(outputs.shape) < 3:
        return Response(status=404, response='Outputs are not images.')

    # mode = request.args.get('mode')
    last = int(request.args['last'])
    print(last)
    response = []

    max = (last + MAX_LINKS_EVERY_REQUEST) % outputs.shape[1]

    response = ['/api/model/image/{}/{}'.format(id, i) for i in range(last, max)]

    response = jsonify(response)
    return response

@app.route('/api/model/image/<layer_id>/<output_id>')
def api_model_layer_output_image(layer_id, output_id):
    # layer_id = int(layer_id)
    output_id = int(output_id)
    try:
        model, inputs, outputs = tracer.idx_to_value[layer_id].traced[0]

        output = outputs[0][output_id]
        output = output.detach().numpy() * 255

        pil_img = Image.fromarray(output)
        pil_img = pil_img.convert('L')
        img_io = io.BytesIO()
        pil_img.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')

    except KeyError:

        return Response(status=500, response='Index not found.')

app.run(host="0.0.0.0", port=5000)