# USAGE
# Start the server:
# 	python run_keras_server.py
# Submit a request via cURL:
# 	curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'
# Submita a request via Python:
#	python simple_request.py

# import the necessary packages
from keras.applications import ResNet50
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from werkzeug.utils import secure_filename
#from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import pickle
import io
import tensorflow as tf
import cv2
import os

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
model = None
lb = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def loadModel():
	# load the pre-trained Keras model (here we are using a model
	# pre-trained on ImageNet and provided by Keras, but you can
	# substitute in your own networks just as easily)
	global model
	#model = ResNet50(weights="imagenet")

	print("[INFO] loading network...")
	#model = load_model("../trained_model.model")
	model = load_model("../pikachu_trained_model.model")
	
	# this is key : save the graph after loading the model
	global graph
	graph = tf.get_default_graph()

def prepare_image(image, target):
	
	img = image
	# resize the input image and preprocess it
	img = img.resize(target)
	img = img.astype("float") / 255.0
	img = img_to_array(img)
	img = np.expand_dims(img, axis=0)
	#image = imagenet_utils.preprocess_input(image)

	# return the processed image
	return img

@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}

	r = flask.request
	
	nparr = np.fromstring(r.data, np.uint8)
	# decode image
	image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	image = cv2.resize(image, (224, 224))
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)

	print('image received. size={}x{}'.format(image.shape[1], image.shape[0]))

	# preprocess the image and prepare it for classification
	# image = prepare_image(img, target=(224, 224))

	lb = pickle.loads(open("../labelbin.pickle", "rb").read())
	print("lb.classes_",lb.classes_)

	with graph.as_default():
		#preds = model.predict(image)
		proba = model.predict(image)[0]
		idx = np.argmax(proba)
		label = lb.classes_[idx]

		print("label:",label)

	# #results = imagenet_utils.decode_predictions(preds)
	data["predictions"] = []
	
	for i in range(len(proba)):
		print(lb.classes_[i], proba[i] * 100, "%")
		r = {"label": lb.classes_[i], "probability": float(proba[i] * 100)}
		data["predictions"].append(r)

	# # indicate that the request was a success
	data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	loadModel()
	app.run('0.0.0.0')
