import socket
import time
from select import select

PORT = 2448
NETWORK_REACH = '0.0.0.0'
LISTEN_LIMIT = 50                       #Number of clients to handle
RECV_BUFFER = 8192

class PlayersState(object):

    def __init__(self):
        self.PlayersCurrentlyPlaying = {}       # (NAME1,NAME2) --> (CurrentlyPlaying<bool>, UID)
        self.PlayersOnline = {}                 # NAME --> (socket,address)

class Server(object):

    def __init__(self,playersObject):
        self.SocketsToTrack = []
        self.serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.serverSocket.bind((NETWORK_REACH,PORT))
        self.serverSocket.listen(LISTEN_LIMIT)
        self.SocketsToTrack.append(self.serverSocket)
        self.playersObject = playersObject

    def addNewPlayer(self,playername,playersocket,playeraddress,playersObject):
        for s in self.SocketsToTrack:
            if s != self.serverSocket:
                s.send("ADD+%s"%playername)

        playersObject.PlayersOnline[playername] = (playersocket,playeraddress)
        self.SocketsToTrack.append(playersocket)
        self.sendCompletePlayerList(playersocket,playersObject)

    def removePlayer(self,playername,playersObject):

        self.SocketsToTrack.remove(playersObject.PlayersOnline[playername][0])
        
        for s in self.SocketsToTrack:
            if s != self.serverSocket:
                s.send("REMOVE+%s"%playername)

        del playersObject.PlayersOnline[playername]

    def sendCompletePlayerList(self,socket,playersObject):

        a = "ADD+" + '+'.join(playersObject.PlayersOnline.keys())
        socket.send(a)

    def acceptNewPlayer(self,playersObject):
        clientSocket,clientAddress = self.serverSocket.accept()
        clientName = clientSocket.recv(RECV_BUFFER)
        if clientName in playersObject.PlayersOnline.keys(): 
            clientSocket.send("NAME_ERROR")
            return 0
        clientSocket.send("WELCOME")
        if clientSocket.recv(RECV_BUFFER) == "READY":
            self.addNewPlayer(clientName,clientSocket,clientAddress,playersObject)
        else:
            return 0
        
        return 1

    def challengeRequest(self,player1,player2,playersObject):
        self.uid = str(time.time())

        self.socket1,self.socket2 = playersObject.PlayersOnline[player1][0],playersObject.PlayersOnline[player2][0]

        self.socket1.send( "SERVER+%s+%s+%s" % (player2,playersObject.PlayersOnline[player2][1][0], self.uid) )

        self.socket2.send( "CLIENT+%s+%s+%s" % (player1,playersObject.PlayersOnline[player1][1][0], self.uid) )

        for s in self.SocketsToTrack:
            if s != self.serverSocket and s != self.socket1 and s != self.socket2:
                s.send("PLAYING+" + '+'.join([player1,player2]))

        playersObject.PlayersCurrentlyPlaying[(player1,player2)] = (True,self.uid) 

    def resultRequest(self,data,playersObject):
        
        print data
        if data.split('+')[1] == "DRAW":
            pass

        elif data.split('+')[1] == "ERROR":
            pass            

        elif data.split('+')[1] == "VICTORY":
            pass

        elif data.split('+')[1] == "DEFEAT":
            pass

        print data

        for s in self.SocketsToTrack:
            if s != self.serverSocket:
                s.send("ADD+" + data.split('+')[2])

    def Serve(self,playersObject):

        while 1:
            read,write,error = select(self.SocketsToTrack,[],[],0.1)

            for s in read:

                #new incoming connection request
                if s==self.serverSocket:
                    self.acceptNewPlayer(playersObject)

                #challenge or exit or GameOver request
                else:
                    temp = s.recv(RECV_BUFFER)  

                    print temp

                    if temp.split('+')[0] == "EXIT":
                        self.removePlayer(temp.split('+')[1],playersObject)
                    
                    elif temp.split('+')[0] == "CHALLENGE":
                        [self.user1,self.user2] = temp.split('+')[1:]
                        self.challengeRequest(self.user1, self.user2, playersObject)

                    elif temp.split('+')[0] == "RESULT":
                        self.resultRequest(temp,playersObject)
                time.sleep(0.2)

    def exit_(self):
        for s in self.SocketsToTrack:
            s.close()
        exit()

def main():
    playersData = PlayersState()
    mainServer = Server(playersData)
    mainServer.Serve(playersData)

if __name__ == "__main__":
    main()