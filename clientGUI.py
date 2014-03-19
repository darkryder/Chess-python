import sys
from PyQt4 import QtGui,QtCore
import socket
from functools import partial
from time import sleep
import select
from subprocess import Popen

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
            a[1].setEnabled(1)
            a[1].setText("Challenge !!")
            
        except KeyError:
            
            self.playerName = QtGui.QLabel(name,self)
            self.playerName.setAlignment(QtCore.Qt.AlignCenter)
            self.mainGrid.addWidget(self.playerName,len(self.playerNamesObjects)+3,0,1,1)

            self.challengeButton = QtGui.QPushButton("Challenge !!")

            if name == NAME:
                self.challengeButton.setDisabled(1)
                self.challengeButton.setText("<You>")
            else:
                self.challengeButton.clicked.connect(partial(self.challenge, name))

            self.mainGrid.addWidget(self.challengeButton,len(self.playerNamesObjects)+3,2,1,2)            
            self.playerNamesObjects[name] = (self.playerName,self.challengeButton)

    def removePlayer(self,name):
        try:
            self.playerNamesObjects[name][1].setDisabled(1)
            self.playerNamesObjects[name][1].setText("Offline")
            
        except KeyError:
            pass

    def initNet(self):
        thread = CheckNewData()
        self.connect(thread,thread.newDataSignal,self.update)
        thread.start()

    def PrintPlayersName(self,data):

        self.PlayersHeadingLabel = QtGui.QLabel('Players Online',self)
        self.PlayersHeadingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainVBox.addWidget(self.PlayersHeadingLabel)

        self.Identifier = QtGui.QLabel("You are %s"%NAME ,self)
        self.Identifier.setAlignment(QtCore.Qt.AlignCenter)
        self.mainVBox.addWidget(self.Identifier)
        self.mainVBox.addWidget(QtGui.QLabel('',self))


        self.mainVBox.addLayout(self.mainGrid)



        for players in data.split('+')[1:]:
            self.addPlayer(players)

    def update(self):

        new = selfSocket.recv(8192)
        # print new

        if new.split('+')[0] == "ADD":
            self.addPlayer(new.split('+')[1])

        elif new.split('+')[0] == "CLIENT":
            Popen(['python','chess_black.py','%s'%NAME,'%s'%new.split('+')[1],'%s'%new.split('+')[2]])        

        elif new.split('+')[0] == "SERVER":
            Popen(['python','chess_white.py','%s'%NAME,'%s'%new.split('+')[1],'%s'%new.split('+')[2]])

            
        elif new.split('+')[0] == "REMOVE":
            self.removePlayer(new.split('+')[1])

        else:
            print "ERROR", new

    def challenge(self,user):
        selfSocket.send("CHALLENGE+%s+%s"%(NAME,user))

    def __init__(self):
        super(mainClientWindow,self).__init__()
        self.playerNamesObjects = {}
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Chess")

        self.mainVBox = QtGui.QVBoxLayout()

        self.mainGrid = QtGui.QGridLayout()


        self.setLayout(self.mainVBox)


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


def main():

    ex = mainClientWindow()

    QtCore.QTimer.singleShot(0,ex.initNet)

    app.exec_()

    selfSocket.send("EXIT+%s"%NAME)
    selfSocket.close()
    sys.exit()

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    main()