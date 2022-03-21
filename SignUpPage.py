from tkinter import *
from tkinter import messagebox
import client

root = Tk()

##set the background colour of GUI window
root.configure(background='white')
 
    # set the title of GUI window
root.title("Sign Up PAGE")
 
    # set the configuration of GUI window
root.geometry("500x300")
 
 
    # create a Form label
heading = Label(root, text="Sign Up", bg="white")
 
    # create a Name label
username = Label(root, text="Username", bg="white")
 
    # create a Course label
password = Label(root, text="Password", bg="white")
confirmpassword = Label(root, text="Confirm Password", bg ="white")
 
 
    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
heading.grid(row=0, column=1)
username.grid(row=1, column=0)
password.grid(row=2, column=0)
confirmpassword.grid(row=3, column = 0)

    
username_field = Entry(root)
password_field = Entry(root)
confirmpassword_field = Entry(root)


username_field.grid(row=1, column=1, ipadx="100")
password_field.grid(row=2, column=1, ipadx="100")
confirmpassword_field.grid(row=3, column = 1, ipadx= "100")

def SignedUp():
     usr = username_field.get()
     passw = password_field.get()
     cpassw = confirmpassword_field.get()
     if("/" in usr):
        messagebox.showerror("showerror", "Error / cannot be used at the end of a username")
        
        import LoginPage
     elif(len(usr) == 0 or len(passw) == 0 or len(cpassw)==0):
        messagebox.showerror("showerrror", "Error, please fill in a username and password")
        
     elif(passw != cpassw):
        messagebox.showerror("showerrror", "Passwords do not match")
     else :
         c = client
         c.signUp(usr, passw)
         root.destroy()
         import GUIbox
    
def backToLogin():
    root.destroy()
    import LoginPage

##create a sign up button
signup = Button(root, text= "Sign up", fg="black", bg = "white", command=SignedUp)
signup.grid(row = 6, column = 1)

##create a back button 
back = Button(root, text= "Back", fg= "black", bg = "white", command= backToLogin )
back.grid(row = 8, column = 1)
    
root.mainloop()