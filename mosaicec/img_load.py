import cv2
from PIL import Image, ImageTk

def main(self):
    self.canvas.delete(self.img_id)

    self.src = cv2.imread(self.img_name)
    img_w, img_h, img_a = self.src.shape # image size(height, width, alpha)

    self.src = cv2.resize(self.src, (int(img_w * 0.6), int(img_h * 1.2)), Image.ANTIALIAS)
    
    print(self.img_name)
    
    img = Image.fromarray(self.src)    # 이미지에 그리기 위해서 CV2 이미지를 PIL 이미지 객체로 변환
    self.original_image = Image.fromarray(self.src)
    
    self.image = img
    self.image_tk = ImageTk.PhotoImage(self.image)

    # 이미지를 Canvas 위젯에 배치
    self.img_id = self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)
    

