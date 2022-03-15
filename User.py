class User:
    def __init__(self, uname, pwd, addr):
        self.uname = uname
        self.pwd = pwd
        self.addr = addr
        self.msgs = []


    def updateIP(self, addr):
        self.addr = addr

    def getUname(self):
        return self.uname

    def getIP(self):
        return self.addr

    def getPwd(self):
        return self.pwd

    def addMsg(self, msg): #msg MUST be in msg, addr format
        self.msgs.append(msg)