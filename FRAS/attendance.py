# import re
import re
from sys import path
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
import os
import mysql.connector as sq
import cv2
import numpy as np
from tkinter import messagebox
from time import strftime
from datetime import datetime
import csv
from tkinter import filedialog
import pandas as pd
from datetime import date
from datetime import datetime

#Global variable for importCsv Function 
mydata=[]

class Attendance:
    
    def __init__(self,root):
        self.root=root
        self.root.geometry("1366x768+0+0")
        self.root.title("Attendance Pannel")

        #-----------Variables-------------------
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_status=StringVar()
        self.var_date=StringVar()
        self.var_subject=StringVar()


        # This part is image labels setting start 
        # first header image  
        img=Image.open(r"Images_GUI\banner.jpg")
        img=img.resize((1366,130),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=1366,height=130)

        # backgorund image 
        bg1=Image.open(r"Images_GUI\bg2.jpg")
        bg1=bg1.resize((1366,768),Image.ANTIALIAS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=1366,height=768)


        #title section
        title_lb1 = Label(bg_img,text="Welcome to Attendance Management Panel",font=("verdana",30,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=1366,height=45)

        #========================Section Creating==================================

        # Creating Frame 
        main_frame = Frame(bg_img,bd=2,bg="white") #bd mean border 
        main_frame.place(x=250,y=55,width=850,height=510)

        # Left Label Frame 
        left_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Details",font=("verdana",12,"bold"),fg="navyblue")
        left_frame.place(x=10,y=10,width=850,height=480)

        

        # ==================================Text boxes and Combo Boxes====================

        #Student Roll

        #Studnet Name

        sub_combo=ttk.Combobox(left_frame,textvariable=self.var_subject,width=15,font=("verdana",12,"bold"),state="readonly")
        sub_combo["values"]=("Select Subject","SE Economics","Arabic","NLP","Topics in SE")
        sub_combo.current(0)
        sub_combo.grid(row=0,column=1,padx=5,pady=15,sticky=W)

        #Department
        # dep_label = Label(left_frame,text="Department:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        # dep_label.grid(row=1,column=2,padx=5,pady=5,sticky=W)

        # dep_entry = ttk.Entry(left_frame,textvariable=self.var_dep,width=15,font=("verdana",12,"bold"))
        # dep_entry.grid(row=1,column=3,padx=5,pady=5,sticky=W)

        #Date 
        # ===============================Table Sql Data View==========================
        table_frame = Frame(left_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=10,y=100,width=780,height=310)
        #scroll bar 
        scroll_x = ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame,orient=VERTICAL)
        #create table 
        self.attendanceReport_left = ttk.Treeview(table_frame,column=("Name","Status","Date","Subject"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.attendanceReport_left.xview)
        scroll_y.config(command=self.attendanceReport_left.yview)
        #self.attendanceReport_left.heading("Roll_No",text="Roll.No")
        self.attendanceReport_left.heading("Name",text="Std-Name")
        self.attendanceReport_left.heading("Status",text="status")
        self.attendanceReport_left.heading("Date",text="date")
        self.attendanceReport_left.heading("Subject",text="subject")

        self.attendanceReport_left["show"]="headings"


        # Set Width of Colums 
        
        #self.attendanceReport_left.column("Roll_No",width=100)
        self.attendanceReport_left.column("Name",width=100)
        self.attendanceReport_left.column("Status",width=100)
        self.attendanceReport_left.column("Date",width=100)
        self.attendanceReport_left.column("Subject",width=100)
        self.attendanceReport_left.pack(fill=BOTH,expand=1)
        self.attendanceReport_left.bind("<ButtonRelease>")
    

        # =========================button section========================

        #Button Frame
        btn_frame = Frame(left_frame,bd=2,bg="white",relief=RIDGE)
        btn_frame.place(x=10,y=390,width=635,height=60)

        #Show button
        save_bt=Button(btn_frame,command=self.fetch_Data,text="Show Att.",width=12,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        save_bt.grid(row=0,column=0,padx=6,pady=10,sticky=W)



        #Save button
        update_btn=Button(btn_frame,command=self.save_data,text="Save Data",width=12,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        update_btn.grid(row=0,column=1,padx=6,pady=8,sticky=W)




        # Right section=======================================================

        # Right Label Frame 
        # right_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Details",font=("verdana",12,"bold"),fg="navyblue")
        # right_frame.place(x=680,y=10,width=660,height=480)

    def get_cursor_left(self,event=""):
            cursor_focus = self.attendanceReport_left.focus()
            content = self.attendanceReport_left.item(cursor_focus)
            data = content["values"]

            self.var_roll.set(data[0]),
            self.var_name.set(data[1]),
            self.var_status.set(data[2]),
            self.var_date.set(data[3]),
            self.var_subject.set(data[4]),


        #----------------------------Fetch Data from Database----------------------
    def fetch_Data(self):
            conn = sq.connect(host="localhost",username="root",password="SuperPC@467",database="face_recognition")
            mycursor = conn.cursor()
            if self.var_subject.get()=="Arabic":
                mycursor = conn.cursor()

                mycursor.execute("select * from arabic")
                data=mycursor.fetchall()

                if len(data)!= 0:
                    self.attendanceReport_left.delete(*self.attendanceReport_left.get_children())
                    for i in data:
                        self.attendanceReport_left.insert("",END,values=i)
                    conn.commit()
                conn.close()
            elif self.var_subject.get()=="NLP":

                mycursor = conn.cursor()

                mycursor.execute("select * from nlp")
                data=mycursor.fetchall()

                if len(data)!= 0:
                    self.attendanceReport_left.delete(*self.attendanceReport_left.get_children())
                    for i in data:
                        self.attendanceReport_left.insert("",END,values=i)
                    conn.commit()
                conn.close()

            elif self.var_subject.get()=="SE Economics":

                mycursor = conn.cursor()

                mycursor.execute("select * from se_economics")
                data=mycursor.fetchall()

                if len(data)!= 0:
                    self.attendanceReport_left.delete(*self.attendanceReport_left.get_children())
                    for i in data:
                        self.attendanceReport_left.insert("",END,values=i)
                    conn.commit()
                conn.close()

            elif self.var_subject.get()=="Topics in SE":
                mycursor = conn.cursor()

                mycursor.execute("select * from topics_in_se")
                data=mycursor.fetchall()

                if len(data)!= 0:
                    self.attendanceReport_left.delete(*self.attendanceReport_left.get_children())
                    for i in data:
                        self.attendanceReport_left.insert("",END,values=i)
                    conn.commit()
                conn.close()
            else:
                messagebox.showerror("error","Error")

    def save_data(self):
            aniData=pd.read_csv("text.txt",sep=' ',index_col=False,delimiter=',')
            aniData.head()
            today = str(date.today())
            aniData=pd.read_csv("text.txt",index_col=False,delimiter=',')
            aniData["Date"] = today
            aniData["Status"]="p"
            aniData["Subject"]=self.var_subject.get()
            finalFile="text.csv"
            aniData.to_csv(finalFile, index=False)
                    # finalFile="live.csv"
            if self.var_subject.get()=="Arabic":
                try:
                    conn=sq.connect(host="localhost",username="root",password="SuperPC@467",database="face_recognition")
                    cursor=conn.cursor()
                    for i,row in aniData.iterrows():
                        sql="Insert into arabic VALUES(%s,%s,%s,%s)"
                        cursor.execute(sql,tuple(row))
                        print("Saved")
                        
                        conn.commit()
                    messagebox.showinfo("Saved","Inserted successfully")
                except Exception as ex:
                        print("Error while connecting to MYSQL",ex)
            elif self.var_subject.get()=="SE Economics":
                try:
                    conn=sq.connect(host="localhost",username="root",password="SuperPC@467",database="face_recognition")
                    cursor=conn.cursor()
                    for i,row in aniData.iterrows():
                        sql="Insert into se_economics VALUES(%s,%s,%s,%s)"
                        cursor.execute(sql,tuple(row))
                        print("Saved")
                        
                        conn.commit()
                    messagebox.showinfo("Saved","Inserted successfully")
                except Exception as ex:
                        print("Error while connecting to MYSQL",ex)

            elif self.var_subject.get()=="NLP":
                try:
                    conn=sq.connect(host="localhost",username="root",password="SuperPC@467",database="face_recognition")
                    cursor=conn.cursor()
                    for i,row in aniData.iterrows():
                        sql="Insert into nlp VALUES(%s,%s,%s,%s)"
                        cursor.execute(sql,tuple(row))
                        print("Saved")
                        
                        conn.commit()
                    messagebox.showinfo("Saved","Inserted successfully")
                except Exception as ex:
                        print("Error while connecting to MYSQL",ex)
            elif self.var_subject.get()=="Topics in SE":
                try:
                    conn=sq.connect(host="localhost",username="root",password="SuperPC@467",database="face_recognition")
                    cursor=conn.cursor()
                    for i,row in aniData.iterrows():
                        sql="Insert into topics_in_se VALUES(%s,%s,%s,%s)"
                        cursor.execute(sql,tuple(row))
                        print("Saved")
                        
                        conn.commit()
                    messagebox.showinfo("Saved","Inserted successfully")
                except Exception as ex:
                        print("Error while connecting to MYSQL",ex)
            else:
                messagebox.showinfo("Not saved","Something wrong")












if __name__ == "__main__":
    root=Tk()
    obj=Attendance(root)
    root.mainloop()