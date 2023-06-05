import cv2 
import numpy as np
import os
from cv2 import dnn_superres


dir = os.getcwd()
dir = os.path.join(dir,"dataset_filled")
dir = dir.replace("\\", "/")
arr = [] # sadrzi imena svih dataset slika

#we are saving each file stored in dataset in arr array so that is easier to iterate after
for filename in os.scandir(dir):
    if filename.is_file():
        arr.append(filename.path)

print(arr)

for each in arr:
    img = cv2.imread(each)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray,10,0.01,10)
    corners = np.int64(corners)
    print(corners)
    for i in corners:
        x,y = i.ravel()
        cv2.circle(img,(x,y),5,255,-1)
 
    each = each.replace("dataset_filled", "dataset_corner")
    cv2.imwrite(each, img)