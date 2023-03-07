import cv2 
import pytesseract
import os
import numpy as np
import math
from pathlib import Path
import cv2 
import numpy as np
import os
from cv2 import dnn_superres

dir = os.getcwd()
dir = os.path.join(dir,"dataset_denoise")
dir = dir.replace("\\", "/")

arr = []
arr_names = []
for filename in os.scandir(dir):
    if filename.is_file():
        arr.append(filename.path)
        arr_names.append(filename.name)
i = 0

dir = os.getcwd()
dir = os.path.join(dir,"ocr")
dir = dir.replace("\\", "/")
os.chdir(dir) #postion in folder where you want to save images

#script for iterating through images and saving results in .txt file
for each in arr:
    file_name = os.path.join(os.path.dirname(__file__), each)
    assert os.path.exists(file_name)
    img = cv2.imread(file_name, -1)
    custom_config = r'--oem 3 --psm 6'
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.3.0_1/bin/tesseract'
    string = pytesseract.image_to_string(img, config=custom_config)

    #odrediste procitanog teksta, ime_slike.txt
    txt_name = str(arr_names[i].replace(".jpg", "")) + ".txt"
    text_file = open(txt_name, "w")
    i += 1
    text_file.write(string)
    text_file.close()