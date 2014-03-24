# SEND NAME
# WAIT FOR WELCOME OR NAME_ERROR
#EXITS BY EXIT+NAME
#THE CHESS PROGRAM SHOULD TRY TO CONNECT 5 TIMES AFTER WAITING FOR 1 SECOND EACH TIME RATHER THAN SLOWING DOWN SERVER.
#ON CHALLENGING THEY SHOULD THE BUTTONS THEMSELVES THEY WONT GET A REQUEST FOR MODIFICATION FROM THE SERVER TO AVOID COLLISION WITH SERVER CLIENT REQUEST

import sys
from PyQt4 import QtGui,QtCore
import socket
from functools import partial
from time import sleep
from select import select
from subprocess import Popen,PIPE
from threading import Thread

NAME = sys.argv[1]

SERVER = '127.0.0.1'
PORT = 2440
RECV_BUFFER = 8192



selfSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
selfSocket.connect((SERVER, PORT))

def getCleanData(sock):
    data = sock.recv(RECV_BUFFER)
    return list(data.strip().split('\n'))

def sendCleanData(sock,data):
    sock.sendall(data + '\n')


gameProcess = None

sendCleanData(selfSocket,NAME)
verification = getCleanData(selfSocket)[0]

if verification == "NAME_ERROR":
    selfSocket.close()
    exit(0)

elif verification == "WELCOME":
    sendCleanData(selfSocket,"READY")

else:
    exit(0)



class CenterPanel(QtGui.QMainWindow):

	def __init__(self,playersRightPane):
		super(CenterPanel,self).__init__()
		self.setWindowTitle("Chess - IIITD")
		self.setGeometry(100,100,600,600)
		self.initGui(playersRightPane)
		
	def initGui(self,playersRightPane):
		self.mainVBox = QtGui.QVBoxLayout()

		self.show()
		
		pass

	pass
	

class MainWindow(QtGui.QWidget):

    def addPlayer(self,nameList):
    	for name in nameList:
	        try:
	            a = self.playerNamesObjects[name]
	            a[1].setEnabled(1)
	            a[1].setText("Challenge !!")
	            if name == NAME: 
	                a[1].setText("<You>")
	                a[1].setDisabled(1)
	        except KeyError:
	            
	            self.playerName = QtGui.QLabel(name,self)
	            self.playerName.setAlignment(QtCore.Qt.AlignCenter)
	            self.mainGrid.addWidget(self.playerName,len(self.playerNamesObjects),0,1,1)

	            self.challengeButton = QtGui.QPushButton("Challenge !!")

	            if name == NAME:
	                self.challengeButton.setDisabled(1)
	                self.challengeButton.setText("<You>")
	            else:
	                self.challengeButton.clicked.connect(partial(self.challenge, name))

	            self.mainGrid.addWidget(self.challengeButton,len(self.playerNamesObjects),2,1,2)
	            self.playerNamesObjects[name] = (self.playerName,self.challengeButton)

    def removePlayer(self,name):
        try:
            self.playerNamesObjects[name][1].setDisabled(1)
            self.playerNamesObjects[name][1].setText("Offline")
            
        except KeyError:
            pass

    def gameStatusChange(self):
        global gameProcess
        data = gameProcess.stdout.read()        
        gameProcess = None

        # print "called"

        if "RESIGN" in data:
            sendCleanData(selfSocket,"RESULT+DEFEAT+%s" %(NAME))
            # print 1

        elif "OPPONENT_SURRENDERED" in data:
            sendCleanData(selfSocket,"RESULT+VICTORY+%s"%NAME)
            # print 2
        elif "CLEAN_EXIT" in data:
            sendCleanData(selfSocket,"RESULT+DRAW+%s"%NAME)
            # print 3
        elif "OpponentNotAuthenticated" in data:
            sendCleanData(selfSocket,"RESULT+ERROR+%s"%NAME)
            # print 4
        else:
            print data

    def initNet(self):
        thread = CheckNewData()
        self.connect(thread,thread.newDataSignal,self.update)
        self.connect(thread,thread.gameFinishedSignal,self.gameStatusChange)
        thread.start()

    def PrintPlayersName(self):

        self.PlayersHeadingLabel = QtGui.QLabel('Players Online',self)
        self.PlayersHeadingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainVBox.addWidget(self.PlayersHeadingLabel)

        self.Identifier = QtGui.QLabel("You are %s"%NAME ,self)
        self.Identifier.setAlignment(QtCore.Qt.AlignCenter)
        self.mainVBox.addWidget(self.Identifier)
        self.mainVBox.addWidget(QtGui.QLabel('',self))

        self.mainVBox.addLayout(self.mainGrid)

    def changePlayerStatus(self,data):
        [user1,user2] = data.split('+')[1:]
        self.playerNamesObjects[user1][1].setText("VS %s"%user2)
        self.playerNamesObjects[user2][1].setText("VS %s"%user1)
        self.playerNamesObjects[user1][1].setDisabled(1)
        self.playerNamesObjects[user2][1].setDisabled(1)

    def startGameServer(self,new):
        
        global gameProcess
        gameProcess = Popen(['python','chess_white.py','%s'%NAME,'%s'%new.split('+')[2],
                            '%s'%new.split('+')[3]], stdout = PIPE)


    def startGameClient(self,new):

        self.playerNamesObjects[new.split('+')[1]][1].setDisabled(1)
        self.playerNamesObjects[new.split('+')[1]][1].setText("VS %s"%NAME)

        self.playerNamesObjects[NAME][1].setText("VS %s"%new.split('+')[1])
        
        global gameProcess
        gameProcess = Popen(['python','chess_black.py','%s'%NAME,'%s'%new.split('+')[2],
                                  '%s'%new.split('+')[3]], stdout = PIPE)

    def update(self):

        newData = getCleanData(selfSocket)
        for new in newData:
            print new

            if new.split('+')[0] == "ADD":
                self.addPlayer(list(new.split('+')[1:]))

            elif new.split('+')[0] == "CLIENT":
                self.startGameClient(new)

            elif new.split('+')[0] == "SERVER":
                self.startGameServer(new)            
                
            elif new.split('+')[0] == "REMOVE":
                self.removePlayer(new.split('+')[1])

            elif new.split('+')[0] == "PLAYING":
                self.changePlayerStatus(new)

            else:
                print "ERROR", new

    def challenge(self,user):
        sendCleanData(selfSocket,"CHALLENGE+%s+%s"%(NAME,user))
        self.playerNamesObjects[user][1].setText("VS %s"%NAME)
        self.playerNamesObjects[NAME][1].setText("VS %s"%user)
        self.playerNamesObjects[user][1].setDisabled(1)

    def __init__(self):
        super(MainWindow,self).__init__()
        self.playerNamesObjects = {}
        self.initUI()
        global gameProcess
        gameProcess = None
        
    def initUI(self):

        # self.setWindowTitle("Chess-IIITD")

        self.mainVBox = QtGui.QVBoxLayout()

        self.mainGrid = QtGui.QGridLayout()


        self.setLayout(self.mainVBox)


        # data = getCleanData(selfSocket)[0]
        self.PrintPlayersName()

        self.show()

class CheckNewData(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self, parent = app)
        self.newDataSignal = QtCore.SIGNAL("NEWDATA")
        self.gameFinishedSignal = QtCore.SIGNAL("GAMEFINISHED")

    def run(self):
        global gameProcess
        while 1:
            r,w,x = select([selfSocket],[],[],0.1)
            if r!=[]: self.emit(self.newDataSignal)
            if gameProcess:
                if gameProcess.poll() == None:
                    pass
                else:
                    self.emit(self.gameFinishedSignal)
                    # print "calling"
            sleep(0.1)

def main():

    ex = MainWindow()

    QtCore.QTimer.singleShot(0,ex.initNet)

    app.exec_()

    sendCleanData(selfSocket,"EXIT+%s"%NAME)
    selfSocket.close()
    sys.exit()

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    main()