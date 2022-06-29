from ntpath import join
from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import json
import io 
from os import listdir
import numpy as np
import base64
from secrets import secrets

db_pass = secrets.get('DB_PASSWORD', 'pass')

class Photos:
    def __init__(self,root):
        self.root= root
        self.root.geometry("1530x790+0+0")
        self.root.title("Photos")

        script_dir = os.path.dirname(__file__)
        img= Image.open(os.path.join(script_dir, "images\\photos_bg.jpg"))
        img= img.resize((1400,750), Image.LANCZOS)
        self.photoimg= ImageTk.PhotoImage(img)

        bg_img= Label(self.root, image= self.photoimg)  
        bg_img.place(x=0,y=0,width=1400,height=750)

        b1= Button(bg_img, text="Images", cursor="hand2", command= self.open_img, font=("times new roman",25,"bold"), bg="#2F8F9D", fg="white")
        b1.place(x=400, y=250, width=630, height=50)

        b2= Button(bg_img, text="Parse JSON File into Database", cursor="hand2", command= self.parse_json, font=("times new roman",25,"bold"), bg="#2F8F9D", fg="white")
        b2.place(x=400, y=350, width=630, height=50)

        b3= Button(bg_img, text="Generate Images from Database",  cursor="hand2", command= self.upload_img, font=("times new roman",25,"bold"), bg="#2F8F9D", fg="white")
        b3.place(x=400, y=450, width=630, height=50)

    def open_img(self):
        os.startfile("data")

    def parse_json(self):
        with open('Photo Data Excel.json', 'r') as json_file:
            json_load= json.load(json_file)

        for entry in json_load['Sheet1']:
            if entry['PID']=="" or entry['Name']== "":
                messagebox.showerror("Error", "All fields are required", parent= self.root)
            else:
                try:
                    conn= mysql.connector.connect(host="localhost", username="root", password= db_pass, database="face_recognition")
                    my_cursor= conn.cursor()
                    img= entry['Photo']
                    img = base64.b64decode(img)
                    my_cursor.execute("insert into details values(%s,%s,%s,%s,%s,%s)", (
                                                                                    entry['PID'],
                                                                                    entry['Name'],
                                                                                    "NULL",
                                                                                    "NULL",
                                                                                    "NULL",
                                                                                    img
                                                                                    ))
                    conn.commit() 
                    conn.close() 
                except Exception as es:
                    print("Errors", f"Due to : {str(es)}")                                                                                                                                                             
        json_file.close()

    def upload_img(self):
        conn= mysql.connector.connect(host="localhost", username="root", password= db_pass, database="face_recognition")
        my_cursor= conn.cursor()
        my_cursor.execute("select * from details")
        users= my_cursor.fetchall()

        for user in users:
            byte_data= user[5]
            img = Image.open(io.BytesIO(byte_data))
            img = np.array(img)
            img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #img.show()
            file_name_path= "data/user."+ str(user[0]) +".jpg"
            cv2.imwrite(file_name_path, img)

if __name__ == "__main__":
    root= Tk()
    obj= Photos(root)
    root.mainloop()