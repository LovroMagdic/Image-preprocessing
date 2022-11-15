import cv2 
import pytesseract
import os
import numpy as np

from PIL import Image, ImageEnhance
from pathlib import Path
from matplotlib import pyplot as plt

def remove_borders(image):
    contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return (crop)

#C:\Users\Lovro\Desktop\projekt\ProjektR\dataset_processed_deskew
home = str(Path.home())
dir = os.path.join(home, "Desktop", "projekt","ProjektR", "dataset_processed")
dir = dir.replace("\\", "/")

arr = [] # sadrzi imena svih dataset slika
for filename in os.scandir(dir):
    if filename.is_file():
        arr.append(filename.path)

for each in arr:
    new = cv2.imread(each)
    new = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)
    no_borders = remove_borders(new)
    each = each.replace("dataset_processed", "dataset_nobg")
    cv2.imwrite(each, no_borders)
