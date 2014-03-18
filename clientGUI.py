import sys
from PyQt4 import QtGui,QtCore
import socket
from functools import partial
from time import sleep
import select

NAME = sys.argv[1]

SERVER = '127.0.0.1'
PORT = 2441
RECV_BUFFER = 8192

selfSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
selfSocket.connect((SERVER, PORT))

selfSocket.send(NAME)

class mainClientWindow(QtGui.QWidget):

    def addPlayer(self,name):

        try:
            # if name!=NAME:
            a = self.playerNamesObjects[name]
            a[2].setEnabled(1)
            a[2].setText("Challenge !!")
        except KeyError:
            self.hbox = QtGui.QHBoxLayout()

            self.playerName = QtGui.QLabel(name,self)
            self.playerName.setAlignment(QtCore.Qt.AlignCenter)
            self.hbox.addWidget(self.playerName)

            self.spacer = QtGui.QLabel("",self)
            self.hbox.addWidget(self.spacer)

            if name == NAME:
                self.challengeButton = QtGui.QPushButton("Can't challenge yourself.")
                self.challengeButton.setDisabled(1)
            else:
                self.challengeButton = QtGui.QPushButton("Challenge !!")
                self.challengeButton.clicked.connect(partial(self.challenge, name))
            self.hbox.addWidget(self.challengeButton)
            self.mainVbox.addLayout(self.hbox)
            self.playerNamesObjects[name] = (self.hbox,self.playerName,self.challengeButton)

    def removePlayer(self,name):
        try:
            self.playerNamesObjects[name][2].setDisabled(1)
            self.playerNamesObjects[name][2].setText("Offline")
            
        except KeyError:
            pass

    def initNet(self):
        thread = CheckNewData()
        self.connect(thread,thread.newDataSignal,self.update)
        thread.start()

    def PrintPlayersName(self,data):

        PlayersHeadingLabel = QtGui.QLabel('Players online\nYOU ARE %s'%NAME.upper() ,self)
        PlayersHeadingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainVbox.addWidget(PlayersHeadingLabel)

        for players in data.split('+')[1:]:
            self.addPlayer(players)

    def update(self):
        # print "RECIEVED"
        new = selfSocket.recv(8192)
        print new
        if new.split('+')[0] == "ADD":
            self.addPlayer(new.split('+')[1])
        elif new.split('+')[0] == "CLIENT":
            print "I KNOW I AM BEING CHALLENGED"
        elif new.split('+')[0] == "SERVER":
            print "I KNOW I AM CHALLENGING"
        elif new.split('+')[0] == "REMOVE":
            self.removePlayer(new.split('+')[1])

        else:
            print "ERROR"

    def challenge(self,user):
        selfSocket.send("CHALLENGE+%s+%s"%(NAME,user))

    def __init__(self):
        super(mainClientWindow,self).__init__()
        self.playerNamesObjects = {}
        self.initUI()

    def initUI(self):
        self.mainVbox = QtGui.QVBoxLayout()
        self.setGeometry(300,300,500,500)
        self.setWindowTitle("Chess")
        self.mainVbox.addStretch(0)

        self.setLayout(self.mainVbox)

        data = selfSocket.recv(RECV_BUFFER)
        self.PrintPlayersName(data)

        self.show()

class CheckNewData(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self, parent = app)
        self.newDataSignal = QtCore.SIGNAL("NEWDATA")
    
    def run(self):
        while 1:
            r,w,x = select.select([selfSocket],[],[],0.01)
            if r!=[]: self.emit(self.newDataSignal)
            sleep(1)


app = QtGui.QApplication(sys.argv)

def main():

    ex = mainClientWindow()

    QtCore.QTimer.singleShot(0,ex.initNet)

    app.exec_()

    selfSocket.send("EXIT+%s"%NAME)
    selfSocket.close()
    sys.exit()

if __name__ == "__main__":
    main()
