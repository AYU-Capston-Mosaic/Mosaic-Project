import tempfile
from pathlib import Path
from pdf2image import convert_from_path
import os
import tkinter.filedialog as filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification

PATH = Path(__file__).parent / 'assets'

def main(self):
    self.imglist = []
    self.bbox = []

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
        self.imglist.append(image_name)
        page.save(image_name, "JPEG")

    self.scroll_frame = ttk.Frame(self.wt_canvas)
    self.wt_canvas.create_window((0, 0), window=self.scroll_frame, anchor=NW)

    for opt in self.imglist:
        cb = ttk.Checkbutton(self.scroll_frame, text=opt, state='deselected')
        cb.invoke()
        cb = ttk.Radiobutton(self.scroll_frame, text=opt, variable=self.radio_selected, value=opt, command=self.radio_select)
        cb.pack(side=TOP, pady=2, fill=X)
    self.notebook.add(self.windows_tab, text='변환 파일 목록')

