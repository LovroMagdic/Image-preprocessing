import cv2 
import pytesseract
import os
import numpy as np

from PIL import Image, ImageEnhance
from pathlib import Path
from matplotlib import pyplot as plt

#prvi pokusaj obrade slike, ne daje dobre rezultate za sve slike, lose obradi slike za izuzetno izblijedenim tekstom
#adaptive_threshold daje bolje rezultate

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#C:\Users\Lovro\Desktop\projekt\ProjektR\dataset_processed
home = str(Path.home())
dir = os.path.join(home, "Desktop", "projekt", "projektR","dataset_deskewed")
dir = dir.replace("\\", "/")

arr = [] # sadrzi imena svih dataset slika
#dir = "C:/Users/Lovro/Desktop/projekt/ProjektR/dataset"
for filename in os.scandir(dir):
    if filename.is_file():
        arr.append(filename.path)

#iteriranje svake slike u folderu
for each in arr:

    #1 izostravanje slike
    image = cv2.imread(each, flags=cv2.IMREAD_COLOR)
    kernel = np.array([[0, -1, 0],
                    [-1, 5,-1],
                    [0, -1, 0]])
    image_sharp = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    each = each.replace("dataset_deskewed", "dataset_processed" )
    cv2.imwrite(each, image_sharp)

    #2 promjena kontrasta slike
    im = Image.open(each)
    enhancer = ImageEnhance.Contrast(im)
    factor = 1.5 #promjenjiv faktor
    im_output = enhancer.enhance(factor)
    im_output.save(each)

    #3 postupak thresholda, potrebno je dobit grayscale pa bw format te provest threshold
    image_file = each
    img = cv2.imread(image_file)

    gray_image = grayscale(img)
    cv2.imwrite(each, gray_image)

    image_gray = each
    img = cv2.imread(image_gray)

    inverted_image = cv2.bitwise_not(img)
    cv2.imwrite(each, inverted_image)
    image_file = each
    img = cv2.imread(image_file)

    thresh, im_bw = cv2.threshold(gray_image, 230, 240, cv2.THRESH_BINARY) #odabrane 230 i 240 zbog izrazitog izblijedenog teksta na pojedinim slikama
    cv2.imwrite(each, im_bw)