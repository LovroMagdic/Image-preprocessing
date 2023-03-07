import cv2
from cv2 import dnn_superres

# Create an SR object
sr = dnn_superres.DnnSuperResImpl_create()

# Read image
image = cv2.imread('original.jpg')

# Read the desired model
path = r'/Users/lovro/Desktop/test/FSRCNN_Tensorflow-master/models/FSRCNN_x4.pb'
sr.readModel(path)

# Set the desired model and scale to get correct pre- and post-processing
sr.setModel("fsrcnn", 4)

# Upscale the image
result = sr.upsample(image)

# Save the image
cv2.imwrite("up.jpg", result)