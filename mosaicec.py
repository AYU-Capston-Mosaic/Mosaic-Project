import tkinter as tk
import cv2
import easyocr
import numpy as np
import random
import tempfile
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image, ImageTk, ImageDraw
import os
import tkinter.filedialog as filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
PATH = Path(__file__).parent / 'assets'

class Mosaic(ttk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        # application images
        self.images = [
            ttk.PhotoImage(
                name='logo',
                file=PATH / 'cat.png'),
            ttk.PhotoImage(
                name='file',
                file=PATH / 'pdf.png'),
            ttk.PhotoImage(
                name='mosaic',
                file=PATH / 'eraser.png'),
            ttk.PhotoImage(
                name='next',
                file=PATH / 'arrow.png')
        ]

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=BOTH, expand=True)
        
        # header
        hdr_frame = ttk.Frame(main_frame, padding=(30, 10, 30, 10), bootstyle=DARK)
        hdr_frame.pack(side=TOP, anchor='nw', fill=X, expand=True)
        # hdr_frame.grid(row=0, column=0, columnspan=3, sticky=EW)
        
        hdr_label = ttk.Label(
            master=hdr_frame,
            image='logo',
            bootstyle=(INVERSE, DARK)
        )
        hdr_label.pack(side=LEFT)

        logo_text = ttk.Label(
            master=hdr_frame,
            text='MosaIcEc',
            font=('TkDefaultFixed', 20),
            bootstyle=(INVERSE, DARK)
        )
        logo_text.pack(side=LEFT, padx=10)

        mosaic_btn = ttk.Button(
            master=hdr_frame,
            image='mosaic',
            bootstyle=INFO,
            command=self.mosaic_image
        )
        mosaic_btn.pack(side=RIGHT, fill=BOTH, ipadx=3, ipady=5)

        select_btn = ttk.Button(
            master=hdr_frame,
            image='file',
            bootstyle=INFO,
            command=self.select_file,
        )
        select_btn.pack(side=RIGHT, fill=BOTH, ipadx=3, ipady=5)

        # # results frame
        # results_frame = ttk.Frame(main_frame)
        # results_frame.pack(anchor='n', fill=BOTH, expand=True)

        # # result cards
        # cards_frame = ttk.Frame(
        #     master=results_frame,
        #     name='cards-frame',
        #     bootstyle=SECONDARY
        # )
        # cards_frame.pack(side=TOP, fill=BOTH, expand=YES)

        # note_msg = ttk.Label(
        #     master=cards_frame, 
        #     text='We recommend that you better protect your data', 
        #     anchor=CENTER,
        #     font=('Helvetica', 12, 'italic'),
        #     bootstyle=(INVERSE, SECONDARY)
        # )
        # note_msg.pack(fill=BOTH)

        # # progressbar with text indicator
        # pb_frame = ttk.Frame(results_frame, padding=(0, 10, 10, 10))
        # pb_frame.pack(side=BOTTOM, fill=X, expand=True)

        # pb = ttk.Progressbar(
        #     master=pb_frame,
        #     bootstyle=(SUCCESS, STRIPED),
        #     variable='progress'
        # )
        # pb.pack(side=LEFT, fill=X, expand=YES, padx=(15, 10))

        # ttk.Label(pb_frame, text='%').pack(side=RIGHT)
        # ttk.Label(pb_frame, textvariable='progress').pack(side=RIGHT)
        # self.setvar('progress', 60)

        self.imagelist = [] # 변환된 이미지 경로 리스트
        self.idx = 0

        self.filepath = ""

    def select_file(self):
        # 파일 선택
        self.filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        
        if not self.filepath:
            toast = ToastNotification(
                title="모자이크에크",
                message="PDF 파일만 지원합니다.",
                duration=10000,
            )
            toast.show_toast()
            return
        else:
            toast = ToastNotification(
                title="모자이크에크",
                message="파일이 정상적으로 선택되었습니다.",
                duration=10000,
            )
            toast.show_toast()

        
        # PDF를 이미지로 변환
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(self.filepath, output_folder=path, fmt="png")
        
        savepath = self.filepath.split('.')[0]

        # 이미지 저장용 디렉토리 생성
        if not os.path.exists(savepath+" images/"):
            os.mkdir(savepath+" images/")

        for i, page in enumerate(images_from_path):
            image_name = savepath+" images/"+str(i)+".jpg"
            self.imagelist.append(image_name)
            page.save(image_name, "JPEG")

    # src : 내부, dest : 외부
    def calc_dist(self, src, dest):
        if (src[0][0] > dest[0][0] and src[0][1] > dest[0][1] 
            and src[1][0] < dest[1][0] and src[1][1] > dest[1][1] 
            and src[2][0] < dest[2][0] and src[2][1] < dest[2][1]
            and src[3][0] > dest[3][0] and src[3][1] < dest[3][1]):
            return True
        return False

    def mosaic_image(self):
        print(self.idx, self.imagelist)
        if self.idx == len(self.imagelist): 
            return
        image_name = self.imagelist[self.idx]
        self.idx += 1
        master = self
        # 이미지 열기
        self.src = cv2.imread(image_name)
        img_w, img_h, img_a = self.src.shape # image size(height, width, alpha)

        # self.master = master
        self.canvas = tk.Canvas(master, width=int(img_w * 0.25), height=int(img_h * 0.5))
        self.canvas.pack()

        self.src = cv2.resize(self.src, (int(img_w * 0.25), int(img_h * 0.5)), Image.ANTIALIAS)
        reader = easyocr.Reader(['ko','en'])
        self.bbox = reader.readtext(self.src, text_threshold=0.1, width_ths=0.1,)
        print("BBOX")
        print(self.bbox)
        
        img = Image.fromarray(self.src)    # 이미지에 그리기 위해서 CV2 이미지를 PIL 이미지 객체로 변환
        self.original_image = Image.fromarray(self.src)
        # font = ImageFont.truetype('./assets/gulim.ttf',15)
        draw = ImageDraw.Draw(img)

        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(255, 3),dtype="uint8")

        bbox_max = reader.readtext(self.src, text_threshold=0.1, width_ths=0.5, height_ths=0.5, low_text=0.1)

        print("BBOX MAX")
        print(bbox_max)


        for i in bbox_max:
            flag = False
            for j in self.bbox:
                if (self.calc_dist(i[0], j[0])): # 기존 바운딩박스 영역내에 위치한 경우
                    print("#$314325#%@#%@#%@#^@#^")
                    flag = True
                    break
            if not flag:
                self.bbox.append(i)

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
            # draw.text((int((x + x + w) / 2) , y-2),str(i[1]), font=font, fill=tuple(color),)
        self.image = img
        self.image_tk = ImageTk.PhotoImage(self.image)

        # 이미지를 Canvas 위젯에 배치
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

        next_button = ttk.Button(
            master=master,
            image='next',
            command=self.capture,
            bootstyle=DARK
        )
        next_button.pack(side=RIGHT, before=self.canvas, ipadx=3, ipady=5)

        # self.capture_button = tk.Button(master, text="Capture", command=self.capture)
        # self.capture_button.pack(side="bottom")
        # self.next_button = tk.Button(master, text="Next Page", command=self.mosaic_image)
        # self.next_button.pack(side=RIGHT)
        # 클릭 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.on_click)

    def capture(self):
        # 스크린샷 저장 위치 선택
        filename = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")])
        
        self.original_image.save(filename)
        toast = ToastNotification(
                title="모자이크에크",
                message="이미지가 정상적으로 저장되었습니다.",
                duration=5000,
            )
        toast.show_toast()
        self.mosaic_image()

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

        


if __name__ == '__main__':

    root = ttk.Window("MosaIcEc", "morph")
    app = Mosaic(root)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 윈도우 크기를 설정합니다.
    window_width = int(screen_width * 0.8) # 모니터 가로 크기의 80%로 설정
    window_height = int(screen_height * 1) # 모니터 세로 크기의 80%로 설정

    root.geometry(f"{window_width}x{window_height}")
    root.mainloop()

