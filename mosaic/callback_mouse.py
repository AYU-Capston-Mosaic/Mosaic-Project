import cv2
import tkinter as tk
from PIL import Image
from PIL import ImageTk

result = []

class MyWidgets(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        global result

        super().__init__(parent, *args, **kwargs)
        canvas = tk.Canvas(self, bg="black") 
        self.src = cv2.imread('./img/0.jpg')
        img_w, img_h, img_a = self.src.shape # image size(height, width, alpha)
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
            
        imgtk = ImageTk.PhotoImage(image=img, master=self)

        self.label = tk.Label(self, image=imgtk)
        self.label.image = imgtk #class 내에서 작업할 경우에는 이 부분을 넣어야 보인다.
        self.label.pack(side="top")
        
        # self.scrollbar = tk.Scrollbar(self)
        # self.scrollbar.pack(side="left", fill="both")

        self.label.config(image=imgtk)
        self.label.image = imgtk
        

def callback_mouse(event): 
    global result

    # self.canvas = tk.Canvas(self)
    # self.canvas.pack(expand=True, fill='both')
    input_x, input_y = event.x,event.y
    print(event.x,event.y)
    for i in result:
        x = i[0][0][0] 
        y = i[0][0][1] 
        w = i[0][1][0]
        h = i[0][2][1]
        if x <= input_x <= w and y <= input_y <= h:
            print('true')
            # canvas.create_polygon(x, y, w, y, w, h, x, h, fill="blue")
    # return input_x, input_y

class MainApp(tk.Tk):
    """Application root window"""

        # canvas.delete("all") 
        # shapes = canvas.create_polygon(event.x, event.y, event.x+15, event.y, event.x+15, event.y+15, event.x, event.y+15, fill="black")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Mouse Events")
        self.resizable(width=True, height=True)

        self.widgetform = MyWidgets(self)
        self.widgetform.grid(row=3, padx=10, sticky=(tk.W + tk.E))      
        self.bind("<Button-1>", callback_mouse) 
        # self.geometry("640x480")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()