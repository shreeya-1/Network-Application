from socket import *
import threading
import User
import array as arr #more efficient data storage than a list

#change
print("wdd2")
serverPort = 5053
serverSocket = socket(AF_INET, SOCK_DGRAM) #datagram or packet being received
serverSocket.bind(('',serverPort))
#endmsg = "!Log off"

users = [] #append users to this list as they register


def new_client(message, clientAdd):
    print (f"Receiving from new client at {clientAdd}")
    receivedmsg = message.decode() #decode function interprets message from bytes to chars, DO SOMETHING W RECIEVED MSG

    ##SEND OF CONF MSG IMMEDIATELY
    confirmed = "Message received by server."
    print (receivedmsg)
    serverSocket.sendto(confirmed.encode(),clientAdd)


    #split string according to fullstops, first element will always be msg type
    parts =  receivedmsg.split(".")
    msgtype = parts[0]

    

    if msgtype == "LOG":
        
        uname = parts[1]
        pwd = parts[2]

        valid = False
        if users:  #find user from list if users not empty
            for i in users:
                if users[i].getUname() == uname and users[i].getPwd() == pwd:
                    valid = True
                    break
        if valid:
            retmsg = "LOGRT." + "1"
        else:
            retmsg = "LOGRT." + "0"
        

    if msgtype == "REG":
        vreg = True

        uname = parts[1]
        pwd = parts[2]

        if "." in uname or "." in pwd:
            vreg = False
            error = "FSTOP" #fullstops

        if users:
            if users.getUname() == uname:
                vreg = False
                error = "TKN" #taken
        
        if not vreg:
            retmsg = "LOGRT." + "0." + error
        else:
            retmsg = "LOGRT." + "1." 

    print ("SENDING TO CLIENT: " + retmsg)
    serverSocket.sendto(retmsg.encode(),clientAdd)
 
def start():
    while True:
         print (f"LISTENING - The server is listening..")
         message, clientAddress = serverSocket.recvfrom(2048) #clientAddress taken from message receive
         thread = threading.Thread(target= new_client, args = (message, clientAddress)) #new thread created for every client
         thread.start()
         print(f"ACTIVE CONNECTIONS {threading.activeCount() }") # -1 because want to exclude main thread 

        
print ("STARTING - server is starting")
start()