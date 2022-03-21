from tkinter import *
from tkinter import messagebox
import client

##import client

root = Tk()


##set the background colour of GUI window
root.configure(background='white')
 
    # set the title of GUI window
root.title("LOGIN PAGE")
 
    # set the configuration of GUI window
root.geometry("500x300")
 
 
    # create a Form label
heading = Label(root, text="LOGIN PAGE", bg="white")
 
    # create a Name label
username = Label(root, text="Username", bg="white")
 
    # create a Course label
password = Label(root, text="Password", bg="white")
 

    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
heading.grid(row=0, column=1)
username.grid(row=1, column=0)
password.grid(row=2, column=0)

    
username_field = Entry(root)
password_field = Entry(root)


username_field.grid(row=1, column=1, ipadx="100")
password_field.grid(row=2, column=1, ipadx="100")

    

def retrieve_input():
    usr = username_field.get()
    passw = password_field.get()
    if("/" in usr):
        messagebox.showerror("showerror", "Error / cannot be used at the end of a username")
        
        import LoginPage
    elif(len(usr) == 0 or len(passw) == 0):
        messagebox.showerror("showerrror", "Error, please fill in a username and password")
    
    
    else :
       
        client.logIn(usr, passw)
        root.destroy()
        import GUIbox
    
def signUpPage():
    root.destroy()
    import SignUpPage
    
def exit():
    root.destroy()

#create a log in button 
login = Button(root, text = "Log In", fg = "Black", bg = "white", command=retrieve_input)
login.grid(row= 4, column = 1)

##sign up label
signuplbl = Label(root, text = "Not a user yet? Proceed to sign up page", bg = "white")
signuplbl.grid(row = 5, column = 1)

    
##create a sign up button
signup = Button(root, text= "Go to Sign up Page", fg="black", bg = "white", command=signUpPage)
signup.grid(row = 6, column = 1, )

##create terminate program button
exit = Button(root, text= "Exit",fg =  "black" , bg = "white", command=exit )
exit.grid(row=7 , column = 1)

    
root.mainloop()