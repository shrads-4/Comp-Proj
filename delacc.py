import os 
import subprocess 
import sys 
import getpass
import tkinter,tkinter.messagebox

def delete_user(): 
     username = input("Enter Username : ") #to be connected to sql
  
     try: 
         output = subprocess.run(['userdel', username ]) 
         if output.returncode == 0: 
             print("Your account is successfully deleted") 
  
     except: 
         print(f"Failed to delete user.") 
         sys.exit(1) 

top=tkinter.Tk()
canvas1=tkinter.Canvas(top, width=400, height=400 )
canvas1.pack()

def application():
    a=tkinter.messagebox.askquestion("Delete account","Are you sure you want to delete your account?")
    if a=="yes":
        b.destroy()
        delete_user()
    else:
        tkinter.messagebox.showinfo("Return")

b=tkinter.Button(top,text="Delete account",command=application)
canvas1.create_window(200,200,window=b)
top.mainloop()
