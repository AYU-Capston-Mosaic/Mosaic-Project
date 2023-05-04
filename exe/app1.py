#!/usr/bin/env python
# coding: utf-8

# In[3]:


from pdf2image import convert_from_path
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image, ImageTk
import easyocr


# In[4]:


# easyocr
reader = easyocr.Reader(['ko','en'])
result = reader.readtext("C:/Users/82109/mosaic/img/0.jpg", width_ths=0.1, adjust_contrast=0.1)
for i in result[:100]:
    print(i)


# In[1]:


'''
import tkinter as tk

img = cv2.imread('./img/0.jpg')

img = Image.fromarray(img)    # 이미지에 그리기 위해서 CV2 이미지를 PIL 이미지 객체로 변환
font = ImageFont.truetype('./assets/gulim.ttf',15)
draw = ImageDraw.Draw(img)

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(255, 3),dtype="uint8")

for i in result :
    # 이미지 좌표 변수 지정
    x = i[0][0][0] 
    y = i[0][0][1] 
    w = i[0][1][0] - i[0][0][0] 
    h = i[0][2][1] - i[0][1][1]
    
    # 랜덤 색상 지정
    color_idx = random.randint(0,255)
    color = [int(c) for c in COLORS[color_idx]]

    # 이미지에 인식 영역 / 인식 문자 출력
    draw.rectangle(((x, y), (x+w, y+h)), outline=tuple(color), width=2)
    draw.text((int((x + x + w) / 2) , y-2),str(i[1]), font=font, fill=tuple(color),)

# img = Image.fromarray(binary)
imgtk = ImageTk.PhotoImage(image=img)

plt.figure(figsize=(50,50))
plt.imshow(img)
plt.show()
root = tk()
root.mainloop()
# plt.savefig('./result/sample_img0_7.jpg')

'''


# In[2]:


import tkinter as tk
import cv2
from PIL import Image, ImageTk, ImageDraw

result = []

class App:
    def __init__(self, master):
        global result
        
        # 이미지 열기
        self.src = cv2.imread('C:/Users/82109/mosaic/img/0.jpg')
        img_w, img_h, img_a = self.src.shape # image size(height, width, alpha)

        self.master = master
        self.canvas = tk.Canvas(master, width=int(img_w * 0.25), height=int(img_h * 0.5))
        self.canvas.pack()

        self.src = cv2.resize(self.src, (int(img_w * 0.25), int(img_h * 0.5)))
        reader = easyocr.Reader(['ko','en'])
        result = reader.readtext(self.src, width_ths=0.1, adjust_contrast=0.1)
        
        img = Image.fromarray(self.src)    # 이미지에 그리기 위해서 CV2 이미지를 PIL 이미지 객체로 변환
        # font = ImageFont.truetype('./assets/gulim.ttf',15)
        draw = ImageDraw.Draw(img)

        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(255, 3),dtype="uint8")

        for i in result :
            # 이미지 좌표 변수 지정
            x = i[0][0][0] 
            y = i[0][0][1] 
            w = i[0][1][0] - i[0][0][0] 
            h = i[0][2][1] - i[0][1][1]
            
            # 랜덤 색상 지정
            color_idx = random.randint(0,254)
            color = [int(c) for c in COLORS[color_idx]]

            # 이미지에 인식 영역 / 인식 문자 출력
            draw.rectangle(((x, y), (x+w, y+h)), outline=tuple(color), width=1)
            # draw.text((int((x + x + w) / 2) , y-2),str(i[1]), font=font, fill=tuple(color),)
        self.image = img
        self.image_tk = ImageTk.PhotoImage(self.image)

        # 이미지를 Canvas 위젯에 배치
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

        # 클릭 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        global result

        # 클릭된 위치 계산
        input_x, input_y = event.x, event.y

        # 모자이크 처리
        for i in result:
            x = i[0][0][0] 
            y = i[0][0][1] 
            w = i[0][1][0]
            h = i[0][2][1]
            if x <= input_x <= w and y <= input_y <= h:
                draw = ImageDraw.Draw(self.image)
                draw.rectangle((x, y, w, h), fill=(0, 0, 0))

        # 모자이크 처리된 이미지를 다시 Tkinter PhotoImage로 변환하여 업데이트
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

