from dataclasses import dataclass
from msilib import add_data
from sqlite3 import paramstyle
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
from secrets import secrets
from requests import delete

db_pass = secrets.get('DB_PASSWORD', 'pass')

class Details:
    def __init__(self,root):
        self.root= root
        self.root.geometry("1530x790+0+0")
        self.root.title("Details")

        # Variable Declaration
        self.var_id= StringVar()
        self.var_name= StringVar()
        self.var_age= StringVar()
        self.var_gender= StringVar()

        script_dir = os.path.dirname(__file__)
        img_path= "images\\commonbg.jpg"
        img= Image.open(os.path.join(script_dir, img_path))
        img= img.resize((1400,800), Image.LANCZOS)
        self.photoimg= ImageTk.PhotoImage(img)

        # Background image
        bg_img= Label(self.root, image= self.photoimg)  
        bg_img.place(x=0,y=0,width=1400,height=800)

        #title
        title_lbl= Label(bg_img, text="DETAILS", font= ("Comic Sans MS", 35, "bold"), bg="white", fg="#82DBD8")
        title_lbl.place(x=0, y=40, width=1400, height=70)

        main_frame= Frame(bg_img, bd=2)  # bd is border
        main_frame.place(x=25, y=155, width= 1300, height=500)

        # Left Frame
        Left_frame= LabelFrame(main_frame, bd=2, relief=RIDGE, text="Submit Details", font= ("times new roman",12,"bold"))
        Left_frame.place(x=15, y=10, width= 620, height=463)

        img_path= "images\\enter_details.jpg"
        img_left= Image.open(os.path.join(script_dir, img_path))
        img_left= img_left.resize((250,415), Image.LANCZOS)
        self.photoimgleft= ImageTk.PhotoImage(img_left)

        # Left frame image
        bg_img_left= Label(Left_frame, image= self.photoimgleft)
        bg_img_left.place(x=15, y=10, width=250, height=415)
        
        # Left sub frame 
        Left_sub_frame1= LabelFrame(Left_frame, bd=0, bg="white")
        Left_sub_frame1.place(x=265, y=10, width=340, height=415)

        Left_sub_frame2= LabelFrame(Left_frame, bd=2, bg="white")
        Left_sub_frame2.place(x=275, y=25, width=315, height=385)

        #Buttons
        id_label= Label(Left_sub_frame2, text=" Enter ID: ", font=("times new roman", 13, "bold"), bg="white")
        id_label.grid(row=0, column=0, padx=1, pady=10, sticky=W)
        id_entry= ttk.Entry(Left_sub_frame2, textvariable= self.var_id, width=18, font=("times new roman", 13,))
        id_entry.grid(row=0, column=1, padx=0, pady=10, sticky=W)

        name_label= Label(Left_sub_frame2, text=" Enter Name: ", font=("times new roman", 13, "bold"), bg="white")
        name_label.grid(row=1, column=0, padx=1, pady=8, sticky=W)
        name_entry= ttk.Entry(Left_sub_frame2, textvariable= self.var_name, width=18, font=("times new roman", 13))
        name_entry.grid(row=1, column=1, padx=0, pady=8, sticky=W)

        age_label= Label(Left_sub_frame2, text=" Enter Age: ", font=("times new roman", 13, "bold"), bg="white")
        age_label.grid(row=2, column=0, padx=1, pady=8, sticky=W)
        age_entry= ttk.Entry(Left_sub_frame2, textvariable= self.var_age, width=18, font=("times new roman", 13))
        age_entry.grid(row=2, column=1, padx=0, pady=8, sticky=W)

        gender_label= Label(Left_sub_frame2, text=" Select Gender: ", font=("times new roman", 13, "bold"), bg="white")
        gender_label.grid(row=3, column=0, padx=1, pady=8, sticky=W)
        gender_combo= ttk.Combobox(Left_sub_frame2, textvariable= self.var_gender, font=("times new roman",13), state="readonly", width=16)
        gender_combo["values"]= ("Select", "Male", "Female", "Non-binary", "Transgender")
        gender_combo.current(0)
        gender_combo.grid(row=3, column=1, padx=1, pady=8, sticky=W)

        # Button Frame
        btn_frame= Frame(Left_sub_frame2, bd=2, relief=RIDGE)
        btn_frame.place(x=2, y=312, width= 305, height= 64)

        save_btn= Button(btn_frame, text="Save", command=self.add_data, width=16, font=("times new roman", 13), bg="#2F8F9D", fg="white")
        save_btn.grid(row=0, column=0)

        update_btn= Button(btn_frame, text="Update", command=self.update_data, width=16, font=("times new roman", 13), bg="#2F8F9D", fg="white")
        update_btn.grid(row=0, column=1)

        del_btn= Button(btn_frame, text="Delete", command=self.delete_data, width=16, font=("times new roman", 13), bg="#2F8F9D", fg="white")
        del_btn.grid(row=1, column=0)

        reset_btn= Button(btn_frame, text="Reset", command= self.reset_data, width=16, font=("times new roman", 13), bg="#2F8F9D", fg="white")
        reset_btn.grid(row=1, column=1)

        # Right Frame
        Right_frame= LabelFrame(main_frame, bd=2, relief=RIDGE, font= ("times new roman",12,"bold"))
        Right_frame.place(x=655, y=10, width= 620, height=463)

        img_path= "images\\information.jpg"
        img_right= Image.open(os.path.join(script_dir, img_path))
        img_right= img_right.resize((602,125), Image.LANCZOS)
        self.photoimgright= ImageTk.PhotoImage(img_right)

        # Right frame image
        bg_img_right= Label(Right_frame, image= self.photoimgright)
        bg_img_right.place(x=7, y=5, width=602, height=125)

        # Table frame
        table_frame= Frame(Right_frame, bd=2, relief=RIDGE)
        table_frame.place(x=7, y=135, width= 602, height= 315)

        scroll_x= ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y= ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.info_table= ttk.Treeview(table_frame, column= ("id", "name", "age", "gender"), xscrollcommand= scroll_x.set, yscrollcommand= scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command= self.info_table.xview)
        scroll_y.config(command= self.info_table.yview)

        self.info_table.heading("id", text="ID")
        self.info_table.heading("name", text="Name")
        self.info_table.heading("age", text="Age")
        self.info_table.heading("gender", text="Gender")
        self.info_table["show"]= "headings"

        self.info_table.column("id", width=100)
        self.info_table.column("name", width=150)
        self.info_table.column("age", width=70)
        self.info_table.column("gender", width=100)
        #self.info_table.column("photo", width=150)

        self.info_table.pack(fill= BOTH, expand=1)
        self.info_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

    # Add details
    def add_data(self):
        if self.var_id.get()=="" or self.var_name=="":
            messagebox.showerror("Error", "All fields are required", parent= self.root)
        else:
            try:
                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

                def face_cropped_func(img):
                    gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces= face_classifier.detectMultiScale(gray, 1.3, 5)

                    for(x,y,w,h) in faces:
                        face_cropped= img[y:y+h, x:x+w]
                        return face_cropped

                conn= mysql.connector.connect(host="localhost", username="root", password= db_pass, database="face_recognition")
                my_cursor= conn.cursor()
                cap = cv2.VideoCapture(0)

                # Check if the webcam is opened correctly
                if not cap.isOpened():
                    raise IOError("Cannot open webcam")

                frame = cap.read()[1]
                face= cv2.resize(face_cropped_func(frame), (450,450))
                img_str = cv2.imencode('.jpg', face)[1].tobytes()
                my_cursor.execute("insert into details values(%s,%s,%s,%s,%s)", (
                                                                                    self.var_id.get(),
                                                                                    self.var_name.get(),
                                                                                    self.var_age.get(),
                                                                                    self.var_gender.get(),
                                                                                    img_str
                                                                                    ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                messagebox.showinfo("Success", "Details have been added successfully", parent= self.root)
            except Exception as es:
                messagebox.showerror("Errors", f"Due to : {str(es)}", parent= self.root)

   # Fetch all details from database
    def fetch_data(self):
        conn= mysql.connector.connect(host="localhost", username="root", password= db_pass, database="face_recognition")
        my_cursor= conn.cursor()
        my_cursor.execute("select * from details")
        data= my_cursor.fetchall()      

        if len(data)!=0:
            self.info_table.delete(*self.info_table.get_children())
            for i in data:
                self.info_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    # Set data
    def get_cursor(self, event=""):
        cursor_focus= self.info_table.focus()
        content= self.info_table.item(cursor_focus)
        data= content["values"]

        self.var_id.set(data[0]),
        self.var_name.set(data[1]),
        self.var_age.set(data[2]),
        self.var_gender.set(data[3]),

    # Update data
    def update_data(self):
        if self.var_id.get()=="" or self.var_name=="":
            messagebox.showerror("Error", "All fields are required", parent= self.root)
        else:
            try:
                update_ans= messagebox.askyesno("Update", "Do you want to update this user details", parent= self.root)
                if update_ans>0:
                    conn= mysql.connector.connect(host="localhost", username="root", password= db_pass, database="face_recognition")
                    my_cursor= conn.cursor()
                    my_cursor.execute("update details set User_Name= %s, User_Age= %s, User_Gender= %s, where User_ID= %s", (
                                                                                                                                                                    self.var_name.get(),
                                                                                                                                                                    self.var_age.get(),
                                                                                                                                                                    self.var_gender.get(),
                                                                                                                                                                    self.var_crime.get(),
                                                                                                                                                                    self.var_id.get(),
                                                                                                                                                               ))
                else:
                    if not update_ans:
                        return
                messagebox.showinfo("Updated", "Details successfully updated", parent= self.root)
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Errors", f"Due to : {str(es)}", parent= self.root)

    # Delete data
    def delete_data(self):
        if self.var_id.get()=="":
            messagebox.showerror("Error", "User ID is required", parent= self.root)
        else:
            try:
                delete_ans= messagebox.askyesno("Delete", "Do you want to delete this user details", parent= self.root)
                if delete_ans>0:
                    conn= mysql.connector.connect(host="localhost", username="root", password= db_pass, database="face_recognition")
                    my_cursor= conn.cursor()
                    sql ="delete from details where User_ID= %s"
                    val= (self.var_id.get(),)
                    my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Deleted", "Successfully deleted user details", parent= self.root)
            except Exception as es:
                messagebox.showerror("Errors", f"Due to : {str(es)}", parent= self.root)
    
    # Reset data
    def reset_data(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_age.set("")
        self.var_gender.set("Select")

if __name__ == "__main__":
    root= Tk()
    obj= Details(root)
    root.mainloop()