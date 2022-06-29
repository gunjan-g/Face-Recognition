from tkinter import*
from tkinter import ttk
import tkinter
from PIL import Image, ImageTk
from details import Details
from face_recognition import Face_Recognition
from photos import Photos
import os

class Face_Recognition_System:
    def __init__(self,root):    #constructor
        self.root= root
        self.root.geometry("1530x790+0+0")   #size of window
        self.root.title("Face Recognition System")

        script_dir = os.path.dirname(__file__)
        img_path= "images\\background.jpg"
        img= Image.open(os.path.join(script_dir, img_path))
        img= img.resize((1400,800), Image.LANCZOS)
        self.photoimg= ImageTk.PhotoImage(img)

        #background image
        bg_img= Label(self.root, image= self.photoimg)  
        bg_img.place(x=0,y=0,width=1400,height=800)

        #title
        title_lbl= Label(bg_img, text="FACE RECOGNITION SOFTWARE", font= ("Comic Sans MS", 35, "bold"), bg="white", fg="#2F8F9D")
        title_lbl.place(x=0, y=40, width=1400, height=70)
        
        #Button1
        img1= Image.open(os.path.join(script_dir, "images\\details.jpg"))
        img1= img1.resize((230,220), Image.LANCZOS)
        self.photoimg1= ImageTk.PhotoImage(img1)
        b1= Button(bg_img, image=self.photoimg1, cursor="hand2", command= self.details_func)
        b1.place(x=100, y=260, width=230, height=220)

        b1_1= Button(bg_img, text="Details",  cursor="hand2", command= self.details_func, font=("times new roman", 15, "bold"), bg="#2F8F9D", fg="white")
        b1_1.place(x=100, y=480, width=230, height=40)

        #Button2
        img2= Image.open(os.path.join(script_dir, "images\\face_detector.jpg"))
        img2= img2.resize((230,220), Image.LANCZOS)
        self.photoimg2= ImageTk.PhotoImage(img2)
        b2= Button(bg_img, image=self.photoimg2, cursor="hand2", command= self.face_recognition_func)
        b2.place(x=400, y=260, width=230, height=220)

        b2_1= Button(bg_img, text="Face Detector", cursor="hand2", command= self.face_recognition_func, font=("times new roman", 15, "bold"), bg="#2F8F9D", fg="white")
        b2_1.place(x=400, y=480, width=230, height=40)

        #Button3
        img3= Image.open(os.path.join(script_dir, "images\\photos.jpg"))
        img3= img3.resize((230,220), Image.LANCZOS)
        self.photoimg3= ImageTk.PhotoImage(img3)
        b3= Button(bg_img, image=self.photoimg3, cursor="hand2", command= self.open_img)
        b3.place(x=700, y=260, width=230, height=220)

        b3_1= Button(bg_img, text="Photos", cursor="hand2", command= self.open_img, font=("times new roman", 15, "bold"), bg="#2F8F9D", fg="white")
        b3_1.place(x=700, y=480, width=230, height=40)

        #Button2
        img4= Image.open(os.path.join(script_dir, "images\\exit.jpg"))
        img4= img4.resize((230,220), Image.LANCZOS)
        self.photoimg4= ImageTk.PhotoImage(img4)
        b4= Button(bg_img, image=self.photoimg4, cursor="hand2", command= self.iExit)
        b4.place(x=1000, y=260, width=230, height=220)

        b4_1= Button(bg_img, text="Exit", cursor="hand2", command=self.iExit, font=("times new roman", 15, "bold"), bg="#2F8F9D", fg="white")
        b4_1.place(x=1000, y=480, width=230, height=40)

     # Functions  
    def details_func(self):
        self.new_window= Toplevel(self.root)
        self.app= Details(self.new_window)

    def face_recognition_func(self):
        self.new_window= Toplevel(self.root)
        self.app= Face_Recognition(self.new_window)

    def open_img(self):
        self.new_window= Toplevel(self.root)
        self.app= Photos(self.new_window)

    def iExit(self):
        self.iExit= tkinter.messagebox.askyesno("Face Recognition System", "Are you sure you want to exit this project", parent= self.root)
        if self.iExit>0:
            self.root.destroy()
        else:
            return

if __name__ == "__main__":
    root= Tk()
    obj= Face_Recognition_System(root)
    root.mainloop()