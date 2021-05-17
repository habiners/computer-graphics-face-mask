
# pip install --upgrade pip setuptools # Done
# pip install virtualenv # Done
# pip install flask
# pip install flask flask-jsonpify flask-sqlalchemy flask-restful flask-cors

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from flask_jsonpify import jsonify
from flask import request

from testing import mask_detector
from Preprocessing import displayImage

from PIL import Image
import io, base64
from binascii import a2b_base64
from base64 import b64decode

from urllib import request
app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/')
def greet():
    return jsonify({"text": "Welcome to the Mask Detector Web Service!"})

# https://stackoverflow.com/questions/33870538/how-to-parse-data-uri-in-python
# https://stackoverflow.com/questions/31410525/base64-uri-to-png-python
# https://stackoverflow.com/questions/24892035/how-can-i-get-the-named-parameters-from-a-url-using-flask
# https://stackoverflow.com/questions/19395649/python-pil-create-and-save-image-from-data-uri
class Mask_Detector(Resource):
  def get(self):
    # print("NAKA SULOD")
    # print(request.args.get('imguri'))
    uri = request.args.get('imguri')
    with request.urlopen(uri) as response:
        data = response.read()

    print(data)
    # binary_data = a2b_base64(uri)
    # print(binary_data)
    image = Image.open(data)
    displayImage(image)

    # image = Image.open(io.BytesIO(base64.b64decode(uri.split(',')[1])))
    # displayImage(image)
    # return jsonify({"result": mask_detector(uri)})
    return jsonify({"test": "YEET"})

api.add_resource(Mask_Detector, '/mask-detector')

if __name__ == "__main__":
    app.run(port=5002)
