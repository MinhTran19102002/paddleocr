from paddleocr import PaddleOCR,draw_ocr
from PIL import Image
import cv2

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image


def select_image():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")])

    # Cat hinh anh trong khung
    img1=cv2.imread(file_path)
    #Img To Gray
    img_gray=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img_gray =  cv2.bilateralFilter(img_gray, 11,17,17)

    edged = cv2.Canny(img_gray, 190, 200)
    contours , new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
    contour_license_plate = None
    license_plate = None
    w= None
    h = None
    x= None
    y = None
    res = ''
    for contour in contours:
        perimeter =  cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018* perimeter, True)
        if len(approx) == 4:
            print('-----------')
            contour_license_plate = approx
            x,y,w,h = cv2.boundingRect(contour_license_plate)
            print(x, y, w, h)
            license_plate = img_gray[y: y+h, x:x+w]
            # cv2.imshow("Result2",license_plate)
            ocr = PaddleOCR(use_angle_cls=True, lang='en')
            result = ocr.ocr(license_plate, cls=True)
            res = result[0]
            # txts = [line[1][0] for line in res]
            if(res):
                break
    if res:
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
        
        result = ocr.ocr(license_plate, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                print(line)


        result = result[0]

        img = Image.open(file_path).convert('RGB')

        
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        # scores = [line[1][1] for line in result]

        for line in result:
            if len(line[1][0]) == 10:
                print(line[1][0])
        im_show = draw_ocr(img, boxes)
        im_show = Image.fromarray(im_show)

        im_show = im_show.resize((300, 300))  # Thay đổi kích thước hình ảnh
        im_show = ImageTk.PhotoImage(im_show)

        image_label.config(image=im_show)
        image_label.image = im_show 
        license_text = ''
        if(len(txts)==2):
            license_text= txts[0]+ '-' + txts[1]
        if(len(txts)==1):
            license_text= txts[0]
        license_text = license_text.replace(".", "")
        license_label.config(text= license_text) 
    elif file_path:
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
        
        result = ocr.ocr(file_path, cls=True)
        print(len(result))
        for idx in range(len(result)):
            res = result[idx]
            print(res)
            for line in res:
                print(line)


        result = result[0]

        img = Image.open(file_path).convert('RGB')

        
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        # scores = [line[1][1] for line in result]

        for line in result:
            if len(line[1][0]) == 10:
                print(line[1][0])
        im_show = draw_ocr(img, boxes)
        im_show = Image.fromarray(im_show)

        im_show = im_show.resize((300, 300))  # Thay đổi kích thước hình ảnh
        im_show = ImageTk.PhotoImage(im_show)

        image_label.config(image=im_show)
        image_label.image = im_show 
        license_text = ''
        if(len(txts)==2):
            license_text= txts[0]+ '-' + txts[1]
        if(len(txts)==1):
            license_text= txts[0]
        license_text = license_text.replace(".", "")
        license_label.config(text= license_text)
        
        



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")

    root.rowconfigure(1, minsize=400)
    root.rowconfigure(3, minsize=100)

    tk.Label(root, text='Xuat nhap xe', fg='red', font=('cambria', 16), width=40).grid(row=0)
    frame1 = tk.Frame(root, bd=2, relief=tk.SOLID, width=600, height=400)
    frame1.grid(pady=20, padx=20,row=1, column=0, sticky="nsew") 
    # listbox = tk.Frame(root, width=90, height=20)
    # listbox.grid(row=1, columnspan=2)
    tk.Button(root, text="Open Image", command=select_image).grid(row=2, pady=20, padx=20)
    # button.pack()

    image_label = tk.Label(frame1)
    image_label.pack(side="left")

    frame2 = tk.Frame(root, bd=1, relief=tk.SOLID, width=600, height=400)
    frame2.grid(row=3, column=0, sticky="nsew", pady=20, padx=20) 
    license_label = tk.Label(frame2)
    license_label.pack(side="left")

    button1 = tk.Button(frame2, text="Nhap xe vao bai")
    button1.pack(side="right")

    root.mainloop()


# # draw result
# from PIL import Image
# result = result[0]
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path='./Aaargh.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')