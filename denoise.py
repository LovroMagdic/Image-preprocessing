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
    each = each.replace("dataset", "dataset_final")
    img = cv2.imread(each,0)
    ret, bw = cv2.threshold(img, 128,255,cv2.THRESH_BINARY_INV)

    connectivity = 4
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(bw, connectivity, cv2.CV_32S)
    sizes = stats[1:, -1]; nb_components = nb_components - 1
    min_size = 50 #threshhold value for small noisy components
    img2 = np.zeros((output.shape), np.uint8)

    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            img2[output == i + 1] = 255

    res = cv2.bitwise_not(img2)
    each = each.replace("dataset_final", "dataset_denoise")
    cv2.imwrite(each, res)