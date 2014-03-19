import socket
import subprocess
import time
import select

PlayersCurrentlyPlaying = {}
PlayersInQueue = {}

SocketsToTrack = []

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

PORT = 2441
NETWORK_REACH = '0.0.0.0'
LISTEN_LIMIT = 50						#How many clients can it handle
RECV_BUFFER = 8192

serverSocket.bind((NETWORK_REACH,PORT))
serverSocket.listen(LISTEN_LIMIT)
SocketsToTrack.append(serverSocket)


def SendPlayerList(sock):

	a = "ADD+" + '+'.join(PlayersInQueue.keys())
	sock.send(a)
	# print "sending to socket"

while 1:

	read,write,error = select.select(SocketsToTrack,[],[],0.1)

	for s in read:

		if s==serverSocket:								#new incoming connection request
			clientSocket,clientAddress = serverSocket.accept()
			clientName = clientSocket.recv(RECV_BUFFER)
			if clientName in PlayersInQueue.keys(): 
				# print "ERROR"
				continue
			
			SocketsToTrack.append(clientSocket)
			PlayersInQueue[clientName] = (clientSocket,clientAddress)
			SendPlayerList(clientSocket)

			for s in SocketsToTrack:
				if s != serverSocket and s != clientSocket:
					s.send("ADD+%s"%clientName)
					# print "SENDING NEW NAME"

		else:
			temp = s.recv(RECV_BUFFER)
			
			if temp.split('+')[0] == "EXIT":
				SocketsToTrack.remove(PlayersInQueue[temp.split('+')[1]][0])
				del PlayersInQueue[temp.split('+')[1]]
				for socket in SocketsToTrack:
					if socket != serverSocket:
						socket.send("REMOVE+%s"%temp.split('+')[1])
						# print "SENDING REMOVE"
			
			
			elif temp.split('+')[0] == "CHALLENGE":
				uid = time.time()
				[user1,user2] = temp.split('+')[1:]
				# print 11254
				# print PlayersInQueue
				PlayersInQueue[user1][0].sendall( "SERVER+%s+%s" % (PlayersInQueue[user2][1][0],str(uid)) )
				# print 'SAGUASBGLUASBGLUIA'
				time.sleep(1)
				PlayersInQueue[user2][0].sendall( "CLIENT+%s+%s" % (PlayersInQueue[user1][1][0],str(uid)) )
				
				# del PlayersInQueue[user1]
				# del PlayersInQueue[user2]
				
				# PlayersCurrentlyPlaying[user1] = (user2,str(uid))
				# PlayersCurrentlyPlaying[user2] = (user1,str(uid))

serverSocket.close()
exit()
