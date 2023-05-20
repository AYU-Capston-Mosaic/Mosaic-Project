import tkinter as tk
import cv2
from pathlib import Path
from PIL import Image, ImageTk, ImageDraw
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification

import file_select as sf
import img_load as il
import img_mosaic as im
import img_save as ims

PATH = Path(__file__).parent / 'assets'

class Mosaic(ttk.Frame):

    def radio_select(self):
        self.progress = self.radio_selected.get()
        self.setvar('progress', self.progress)
        self.img_name = self.progress
        il.main(self)
    
    def on_click(self, event):
        if (not self.bbox): return

        # 클릭된 위치 계산
        input_x, input_y = event.x, event.y

        wt_scrollbar_position = self.all_wt_scrollbar.get()  
        ht_scrollbar_position = self.all_ht_scrollbar.get()  
        
        # self.src.shape = (height, width)
        input_x = event.x  + (self.src.shape[1] * ht_scrollbar_position[0])
        input_y = event.y  + (self.src.shape[0] * wt_scrollbar_position[0])

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


    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=BOTH, expand=True)

        self.imglist = [] # 이미지 리스트
        self.bbox = []
        self.progress = '선택된 파일이 없습니다.'
        self.radio_selected = tk.StringVar()

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
                name='save',
                file=PATH / 'save.png')
        ]

        # header
        hdr_frame = ttk.Frame(self, padding=20, bootstyle=DARK)
        # hdr_frame.grid(row=0, column=0, columnspan=3, sticky=EW)
        hdr_frame.pack(side=TOP, anchor='nw', fill=X, expand=True)

        hdr_label = ttk.Label(
            master=hdr_frame,
            image='logo',
            bootstyle=(INVERSE, DARK)
        )
        hdr_label.pack(side=LEFT)

        logo_text = ttk.Label(
            master=hdr_frame,
            text='모자이크에크',
            font=('TkDefaultFixed', 30),
            bootstyle=(INVERSE, DARK)
        )
        logo_text.pack(side=LEFT, padx=10)

        # action buttons
        action_frame = ttk.Frame(self)
        action_frame.pack(side=LEFT, anchor='nw', fill=BOTH, expand=True)

        cleaner_btn = ttk.Button(
            master=action_frame,
            image='file',
            text='파일 선택하기',
            compound=TOP,
            bootstyle=INFO,
            command=lambda: sf.main(self)
        )
        cleaner_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=40)

        registry_btn = ttk.Button(
            master=action_frame,
            image='mosaic',
            text='모자이크 진행하기',
            compound=TOP,
            bootstyle=INFO,
            command=lambda: im.main(self)
        )
        registry_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=40)

        tools_btn = ttk.Button(
            master=action_frame,
            image='save',
            text='파일로 저장하기',
            compound=TOP,
            bootstyle=INFO,
            command=lambda: ims.main(self)
        )
        tools_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=40)

        # option notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side=LEFT, anchor='nw', fill=BOTH, expand=True, padx=10, pady=10)

        # windows tab
        self.windows_tab = ttk.Frame(self.notebook, padding=10)
        wt_scrollbar = ttk.Scrollbar(self.windows_tab)
        wt_scrollbar.pack(side=RIGHT, fill=Y)
        wt_scrollbar.set(0, 1)
        ht_scrollbar = ttk.Scrollbar(self.windows_tab, orient="horizontal")
        ht_scrollbar.pack(side=BOTTOM, fill=X)
        ht_scrollbar.set(0, 1)

        self.wt_canvas = ttk.Canvas(
            master=self.windows_tab,
            relief=FLAT,
            borderwidth=0,
            selectborderwidth=0,
            highlightthickness=0,
            xscrollcommand=ht_scrollbar.set,
            yscrollcommand=wt_scrollbar.set
        )
        self.wt_canvas.pack(side=LEFT, fill=BOTH)

        # adjust the scrollregion when the size of the canvas changes
        self.wt_canvas.bind(
            sequence='<Configure>',
            func=lambda e: self.wt_canvas.configure(
                scrollregion=self.wt_canvas.bbox(ALL))
        )
        wt_scrollbar.configure(command=self.wt_canvas.yview)
        ht_scrollbar.configure(command=self.wt_canvas.xview)
        self.scroll_frame = ttk.Frame(self.wt_canvas)
        self.wt_canvas.create_window((0, 0), window=self.scroll_frame, anchor=NW)

        for opt in self.imglist:
            cb = ttk.Checkbutton(self.scroll_frame, text=opt, state='deselected')
            cb.invoke()
            cb.pack(side=TOP, pady=2, fill=X)
        self.notebook.add(self.windows_tab, text='변환 파일 목록')

        # results frame
        results_frame = ttk.Frame(self)
        results_frame.pack(side=LEFT, anchor='nw', fill=BOTH, expand=True)

        # selected file with text indicator
        pb_frame = ttk.Frame(results_frame, padding=10)
        pb_frame.pack(side=TOP, fill=X, expand=YES)

        pb_edge = ttk.Labelframe(
            master=results_frame,
            text='현재 선택된 파일',
            bootstyle="info",
            padding=(20, 5)
        )
        pb_edge.pack(fill=BOTH, expand=YES, padx=20, pady=10) 

        ttk.Label(pb_edge, bootstyle="inverse-info", textvariable='progress').pack(side=RIGHT)
        self.setvar('progress', self.progress)

        # result cards
        self.cards_frame = ttk.Frame(
            master=results_frame,
            name='cards-frame',
            bootstyle=SECONDARY,
        )
        self.cards_frame.pack(fill=BOTH, expand=YES)

        self.img_name = './assets/default.png'
        self.src = cv2.imread(self.img_name)
        img_w, img_h, img_a = self.src.shape # image size(height, width, alpha)

        self.all_wt_scrollbar = ttk.Scrollbar(self.cards_frame)
        self.all_wt_scrollbar.pack(side=RIGHT, fill=Y)
        self.all_wt_scrollbar.set(0, 1)
        self.all_ht_scrollbar = ttk.Scrollbar(self.cards_frame, orient="horizontal")
        self.all_ht_scrollbar.pack(side=BOTTOM, fill=X)
        self.all_ht_scrollbar.set(0, 1)

        # self.master = master
        self.canvas = tk.Canvas(self.cards_frame, 
                                width=int(img_w * 0.6), 
                                height=int(img_h * 1.2),
                                xscrollcommand=self.all_ht_scrollbar.set,
                                yscrollcommand=self.all_wt_scrollbar.set)
        self.canvas.pack()


        self.src = cv2.resize(self.src, (int(img_w * 0.6), int(img_h * 1.2)))  
        img = Image.fromarray(self.src)    # 이미지에 그리기 위해서 CV2 이미지를 PIL 이미지 객체로 변환
        self.original_image = Image.fromarray(self.src)

        self.image = img
        self.image_tk = ImageTk.PhotoImage(self.image)

        # 이미지를 Canvas 위젯에 배치
        self.img_id = self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

        self.canvas.bind("<Button-1>", self.on_click)

        # adjust the scrollregion when the size of the canvas changes
        self.canvas.bind(
            sequence='<Configure>',
            func=lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox(ALL))
        )
        self.all_wt_scrollbar.configure(command=self.canvas.yview)
        self.all_ht_scrollbar.configure(command=self.canvas.xview)
        all_scroll_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=all_scroll_frame, anchor=NW)


if __name__ == '__main__':
    root = ttk.Window("MosaIcEc", "morph")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 윈도우 크기 설정
    window_width = int(screen_width * 1) 
    window_height = int(screen_height * 1)

    root.geometry(f"{window_width}x{window_height}")
    app = Mosaic(root)
    root.mainloop()
