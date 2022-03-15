

# creating client first

#only client needs to know ip address of server since server will receive from packet 
import socket
serverName =  "192.168.1.68"
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


flist = fdback.split("/")
if flist[0] == "LOGRT":

    if (int(flist[1]) == 1):         #login succesful
        print (f"Your login was succesful, you are now online.")
        #STATUS MUST BE UPDATED ON SERVER SIDE BEFORE FBCK SENT
    else:
        print(f"Your username or password is incorrect.")

elif flist[0] == "REGRT":
    print(flist[1])
    if (int(flist[1])==1):
            #sign up succesful
        print("Your sign up was succesful. You are now a registered user.")
    else:
         emsg = "That username is already taken, please enter a different username."
         print (emsg)
         uname = input("Username: ")
    
recip = input("List of online users")
message = input('Input message to send to user, enter "QUIT" to log off:  ')
if message != "QUIT":
    online = True

while online:
    
    clientSocket.sendto(message.encode(),(serverName,serverPort))
    print ("Message has been sent")
    modMsg, clientAddress = clientSocket.recvfrom(2048) #2048 specifies amt of space in buffer
    print (modMsg.decode())
    #clientSocket.close()
    message = input('Input message to send to user, enter "QUIT" to log off:  ')
    if message == "QUIT":
        online = False


