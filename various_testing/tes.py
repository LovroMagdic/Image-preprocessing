import cv2 
import pytesseract
import os
import numpy as np
import math

from PIL import Image, ImageEnhance
from pathlib import Path
from matplotlib import pyplot as plt

image = cv2.imread("various_testing/Z05353721.jpg")
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)
# cv2.imwrite('demo/dataset-result/Z05353401-bw.jpg', thresh)

contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
image_copy = image.copy()

cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=4, lineType=cv2.LINE_AA)
cv2.imwrite("image-draw.jpg", image_copy)

# black_canvas = np.zeros_like(img_gray)
# cv2.drawContours(black_canvas, contours, -1, 255, cv2.FILLED) # this gives a binary mask
# cv2.imwrite("test.jpg", black_canvas)