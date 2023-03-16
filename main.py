import cv2 
import numpy as np
import os
from cv2 import dnn_superres


dir = os.getcwd()
dir = os.path.join(dir,"dataset")
dir = dir.replace("\\", "/")
arr = [] # sadrzi imena svih dataset slika

#we are saving each file stored in dataset in arr array so that is easier to iterate after
for filename in os.scandir(dir):
    if filename.is_file():
        arr.append(filename.path)

# Create an SR object
sr = dnn_superres.DnnSuperResImpl_create()
for each in arr:
    # Read image
    image = cv2.imread(each)

    # Read the desired model
    path = r'/Users/lovro/Desktop/image-preprocessing - testing branch/FSRCNN_Tensorflow-master/models/FSRCNN_x4.pb'
    sr.readModel(path)

    # Set the desired model and scale to get correct pre- and post-processing
    sr.setModel("fsrcnn", 4)

    # Upscale the image
    result = sr.upsample(image)

    # Save the image
    each = each.replace("dataset", "dataset_upscaled")
    cv2.imwrite(each, result)