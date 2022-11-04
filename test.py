import cv2 
import pytesseract
import os
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

arr = [] # sadrzi imena svih dataset slika


dir = "C:/Users/Lovro/Desktop/projekt/ProjektR/dataset"
for filename in os.scandir(dir):
    if filename.is_file():
        arr.append(filename.path)

print(arr)
for each in arr:
    
    
    #1
    image = cv2.imread(each, flags=cv2.IMREAD_COLOR)
    kernel = np.array([[0, -1, 0],
                    [-1, 5,-1],
                    [0, -1, 0]])
    image_sharp = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    each = each.replace("dataset", "dataset_processed" )
    cv2.imwrite(each, image_sharp)

    #2
    im = Image.open(each)

    #image brightness enhancer
    enhancer = ImageEnhance.Contrast(im)

    factor = 1.5 #increase contrast
    im_output = enhancer.enhance(factor)
    im_output.save(each)

    #3
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

    thresh, im_bw = cv2.threshold(gray_image, 230, 240, cv2.THRESH_BINARY)
    cv2.imwrite(each, im_bw)