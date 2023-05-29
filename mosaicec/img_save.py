import tkinter.filedialog as filedialog
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification

def main(self):
    filename = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")])
    
    self.original_image.save(filename)
    toast = ToastNotification(
            title="모자이크에크",
            message="이미지가 정상적으로 저장되었습니다.",
            duration=10000,
        )
    toast.show_toast()