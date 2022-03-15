from socket import *
import threading
from User import *

serverPort = 5053 
serverSocket = socket(AF_INET, SOCK_DGRAM) #datagram or packet being received
serverSocket.bind(('',serverPort))
#endmsg = "!Log off"

users = [] #append users to this list as they register
actives = []

def new_client(message, clientAdd):
    print (f"Receiving from new client at {clientAdd}")
    receivedmsg = message.decode() #decode function interprets message from bytes to chars, DO SOMETHING W RECIEVED MSG

    ##SEND OF CONF MSG IMMEDIATELY
    confirmed = "Message received by server."
    print (receivedmsg)
    serverSocket.sendto(confirmed.encode(),clientAdd)


    #split string according to fullstops, first element will always be msg type
    parts =  receivedmsg.split("/")
    msgtype = parts[0]

    

    if msgtype == "LOG":
        
        uname = parts[1]
        pwd = parts[2]

        valid = False
        
        if users:  #find user from list if users not empty
            index1 = 0
            for user in users:
                if users[index1].getUname() == uname and users[index1].getPwd() == pwd:
                    valid = True
                    pos = index1
                    break
                index1 = index1 +1
        if valid:
            #USER IS NOW LOGGED IN AND ONLINE
            #UPDATE STATUS

            #update their ip address to new ip addr
            users[pos].updateIP(clientAdd)
        
            if actives: #if there are any active users
                temp = ""
                for active in actives:
                    temp = temp + active.getUname() + "|"
            else:
                temp = "NULL"

            actives.append(users[pos])
            retmsg = "LOGRT/" + "1/" + temp
        
        else:
            retmsg = "LOGRT/" + "0"
        

    if msgtype == "REG":
        vreg = True

        uname = parts[1]
        pwd = parts[2]
        print(uname)
        print(pwd)
        

        if users:
            index = 0
            for user in users:
                test = users[index] 
                if test.getUname() == uname:
                    vreg = False
                    
        
        if vreg == False:
            retmsg = "REGRT/" + "0/" 
        else:
            newuser = User(uname,pwd,clientAdd)
            users.append(newuser) #register new user
            actives.append(newuser)
            ##STATUS UPDATE broadcast that they are online 
            
            if actives: #if there are any active users send that to client
                temp = ""
                for active in actives:
                    temp = temp + active.getUname() + "|"
            else:
                temp = "NULL"
            retmsg = "REGRT/" + "1/" + temp

    print ("SENDING TO CLIENT: " + retmsg)
    serverSocket.sendto(retmsg.encode(),clientAdd)
    msg, addr = serverSocket.recvfrom(2048)
    msg = msg.decode()
    comps = msg.split("/")
    if comps[0] == "CHAT":
        recip = comps[1]
        txt = comps[2]

        for user in users:
            if recip == user.getUname():
                dest = user.getIP
                srcip = str(clientAdd[0])
                outgoing = "CHAT/" + srcip + "/" + txt
                print("OVER HERE" + dest)
                serverSocket.sendto(outgoing.encode(), dest)
                print("Message sent to user.")
 
def start():
    while True:
         print (f"LISTENING - The server is listening..")
         message, clientAddress = serverSocket.recvfrom(2048) #clientAddress taken from message receive
         thread = threading.Thread(target= new_client, args = (message, clientAddress)) #new thread created for every client
         thread.start()
         print(f"ACTIVE CONNECTIONS {threading.activeCount() }") # -1 because want to exclude main thread 

        
print ("STARTING - server is starting")
start()