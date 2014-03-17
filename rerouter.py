import socket
import subprocess
import time
import select

PlayersCurrentlyPlaying = {}
PlayersInQueue = {}

SocketsToTrack = []

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

PORT = 2440
NETWORK_REACH = '0.0.0.0'
LISTEN_LIMIT = 50						#How many clients can it handle
RECV_BUFFER = 8192

serverSocket.bind((NETWORK_REACH,PORT))
serverSocket.listen(LISTEN_LIMIT)
SocketsToTrack.append(serverSocket)


def SendPlayerList(sock):

	a = "ADD+" + '+'.join(PlayersInQueue.keys())
	sock.send(a)

while 1:
	try:

		read,write,error = select.select(SocketsToTrack,[],[],0.1)

		for s in read:

			if s==serverSocket:								#new incoming connection request
				clientSocket,clientAddress = serverSocket.accept()
				clientName = clientSocket.recv(RECV_BUFFER)
				if clientName in PlayersInQueue.keys(): 
					print "ERROR"
					continue
				
				SocketsToTrack.append(clientSocket)
				PlayersInQueue[clientName] = (clientSocket,clientAddress)

			else:
				temp = s.recv(RECV_BUFFER)
				
				if temp.split()[0] == "EXIT":
					SocketsToTrack.remove(PlayersInQueue[temp.split()[1]][0])
					del PlayersInQueue[temp.split()[1]]
				
				elif temp == "REFRESH":
					#send the player all the current players
					SendPlayerList(s)

				elif temp.split()[0] == "CHALLENGE":
					uid = time.time()
					user1 = temp.split()[1]
					user2 = temp.split()[2]
					
					PlayersInQueue[user1][0].send( "SERVER %s %s" % (PlayersInQueue[user2][1],str(uid)) )
					PlayersInQueue[user2][0].send( "CLIENT %s %s" % (PlayersInQueue[user1][1],str(uid)) )
					
					del PlayersInQueue[user1]
					del PlayersInQueue[user2]
					
					PlayersCurrentlyPlaying[user1] = (user2,str(uid))
					PlayersCurrentlyPlaying[user2] = (user1,str(uid))


	except:
		serverSocket.close()
		exit()
