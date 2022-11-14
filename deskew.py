import cv2
import numpy as np
import math

def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

real_img = cv2.imread('Z05353721.jpg')
img = cv2.imread('Z05353721-proc.jpg')
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
print(global_angle)
cv2.imwrite('Z05353721-lines.jpg', img)

deskew_img = rotateImage(real_img, -1 * global_angle)

cv2.imwrite("Z05353721-deskew.jpg", deskew_img)
