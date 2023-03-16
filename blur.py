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

for each in arr:
    img = cv2.imread(each, 0)
    blur = cv2.blur(img,(10,10))

    each = each.replace("dataset", "dataset_blurred")
    cv2.imwrite(each, blur)
