import tkinter as tk
import cv2
import easyocr
import numpy as np
import random
import tempfile
from pdf_to_image import convert_from_path
from PIL import Image, ImageTk, ImageDraw
import tkinter.filedialog as filedialog
import os

class App:
    def __init__(self, master):
        self.imagelist = [] # 변환된 이미지 경로 리스트
        self.idx = 0

        # 파일 선택 버튼 생성
        self.file_button = tk.Button(master, text="Select PDF File", command=self.select_file)
        self.file_button.pack(side="bottom")

        # 이미지 저장 버튼 생성
        self.save_button = tk.Button(master, text="Save Image", command=self.save_image)
        self.save_button.pack(side="bottom")

        # 모자이크 버튼 생성
        self.mosaic_button = tk.Button(master, text="Mosaic Image", command=self.mosaic_image)
        self.mosaic_button.pack(side="bottom")

        # 선택한 파일의 경로 저장할 변수 생성
        self.filepath = ""

    def select_file(self):
        # 파일 선택
        self.filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        
        # 선택한 파일 경로 출력
        print("Selected file:", self.filepath)

    def save_image(self):
        # 파일 선택 여부 확인
        if not self.filepath:
            print("No file selected.")
            return
        
        # PDF를 이미지로 변환
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(self.filepath, output_folder=path, fmt="png")
        
        savepath = self.filepath.split('.')[0]

        for i, page in enumerate(images_from_path):
            image_name = savepath+str(i)+".jpg"
            self.imagelist.append(image_name)
            page.save(image_name, "JPEG")

    def mosaic_image(self):
        print(self.idx, self.imagelist)
        if self.idx == len(self.imagelist): 
            return
        image_name = self.imagelist[self.idx]
        self.idx += 1
        master = tk.Toplevel()
        # 이미지 열기
        self.src = cv2.imread(image_name)
        img_w, img_h, img_a = self.src.shape # image size(height, width, alpha)

        # self.master = master
        self.canvas = tk.Canvas(master, width=int(img_w * 0.25), height=int(img_h * 0.5))
        self.canvas.pack()

        self.src = cv2.resize(self.src, (int(img_w * 0.25), int(img_h * 0.5)))
        reader = easyocr.Reader(['ko','en'])
        self.bbox = reader.readtext(self.src, width_ths=0.1, adjust_contrast=0.1)
        
        img = Image.fromarray(self.src)    # 이미지에 그리기 위해서 CV2 이미지를 PIL 이미지 객체로 변환
        self.original_image = Image.fromarray(self.src)
        # font = ImageFont.truetype('./assets/gulim.ttf',15)
        draw = ImageDraw.Draw(img)

        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(255, 3),dtype="uint8")

        for i in self.bbox :
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

        self.capture_button = tk.Button(master, text="Capture", command=self.capture)
        self.capture_button.pack(side="bottom")
        self.next_button = tk.Button(master, text="Next Page", command=self.mosaic_image)
        self.next_button.pack(side="bottom")
        # 클릭 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.on_click)

    def capture(self):
        # 스크린샷 저장 위치 선택
        filename = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")])
        
        self.original_image.save(filename)

    def on_click(self, event):
        # 클릭된 위치 계산
        input_x, input_y = event.x, event.y

        # 모자이크 처리
        for i in self.bbox:
            x = i[0][0][0] 
            y = i[0][0][1] 
            w = i[0][1][0]
            h = i[0][2][1]
            if x <= input_x <= w and y <= input_y <= h:
                draw = ImageDraw.Draw(self.image)
                draw_origin = ImageDraw.Draw(self.original_image)
                draw.rectangle((x, y, w, h), fill=(0, 0, 0))
                draw_origin.rectangle((x, y, w, h), fill=(0, 0, 0))

        # 모자이크 처리된 이미지를 다시 Tkinter PhotoImage로 변환하여 업데이트
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
