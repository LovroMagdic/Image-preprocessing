import cv2 
import pytesseract
import os
import numpy as np

from PIL import Image, ImageEnhance
from pathlib import Path
from matplotlib import pyplot as plt

#C:\Users\Lovro\Desktop\projekt\ProjektR\dataset
home = str(Path.home())
dir = os.path.join(home, "Desktop", "projekt", "projektR", "dataset")
dir = dir.replace("\\", "/")

arr = []
for filename in os.scandir(dir):
    if filename.is_file():
        arr.append(filename.path)

for each in arr:

    img = cv2.imread(each, 0)

    image = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,25,4)
    each = each.replace("dataset","dataset_adaptive_threshold")
    cv2.imwrite(each, image)
