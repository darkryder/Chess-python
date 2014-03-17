import sys
from PyQt4 import QtGui,QtCore
import socket
from functools import partial

NAME = sys.argv[1]

SERVER = '127.0.0.1'
PORT = 2440

selfSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
selfSocket.connect((SERVER, PORT))

selfSocket.send(NAME)

class mainClientWindow(QtGui.QWidget):

	def getAndPrintPlayersName(self):
		for p in self.playerNamesObjects:
			p.hide()

		p = []
		PlayersHeadingLabel = QtGui.QLabel('Players online',self)
		PlayersHeadingLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.mainVbox.addWidget(PlayersHeadingLabel)

		RefreshButton = QtGui.QPushButton("Refresh Players",self)
		self.mainVbox.addWidget(RefreshButton)
		RefreshButton.clicked.connect(self.refresh)

		self.playerNamesObjects.extend([PlayersHeadingLabel,RefreshButton])

		new = selfSocket.recv(8192)

		if new.split('+')[0] == "ADD":
			for players in new.split('+')[1:]:	
				self.hbox = QtGui.QHBoxLayout()

				self.playerName = QtGui.QLabel(players,self)
				self.playerName.setAlignment(QtCore.Qt.AlignCenter)
				self.hbox.addWidget(self.playerName)

				self.spacer = QtGui.QLabel("",self)
				self.hbox.addWidget(self.spacer)

				self.challengeButton = QtGui.QPushButton("Challenge %s !!" %players)				
				self.challengeButton.clicked.connect(partial(self.challenge, players))
				self.hbox.addWidget(self.challengeButton)
				self.mainVbox.addLayout(self.hbox)

				self.playerNamesObjects.extend([self.playerName,self.challengeButton])


	def refresh(self):
		selfSocket.send("REFRESH")
		self.mainVbox.addStretch(0)
		self.getAndPrintPlayersName()

	def challenge(self,user):
		selfSocket.send("CHALLENGE %s %s"%(NAME,user))

	def __init__(self):
		super(mainClientWindow,self).__init__()
		self.playerNamesObjects = []
		self.initUI()

	def initUI(self):
		self.mainVbox = QtGui.QVBoxLayout()
		self.setGeometry(300,300,500,500)
		self.setWindowTitle("Chess")
		self.setLayout(self.mainVbox)
		self.refresh()
		self.show()

def main():

	app = QtGui.QApplication(sys.argv)
	ex = mainClientWindow()
	a = app.exec_()

	selfSocket.send("EXIT %s"%NAME)
	selfSocket.close()
	sys.exit()

if __name__ == "__main__":
	main()
