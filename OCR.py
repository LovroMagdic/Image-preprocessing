import cv2 
import pytesseract
import os
import numpy as np

from PIL import Image, ImageEnhance
from pathlib import Path
from matplotlib import pyplot as plt


#C:\Users\Lovro\Desktop\projekt\ProjektR\dataset_processed
home = str(Path.home())
dir = os.path.join(home, "Desktop", "projekt", "projektR","dataset_nobg")
dir = dir.replace("\\", "/")

arr = []
arr_names = []
for filename in os.scandir(dir):
    if filename.is_file():
        arr.append(filename.path)
        arr_names.append(filename.name)
i = 0
os.chdir(r"C:\Users\Lovro\Desktop\projekt\ProjektR\read")
for each in arr:
    file_name = os.path.join(os.path.dirname(__file__), each)
    assert os.path.exists(file_name)
    img = cv2.imread(file_name, -1)
    # Adding custom options
    custom_config = r'--oem 3 --psm 6'
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    string = pytesseract.image_to_string(img, config=custom_config)

    
    txt_name = str(arr_names[i].replace(".jpg", "")) + ".txt"
    text_file = open(txt_name, "w")
    i += 1
    text_file.write(string)
    text_file.close()
