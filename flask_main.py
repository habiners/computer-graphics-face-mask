from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jsonpify import jsonify

from testing import mask_detector

from PIL import Image
import numpy as np
import io, base64
from base64 import b64decode

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/')
def greet():
    return jsonify({"text": "Welcome to the Mask Detector Web Service!"})

@app.route("/mask-detector/<path:url>")
def image_check(url):
    try:
        data = url.split(',', 1)[1]
        base64_decoded = b64decode(data)
        image_file = io.BytesIO(base64_decoded)
        image = Image.open(image_file)
        image_np = np.array(image, dtype=np.uint8)
        result = mask_detector(image_np)
        print(f"Verdict: {result}")
        return jsonify({"result": result})
    except Exception as e:
        print(e)
        return jsonify({"result": "An error occured. Exception: " + e})

if __name__ == "__main__":
    app.run(port=5002)
