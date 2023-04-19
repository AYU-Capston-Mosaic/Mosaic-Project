from pdf2image import convert_from_path
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image, ImageTk
import easyocr

# pdf2image
file_name = "sample_doc.pdf" # pdf 파일 이름

pages = convert_from_path("./assets/" + file_name) # 파일 경로

for i, page in enumerate(pages):
	page.save("./img/"+str(i)+".jpg", "JPEG")

# easyocr
reader = easyocr.Reader(['ko','en'])
result = reader.readtext("./img/0.jpg", width_ths=0.1, adjust_contrast=0.1)
for i in result[:100]:
    print(i)