import cv2 
import pytesseract
import os
import numpy as np
import math

from PIL import Image, ImageEnhance
from pathlib import Path
from matplotlib import pyplot as plt

def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

home = str(Path.home())
dir = os.path.join(home, "Desktop", "projekt", "ProjektR", "dataset")
dir = dir.replace("\\", "/")

arr = [] # sadrzi imena svih dataset slika
#dir = "C:/Users/Lovro/Desktop/projekt/ProjektR/dataset"
for filename in os.scandir(dir):
    if filename.is_file():
        arr.append(filename.path)

#spremljene slike za pronalazenje linija
for each in arr:
    tmp_img = cv2.imread(each)

    gray_image = grayscale(tmp_img)
    thresh, im_bw = cv2.threshold(gray_image, 100, 110, cv2.THRESH_BINARY)
    each = each.replace("dataset", "dataset_processed_deskew")
    cv2.imwrite(each, im_bw)

#pronalaznje linija i rotiranje
#real_img ona koja ustvari rotiram, img je slika za pronalaznje linija
for each in arr:
    real_img = cv2.imread(each)
    each=each.replace("dataset", "dataset_processed_deskew")
    img = cv2.imread(each)
    arr2 = []
    global_angle = 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

    for r_theta in lines:
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr

        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*r
        y0 = b*r
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        if ((x2-x1) != 0):
            res1 = (y2-y1)/(x2-x1)
            res2 = y1-res1*x1
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        k2 = res1
        angle = math.tan(abs((k2-0)/(1+k2*0)))
        res = math.degrees(math.atan(angle))
        if res > 0 and res < 10:
            arr2.append(res)
            global_angle += res

    global_angle = global_angle/len(arr2)
    #if "668" in each:
        #cv2.imwrite('test-668.jpg', img)
        #print(global_angle)

    deskew_img = rotateImage(real_img, -1 * global_angle)

    each=each.replace("dataset_processed_deskew", "dataset_deskewed")
    cv2.imwrite(each, deskew_img)