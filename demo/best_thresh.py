import cv2 
import pytesseract
import os
import numpy as np
import math

best_thresh = 0
ar = []
arr = []

for i in range(100, 250, 5): # i == best_thresh
    image = cv2.imread("Z05353422.jpg")
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, i, 255, cv2.THRESH_BINARY)
    cv2.imwrite('test-bw.jpg', thresh)

    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    image_copy = image.copy()

    cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

    c = max(contours, key = cv2.contourArea)
    #print(cv2.contourArea(c))
    x,y,w,h = cv2.boundingRect(c)
    #print(w*h)

    ar.append([cv2.contourArea(c), w*h, i])
    arr.append(int(w*h)-int(cv2.contourArea(c)))

index = arr.index(min(arr))
print(ar[index])

i = int(ar[index][2])
image = cv2.imread("Z05353422.jpg")
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(img_gray, i, 255, cv2.THRESH_BINARY)
cv2.imwrite('test-bw.jpg', thresh)

contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
image_copy = image.copy()

cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

c = max(contours, key = cv2.contourArea)
x,y,w,h = cv2.boundingRect(c)
cv2.rectangle(thresh,(x,y),(x+w,y+h),(0,255,0),5)
foreground = image[y:y+h,x:x+w]
cv2.imwrite("test.jpg", foreground)