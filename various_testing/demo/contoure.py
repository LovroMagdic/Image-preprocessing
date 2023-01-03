import cv2 
import pytesseract
import os
import numpy as np
import math

# C:\Users\Lovro\Desktop\projektR-isprobavanje\contour\dataset
dir = r"C:\Users\Lovro\Desktop\projektR-isprobavanje\contour\dataset_deskewed"

arr = [] # sadrzi imena svih dataset slika
for filename in os.scandir(dir):
    if filename.is_file():
        arr.append(filename.path)

#spremljene slike za pronalazenje linija
for each in arr:

    # read the image
    image = cv2.imread(each)

    # convert the image to grayscale format
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply binary thresholding
    ret, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)

    # visualize the binary image
    #cv2.imwrite('Z05353422-bw.jpg', thresh)

    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
                                        
    # draw contours on the original image
    image_copy = image.copy()

    cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    #cv2.imwrite("Z05353422-draw.jpg", image_copy)
    c = max(contours, key = cv2.contourArea)
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(thresh,(x,y),(x+w,y+h),(0,255,0),5)
    foreground = image[y:y+h,x:x+w]
                    
    # see the results
    each = each.replace("dataset_deskewed", "dataset_contour")
    cv2.imwrite(each, foreground)
