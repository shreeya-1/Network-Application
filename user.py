# creating a user class to store user details 

class User:
    # name = ""
    # IP adress = ""
    # password = ""

    def __init__(self,uname, pwd, addr):
        print(f'instatiating user object with the following properties/arguments {uname} {pwd} {addr}')
        self.uname = uname
        self.pwd = pwd 
        self.addr = addr
        self.mlist = []

    #list of messages property 
    def appendList(self, message):
        return (self.message_list.append(message))

    #setter
    def updateIP(self, addr):
        self.addr = addr

    #getter
    def getUname(self):
        return self.uname 

    def getPwd(self):
        return self.pwd 

    def getList (self):
        return self.mlist


    

   