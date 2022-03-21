

# creating client first

#only client needs to know ip address of server since server will receive from packet 
import time
import socket
import threading
serverName =  "10.0.0.101"
#socket.gethostbyname(socket.gethostname())

serverPort = 5053 # first few addresses are reserved for common protocols such as http 
            # must specify port where messages will be received
#creating new socket for client
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #AF_INET specifies length of ip address

#message number
message_num = 0
#ack timer
start_time = 0
end_time = 0

#method to track the time of the rtt of the acks 
def ackTime(start_time ,end_time):
    diff= end_time - start_time   #it is in seconds 
    if(end_time == 0):
        print("Message (" + message_num + ") has failed - resend the message")  #messages should be stored so that user does not have to resend 
    print(diff)

startmsg = input("Enter 1 to Log in and 2 to Sign up: ")
startmsg = int(startmsg)
online = False


if (startmsg == 1) :
    loguser = input ("Enter your username: ")
    logpwd = input ("Enter your password: ")
    

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

def signUp(usrname, pwd):

    #sends off login details to server
    reg = "REG/" + usrname +"/" + pwd
    clientSocket.sendto(reg.encode(),(serverName,serverPort))

    #receives confirmation + feedback from server
    fdback2, addr = clientSocket.recvfrom(2048)
    fdback2 = fdback2.decode()
    #print(fdback2)

    fdback, addr = clientSocket.recvfrom(2048) 
    fdback = fdback.decode()
    #print(fdback)

    flist = fdback.split("/")
    retmsg = ""

    if flist[0] == "REGRT":
        print(flist[1])
        if (int(flist[1])==1):
                #sign up succesful
            global online
            online = True
            retmsg = "Your sign up was succesful. You are now a registered user."
            
            others = flist[2]
            global unames
            if others == "NULL":
                unames = "There are no other users online."
            else:
                unames = others.split("|")
            

        else:
            retmsg = "That username is already taken, please enter a different username."
            #print (retmsg)
            #uname = input("Username: ")
            

            #reg = "REG/" + uname +"/" + regpwd
            #clientSocket.sendto(reg.encode(),(serverName,serverPort))
    return online + "/" + retmsg + "/" + others



def logIn(usrname, pwd):
    creds = "LOG/" + usrname + "/" + pwd #user credentials
    clientSocket.sendto(creds.encode(),(serverName,serverPort))

    fdback2, addr = clientSocket.recvfrom(2048)
    fdback2 = fdback2.decode()
    print(fdback2)

    fdback, addr = clientSocket.recvfrom(2048) 
    fdback = fdback.decode()
    print(fdback)


    flist = fdback.split("/")
    if flist[0] == "LOGRT":

        if (int(flist[1]) == 1):         #login succesful
            retmsg = "Your login was succesful, you are now online."
            global online
            online = True

            others = flist[2]
            #if others == "NULL":
             #   unames = "There are no other users online."
            #else:
              #  unames = others.split("|")
            #STATUS MUST BE UPDATED ON SERVER SIDE BEFORE FBCK SENT
        else:
            retmsg = "Your username or password is incorrect."

    return online + "/" + retmsg + "/" + others


def incoming():
    while True: # currently listening indefinitely
         newmsg, addr = clientSocket.recvfrom(2048)
         newmsg = newmsg.decode()

         #checking the time of the ack rtt 
         if(start_time != 0):
             t = threading.Timer(15.0, ackTime(start_time , end_time))    #give the ack 15 seconds to return 
             t.start()

         comps = newmsg.split("/") 
         mtype = comps[0]   
         if (mtype == "CHAT"):
             message_from = comps[1]
             print("You received a message from " + message_from)
             print ("MESSAGE: " + comps[2])
             #find the hash value of value of message 
             hashMessage = str(hash(comps[2]))
             #compare the hash values to verify correctness of message
             if(hashMessage == str(comps[3])):
                 print("Message received is correct") #error handling in GUI section
             else:
                 print("Message received is erroneous")
             messageNumber = comps[4]
             #send an ACK(2) to server to acknowledge receipt of message 
             ack2 = "ACK/" + "2/" + message_from + "/" + messageNumber
             clientSocket.sendto(ack2.encode(), (serverName,serverPort))
         
         elif (mtype == "ACK"):
             ack_type = comps[1]
             if(ack_type == "2"):
                message_num = comps[3]
                ack_from = comps[4]
                #stop the time 
                end_time = time.time()
                print("FINAL ACK returned: message number " + message_num + " sent to " + ack_from + " has been received ")
             elif (ack_type == "1"):
                 recip = comps[2]
                 message_num = comps[3]
                 print("Message " + message_num + " for " + recip +" has been received by the server")


    
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
    #hash the message to be sent 
    hash_message = str(hash(message))

    msg = "CHAT/" + recip +"/" + message + "/" + hash_message + "/" + message_num #includes hash & message number 
    clientSocket.sendto(msg.encode(),(serverName,serverPort))
    print ("Message has been sent to server")
    #message number increment 
    message_num= message_num+1
    #start the time 
    start_time = time.time()



#stop and wait for ack?
    #conf, clientAddress = clientSocket.recvfrom(2048) #2048 specifies amt of space in buffer
    #print(conf.decode()) #confirmation message

clientSocket.close()
   


