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

def thin_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,1),np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

def thick_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

#C:\Users\Lovro\Desktop\ProjektR\dataset
home = str(Path.home())
dir = os.path.join(home, "Desktop", "ProjektR", "dataset")
dir = dir.replace("\\", "/")

arr = [] # sadrzi imena svih dataset slika


for filename in os.scandir(dir):
    if filename.is_file():
        arr.append(filename.path)

#spremljene slike za pronalazenje linija
for each in arr:
    tmp_img = cv2.imread(each)

    gray_image = grayscale(tmp_img)
    thresh, im_bw = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
    each = each.replace("dataset", "dataset_processed_deskew")
    cv2.imwrite(each, im_bw)

#spremanje slika za rotiranje i traznje linija
for each in arr:

    image = cv2.imread(each, 0)
    each = each.replace("dataset","dataset_copy")
    cv2.imwrite(each, image)

#pronalaznje linija i rotiranje
#real_img ona koja ustvari rotiram, img je slika za pronalaznje linija
for each in arr:
    arr1 = []
    each = each.replace("dataset", "dataset_copy")
    real_img = cv2.imread(each)
    each=each.replace("dataset_copy", "dataset_processed_deskew")
    img = cv2.imread(each)
    arr2 = []
    global_angle = 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

    for r_theta in lines:
        arr1 = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr1

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
        
        #uzimanje samo kuteva izmedu 0-10 stup, izbacujemo prevelike kuteve
        if res > 0 and res < 10:
            arr2.append(res)
            global_angle += res
    
    global_angle = global_angle/len(arr2) #konacni kut korekcije je prosjek kuteva koje smo uzeli u obzir
    # if "668" in each:
    #     cv2.imwrite('test-668.jpg', img)
    #     print(arr2)

    deskew_img = rotateImage(real_img, -1 * global_angle)

    each=each.replace("dataset_processed_deskew", "dataset_deskewed")
    cv2.imwrite(each, deskew_img)

# pronalazenje najboljeg thresholda
ar = []
array = []

#ovdje je bug ne uzimas deskew-ane slike kasnije, nego ciste iz dataseta

for each in arr:
    each = each.replace("dataset","dataset_deskewed")
    for i in range(100, 235, 5): # i == best_thresh
        image = cv2.imread(each)
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, i, 255, cv2.THRESH_BINARY)
        # cv2.imwrite('demo/test-bw.jpg', thresh)

        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        image_copy = image.copy()

        cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        # cv2.imwrite("image-draw.jpg", image_copy)

        c = max(contours, key = cv2.contourArea)
        # print(cv2.contourArea(c))
        x,y,w,h = cv2.boundingRect(c)
        # print(w*h)

        ar.append([cv2.contourArea(c), w*h, i])
        array.append(int(w*h)-int(cv2.contourArea(c)))

    index = array.index(min(array))
    # print(ar[index])

    i = int(ar[index][2])
    # each = each.replace("dataset_deskewed","dataset")
    image = cv2.imread(each)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, i, 255, cv2.THRESH_BINARY)
    # cv2.imwrite('demo/dataset-result/Z05353401-bw.jpg', thresh)

    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    image_copy = image.copy()

    cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

    c = max(contours, key = cv2.contourArea)
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(thresh,(x,y),(x+w,y+h),(0,255,0),5)
    foreground = image[y:y+h,x:x+w]
    each = each.replace("dataset_deskewed", "dataset_contour")
    cv2.imwrite(each, foreground)

for each in arr:
    each = each.replace("dataset", "dataset_contour")
    image = cv2.imread(each, 0)

    blur = cv2.GaussianBlur(image,(5,5),0)
    alpha = 1.5
    beta = (1.0 - alpha)
    sharp = cv2.addWeighted(image, alpha, blur, beta, 0.0)
    each = each.replace("dataset_contour", "dataset_blur")
    cv2.imwrite(each, sharp)
'''
for each in arr:
    each = each.replace("dataset", "dataset_blur")
    # thicker font
    image = cv2.imread(each)
    dilated_image = thick_font(image)
    each = each.replace("dataset_blur","dataset_thick")
    cv2.imwrite(each, dilated_image)
'''

for each in arr:
    each = each.replace("dataset","dataset_blur")
    img = cv2.imread(each, 0)

    image = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,25,4)
    each = each.replace("dataset_blur","dataset_adaptive")
    cv2.imwrite(each, image)

for each in arr:

    # thinner font
    each = each.replace("dataset","dataset_adaptive")
    image = cv2.imread(each)
    eroded_image = thin_font(image)
    each = each.replace("dataset_adaptive", "dataset_thin")
    cv2.imwrite(each, eroded_image)

for each in arr:
    each = each.replace("dataset", "dataset_thin")
    image = cv2.imread(each, 0)

    blur = cv2.GaussianBlur(image,(5,5),0)
    alpha = 1.5
    beta = (1.0 - alpha)
    # sharp = cv2.addWeighted(image, alpha, blur, beta, 0.0)
    each = each.replace("dataset_thin", "dataset_final")
    cv2.imwrite(each, blur)

