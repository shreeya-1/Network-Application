

# creating client first

#only client needs to know ip address of server since server will receive from packet 
import socket
import threading
serverName =  "10.0.0.104"
#socket.gethostbyname(socket.gethostname())

serverPort = 5053 # first few addresses are reserved for common protocols such as http 
            # must specify port where messages will be received
#creating new socket for client
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #AF_INET specifies length of ip address

startmsg = input("Enter 1 to Log in and 2 to Sign up: ")
startmsg = int(startmsg)

if (startmsg == 1) :
    loguser = input ("Enter your username: ")
    logpwd = input ("Enter your password: ")
    
    #usernames cannot end w/ .

    #send to server to check user
    creds = "LOG/" + loguser + "/" + logpwd #user credentials
    clientSocket.sendto(creds.encode(),(serverName,serverPort))

    
    
if (startmsg == 2):
    vreg = False   
    regname = input("What would you like your username to be?: ")

    while ("/" in regname):
          print("Forward slashes not permitted in username.")
          regname = input("Enter a valid username: ")

    
    regpwd = input("Please enter a password for your account: ")
    while ("/"  in regpwd):
        print("Forward slashes not permitted in password.")
        regpwd = input("Enter a valid password: ")
        
    regpwd2 = input("Confirm your password choice: ")

    while (regpwd != regpwd2):
        regpwd = input ("Your passwords do not match, please re-enter password: ")
        regpwd2 = input ("Confirm your password choice: ")

    reg = "REG/" + regname +"/" + regpwd
    clientSocket.sendto(reg.encode(),(serverName,serverPort))


#feeback from log in or registration from server
fdback2, addr = clientSocket.recvfrom(2048)
fdback2 = fdback2.decode()
print(fdback2)

fdback, addr = clientSocket.recvfrom(2048) 
fdback = fdback.decode()
print(fdback)

online = False

flist = fdback.split("/")
if flist[0] == "LOGRT":

    if (int(flist[1]) == 1):         #login succesful
        print (f"Your login was succesful, you are now online.")
        online = True

        others = flist[2]
        if others == "NULL":
            unames = "There are no other users online."
        else:
            unames = others.split("|")
        #STATUS MUST BE UPDATED ON SERVER SIDE BEFORE FBCK SENT
    else:
        print(f"Your username or password is incorrect.")


elif flist[0] == "REGRT":
    print(flist[1])
    if (int(flist[1])==1):
            #sign up succesful
        print("Your sign up was succesful. You are now a registered user.")
        online = True
        others = flist[2]
        if others == "NULL":
            unames = "There are no other users online."
        else:
            unames = others.split("|")
        

    else:
         emsg = "That username is already taken, please enter a different username."
         print (emsg)
         uname = input("Username: ")
         while ("/" in uname):
             print("Forward slashes not permitted in username.")
             uname = input("Enter a valid username: ")

         reg = "REG/" + uname +"/" + regpwd
         clientSocket.sendto(reg.encode(),(serverName,serverPort))



def incoming():
    while True: # currently listening indefinitely
         newmsg, addr = clientSocket.recvfrom(2048)
         newmsg = newmsg.decode()

         comps = newmsg.split("/") 
         mtype = comps[0]   
         if (mtype == "CHAT"):
             print("You received a message from " + comps[1])
             print ("MESSAGE: " + comps[2])
    
         elif (mtype == "STTS"):
 #notify users when someone logs on /out
            if (int(comps[2]) == 1):
               print(comps[1] + " is now online.")

            elif(int(comps[2]) == 0):
               print(comps[1] + " is now offline.")
         else:
             #confirmation message
             print(newmsg)

if online:
    thread = threading.Thread(target= incoming, args = ())
    thread.start()



#ONLY AFTER USER HAS REGISTERED OR LOGGED IN
while online : 
    print ("************List of online users************")
    #unames will need to be updated or status broadcasts implemented
    for usr in unames:
        print(usr + "\n")

    recip = input("Who would you like to send a message to?\nEnter username of recipient: ")
    message = input("Enter message or press QUIT: ")
    if message == "QUIT":
        online = False
        break
    

    msg = "CHAT/" + recip +"/" + message #will include message hash later
    clientSocket.sendto(msg.encode(),(serverName,serverPort))
    print ("Message has been sent to server")

    #dangerous, rather create new thread in case no message received from server
    # should it wait for confirmation before another message is allowed to be sent?

#stop and wait for ack?
    #conf, clientAddress = clientSocket.recvfrom(2048) #2048 specifies amt of space in buffer
    #print(conf.decode()) #confirmation message

clientSocket.close()
   


