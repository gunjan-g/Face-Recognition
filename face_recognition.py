from ntpath import join
from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from cv2 import cvtColor, putText
import cv2
import os
import io 
from os import listdir
import base64
import numpy as np
from deepface import DeepFace
import matplotlib.pyplot as plt

class Face_Recognition:
    def __init__(self,root):    #constructor
        self.root= root
        self.root.geometry("1530x790+0+0")   #size of window
        self.root.title("Face Detection and Recognition")

        #title
        title_lbl= Label(self.root, text="Face Recognition", font= ("Comic Sans MS", 35, "bold"), bg="white", fg="#82DBD8")
        title_lbl.place(x=0, y=0, width=1400, height=70)

        script_dir = os.path.dirname(__file__)
        img= Image.open(os.path.join(script_dir, "images\\face_recognition.jpg"))
        img= img.resize((1400,640), Image.LANCZOS)
        self.photoimg= ImageTk.PhotoImage(img)

        bg_img= Label(self.root, image= self.photoimg)  
        bg_img.place(x=0,y=70,width=1400,height=640)

        b1= Button(bg_img, text="Start", cursor="hand2", command= self.face_recog, font=("times new roman",25,"bold"), bg="#2F8F9D", fg="white")
        b1.place(x=200, y=280, width=130, height=50)

    def face_recog(self):
        script_dir = os.path.dirname(__file__)
        db_path= os.path.join(script_dir + "\data")
        cap = cv2.VideoCapture(0)

        # Check if the webcam is opened correctly
        if not cap.isOpened():
            raise IOError("Cannot open webcam")

        print("Scanning Face...")
        frame = cap.read()[1]
        img= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('img.jpg',img)
        cap.release()
        cv2.destroyAllWindows()
        print("Face Scan Complete")

        found= 0
        model_name= "VGG-Face"
        model = DeepFace.build_model(model_name) 

        for images in os.listdir(db_path):
            try:
                if DeepFace.verify(img, images, model_name, enforce_detection=False)['verified']:
                    found =1
                    messagebox.showinfo("Found", "The suspect is present in database", parent= self.root)
                    break
                if found == 1:
                    break
            except ValueError: 
                pass
        print("Recognition done")

        if found == 0:
            messagebox.showinfo("Not found", "The suspect is not present in database", parent= self.root)

        #df = DeepFace.find(img, db_path, model_name = "VGG-Face", enforce_detection=False)
        #print(df)

if __name__ == "__main__":
    root= Tk()
    obj= Face_Recognition(root)
    root.mainloop()