from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import time
from login import Login
class Startup:
    def __init__(self,root):
        self.root=root
        self.root.geometry("780x500+280+100")
        self.root.title("Smart Classroom System")
        self.root.resizable(False,False)
        self.root.focus_force()

        bg1=Image.open(r"C:\Users\AMMAR MEER\Desktop\FRAS\Images_GUI\Smart Classroom System.png")
        bg1=bg1.resize((780,500))
        self.photobg1=ImageTk.PhotoImage(bg1)
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=0,width=780,height=500)

        start=Button(bg_img,command=self.runn,text="Start",font=("times new roman",15,"bold"),bd=0,relief=RIDGE,fg="White",bg="#00a79d",activeforeground="white",activebackground="#007ACC")
        start.place(x=40,y=338,width=316,height=20)
    def runn(self):
        root.withdraw()
        self.new_window=Toplevel(self.root)
        self.app=Login(self.new_window)





    # def mainWindow(self):
    #     time.sleep(5)
    #     self.new_window=Toplevel(self.root)
    #     self.app=Login(self.new_window)


if __name__ == "__main__":
    root=Tk()
    obj=Startup(root)
    root.mainloop()
    
    