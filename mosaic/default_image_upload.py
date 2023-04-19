from tkinter import *
from PIL import ImageTk,Image
import os
from pdf2image import convert_from_path
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image, ImageTk
import easyocr

reader = easyocr.Reader(['ko','en'])
result = reader.readtext("./img/0.jpg", width_ths=0.1, adjust_contrast=0.1)
for i in result[:100]:
    print(i)
 
# Anchor path
os.chdir(os.path.abspath(os.path.dirname(__file__)))
 
root = Tk()
root.title('Default Image Uploading')
# root.geometry('800x600')
 
img = ImageTk.PhotoImage(Image.open('img/0.jpg').convert('RGB'))
label = Label(image=img)
label.image = img
label.pack(side="top")
 
# quit = Button(root, text='Quit', command=root.quit)
# quit.pack()
 
root.mainloop()