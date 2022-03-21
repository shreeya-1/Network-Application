from http import server
from tkinter import *
import client
root = Tk()

root.title('WhatsDown')
root.geometry('{}x{}'.format(600, 600))

# create all of the main containers
center = Frame(root, bg='gray2', width=590, height=590, padx=3, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

center.grid(row=1, sticky="nsew")

# create the center widgets
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

ctr_left = Frame(center, bg='grey', width=295, height=590, padx=50, pady=50)
ctr_right = Frame(center, bg='white', width=295, height=590, padx=70, pady=50)

ctr_left.grid(row=0, column=0, sticky="ns")
ctr_right.grid(row=0, column=2, sticky="ns")

# create right sub widgets
ctr_right.grid_rowconfigure(1, weight=1)
ctr_right.grid_columnconfigure(0, weight=1)

##userlst = server.users
##lbl = Label(ctr_left, text = userlst)
##activelst = server.actives

##for()


#
# make the Listbox and buttons
#

def Exit():
   root.destroy()
   import LoginPage
   
def curseSelctor():
   to_field.delete("1.0", "end")
   to_field.insert(INSERT, subjects.get(ACTIVE))
   print(subjects.get(ACTIVE))
   
      
      

tolbl = Label(ctr_right, text = "To: ", bg = "white")
tolbl.grid(row = 0, column = 0)

to_field = Text(ctr_right, height=1, width = 3)

to_field.grid(row =0 , column = 1, ipadx="100")

##sign out button
signOut = Button(ctr_right, text="Sign Out", command=Exit)
signOut.grid(row = 2, column=15)

##message box
sendMessage_field = Entry(ctr_right)

sendMessage_field.grid(row = 2, column = 0)

##send message button 

sendMessage = Button(ctr_right, text="Send")

sendMessage.grid(row = 2, column = 1)

## chat button 

chatButton = Button(ctr_right, text= "Chat", command=curseSelctor)
chatButton.grid(row = 0, column = 0)


# Creates Listbox of existing subjects, from .txt files in directory of program
subjects = Listbox(ctr_left,width=32,height=30)
sub = ["User 1" , "User 2", "User 3"]

for i in range(len(sub)):
   
   subjects.insert(i, sub[i])
   
   
for i in range(len(sub)):
   if(sub[i] == "User 1"):
      subjects.itemconfig(i, {'bg': 'OrangeRed3'})
      ##print(sub[i])





##for this_file in glob.glob("*.txt"):
   ## subjects.insert(0, this_file.split('.')[0])
##subjects.grid(column=0, row=0, sticky="e")




subjects.pack()

root.mainloop()