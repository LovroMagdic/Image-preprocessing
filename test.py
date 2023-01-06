import cv2 
import pytesseract
import os
import numpy as np
import math

from PIL import Image, ImageEnhance
from pathlib import Path
from matplotlib import pyplot as plt

#C:\Users\Lovro\Desktop\ProjektR\dataset
home = str(Path.home())
dir = os.path.join(home, "Desktop", "ProjektR", "dataset")
dir = dir.replace("\\", "/")

arr = [] # sadrzi imena svih dataset slika

for filename in os.scandir(dir):
    if filename.is_file():
        arr.append(filename.path)

for each in arr:
    each = each.replace("dataset", "dataset_contour")
    image = cv2.imread(each, 0)

    blur = cv2.GaussianBlur(image,(5,5),0)
    alpha = 1.5
    beta = (1.0 - alpha)
    sharp = cv2.addWeighted(image, alpha, blur, beta, 0.0)
    # each = each.replace("dataset_contour", "dataset_blur")
    cv2.imwrite(each, sharp)

