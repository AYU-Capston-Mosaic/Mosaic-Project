import cv2
import easyocr
import numpy as np
import random
from PIL import Image, ImageTk, ImageDraw
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification

def main(self):
    self.canvas.delete(self.img_id)
    self.bbox = []

    self.src = cv2.imread(self.img_name)
    img_w, img_h, img_a = self.src.shape # image size(height, width, alpha)

    self.src = cv2.resize(self.src, (int(img_w * 0.6), int(img_h * 1.2)), Image.ANTIALIAS)
    reader = easyocr.Reader(['ko','en'])
    self.bbox = reader.readtext(self.src, width_ths=0.1, height_ths=0.1)
    print(self.img_name)
    
    img = Image.fromarray(self.src)    # 이미지에 그리기 위해서 CV2 이미지를 PIL 이미지 객체로 변환
    self.original_image = Image.fromarray(self.src)
    draw = ImageDraw.Draw(img)

    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(255, 3),dtype="uint8")

    for i in self.bbox:
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

    self.image = img
    self.image_tk = ImageTk.PhotoImage(self.image)

    # 이미지를 Canvas 위젯에 배치
    self.img_id = self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)
    
    toast = ToastNotification(
            title="모자이크에크",
            message="모자이크가 정상적으로 완료되었습니다.",
            duration=10000,
    )
    toast.show_toast()

