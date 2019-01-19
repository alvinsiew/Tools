# USAGE
# python simple_request.py

# import the necessary packages
import requests
import cv2

# initialize the Keras REST API endpoint URL along with the input
# image path
KERAS_REST_API_URL = "http://localhost:5000/predict"
IMAGE_PATH = "background2.jpeg"
#IMAGE_PATH = "dog.jpg"
# load the input image and construct the payload for the request

content_type = 'image/jpeg'
headers = {'content-type': content_type}
# image = open(IMAGE_PATH, "rb").read()
image = cv2.imread(IMAGE_PATH)
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', image)


payload = {"image": image}

# submit the request
# r = requests.post(KERAS_REST_API_URL, files=payload).json()
response = requests.post(KERAS_REST_API_URL, data=img_encoded.tostring(), headers=headers).json()

# ensure the request was sucessful
if response["success"]:
	# loop over the predictions and display them
	for (i, result) in enumerate(response["predictions"]):
		print("{}. {}: {:.2f}%".format(i + 1, result["label"],
			result["probability"]))

# otherwise, the request failed
else:
	print("Request failed")
