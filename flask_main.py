
# pip install --upgrade pip setuptools # Done
# pip install virtualenv # Done
# pip install flask
# pip install flask flask-jsonpify flask-sqlalchemy flask-restful flask-cors

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from flask_jsonpify import jsonify

from testing.py import mask_detector

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/')
def greet():
    return jsonify({"text": "Welcome to the Mask Detector Web Service!"})

class Mask_Detector(Resource):
  def get(self, filename):
    return jsonify({"result": mask_detector(filename)})

api.add_resource(Mask_Detector, '/mask-detector/<filename>')

if __name__ == "__main__":
    app.run(port=5002)
