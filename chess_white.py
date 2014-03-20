###################################################################
#   Created by: Sambhav Satija
#   Alias: Dark Ryder
#   For: Introduction to Programming Final Project Submission
#   Date: November, 2013
#   Insititute: IIIT-D
#   Version:  1.2
###################################################################


#---------------------!!----------------Initialisation----------------------!!---------------------------#


from sys import argv

import socket
from select import select

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER = argv[2]
PORT = 8900
RECV_BUFFER = 8192
NAME = argv[1]
AUTHENTICATION = str(hash(argv[3]))

# print SERVER

def quitGame(resign = False, opponent_resign = False):
    if resign:
        authenticateAndSend("RESIGN")
        print "RESIGN"
    elif opponent_resign:
        authenticateAndSend("VICTORY")
        print "OPPONENT_SURRENDERED"
    else:
        authenticateAndSend("EXIT")
        print "CLEANEXIT"
    

    clientSocket.close()

    pygame.quit()
    
    exit(0)

def authenticateAndSend(data):
    dataStream = '+'.join([AUTHENTICATION, data])
    clientSocket.send(dataStream)

def authenticateAndReceive():
    dataStream = clientSocket.recv(RECV_BUFFER)
    if dataStream.split('+')[0] == AUTHENTICATION:
        return '+'.join(dataStream.split('+')[1:])
    else: return 0

# print "MY NAME IS %s"%NAME
# print "OPENING SERVER AT %s at %s"%(str(SERVER),str(PORT))

serverSocket.bind((SERVER,PORT))
serverSocket.listen(1)
clientSocket, clientAddress = serverSocket.accept()

authenticateAndSend(NAME)

data = authenticateAndReceive()
if not data:
    print "OpponentNotAuthenticated"
    quitGame()
OPPONENT_NAME = data

# print NAME + ' vs ' + OPPONENT_NAME

import pygame
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
pygame.init()

console = False

size = [860,640] if console else [640,640]
font = pygame.font.Font(None, 40)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("%s VS %s"%(NAME,OPPONENT_NAME))
clock = pygame.time.Clock()

#---------------------!!---------All the Game Logic Methods----------!!---------------------------#


def cd(x,y):
    """takes input as coordinate number of box and outputs the required pixel numbers to print"""
    if x > 8 or y > 8 : return 0
    else: return ((x-1)*80 , (y-1)*80)

def checkBoundaryCondition(X1,Y1,X2,Y2):
    """checks boundary conditions and overlapping with self"""
    return ((1 <= X1 <= 8) and (1 <= Y1 <= 8) and (1 <= X2 <= 8) and (1 <= Y2 <= 8) and ((X1,Y1) != (X2,Y2)))

def checkStraightMovement(piece,dest_x,dest_y):                             
    """Returns a tuple of (movement possible, whether it will kill something)"""

    if ((piece.y-dest_y) and (piece.x-dest_x)): return (False,False)

    # filling tempLocations with places that piece will have to go through to reach destination
    if piece.y == dest_y: tempLocations = [(x,dest_y) for x in range(dest_x,piece.x) + range(piece.x+1,dest_x+1)]
    else:                 tempLocations = [(dest_x,y) for y in range(piece.y+1,dest_y+1) + range(dest_y,piece.y)]
    
    # we have to give preference to the fact there should not be any piece between destination and current position
    k=(True,False)
    for i in tempLocations:
        j = checkPositionToPieceDict(i)
        if (j):
            if (j.colour != piece.colour and (j.x,j.y) == (dest_x,dest_y)): k = (True,True)
            if j.colour == piece.colour or (j.colour != piece.colour and (j.x,j.y) != (dest_x,dest_y)): return (False,False)
    return k

def checkDiagonalMovement(piece,dest_x,dest_y):
    """Returns a tuple of (movement possible, it will have to kill something)"""

    if (piece.x == dest_x) or (piece.y == dest_y): return (False,False)                 #prevents zero division error
    if abs((float(piece.x) - dest_x) / (piece.y - dest_y)) != 1: return (False,False)

    XPositiveMove = True if (dest_x>piece.x) else False
    YPositiveMove = True if (dest_y>piece.y) else False

    # filling tempLocations with the places where the piece would have to go through to reach destination  
    if (XPositiveMove,YPositiveMove)   == (1,1):   tempLocations = [(piece.x+i,piece.y+i) for i in range(1,dest_x-piece.x+1)]
    elif (XPositiveMove,YPositiveMove) == (0,0):   tempLocations = [(piece.x-i,piece.y-i) for i in range(1,piece.x-dest_x+1)]
    elif (XPositiveMove,YPositiveMove) == (1,0):   tempLocations = [(piece.x+i,piece.y-i) for i in range(1,dest_x-piece.x+1)]
    elif (XPositiveMove,YPositiveMove) == (0,1):   tempLocations = [(piece.x-i,piece.y+i) for i in range(1,piece.x-dest_x+1)]

    # we have to give preference to the fact there should not be any piece between destination and current position
    k=(True,False)
    for i in tempLocations:
        j = checkPositionToPieceDict(i)
        if (j):
            if (j.colour != piece.colour and (j.x,j.y) == (dest_x,dest_y)): k = (True,True)
            if j.colour == piece.colour or (j.colour != piece.colour and (j.x,j.y) != (dest_x,dest_y)): return (False,False)
    return k

def moveAndKill(piece,dest_x,dest_y):
    """It does the following assuming logic is met:
        (1) kills the opponent piece
        (2) removes it from pieces_in_play and positionToPieceDict
        (3) checks if king is dead
        (4) moves the piece to destination
        (5) triggers the pawn_sacrificied event if needed
    """
    global pawnSacrificed
    j = checkPositionToPieceDict((dest_x,dest_y))
    if (j):
        j.survive = 0;
        pieces_in_play.remove(j)
        del positionToPieceDict[(j.x,j.y)]
        del legal_moves_dict[selectedPiece]
        del nameToPieceDict[j.name]
        if j.type == "king": kingKilled(j)
    del positionToPieceDict[(piece.x,piece.y)]
    piece.x = dest_x
    piece.y = dest_y
    positionToPieceDict[(piece.x,piece.y)] = piece

    if piece.type == "pawn" and piece.y in [1,8]: pawnSacrificed = True

    if j: sendData(piece, pieceKilled = j)
    else: sendData(piece)

    return True

def checkKnightMovement(piece,dest_x,dest_y):
    """What else should it do ?"""
    a = ((abs(piece.x-dest_x) == 2 and abs(piece.y-dest_y) == 1) or (abs(piece.x-dest_x) == 1 and abs(piece.y-dest_y) == 2))
    i = checkPositionToPieceDict((dest_x,dest_y))
    b = True
    if i:
        if i.colour == piece.colour: b = False
    return (a and b)

def refreshLegalMoves():
    """ keeps a track of all the moves allowed by all the pieces"""
    for p in pieces_in_play:
        tem = []
        for x_temp in range(1,9):
            for y_temp in range(1,9):
                if p.check(p.x,p.y,x_temp,y_temp):
                    tem.append((x_temp,y_temp))             
        legal_moves_dict[p] = tem

def createPositionToPieceDict():
    """Initialises the positionToPieceDict"""
    for p in pieces_in_play:
        positionToPieceDict[(p.x,p.y)] = p

def printValidMoves(selectedPiece):
    """prints a boundary over the boxes where moves are possible."""
    moves = legal_moves_dict[selectedPiece]
    for validmoves in moves:
        pygame.draw.rect(screen,blue,[cd(validmoves[0],validmoves[1])[0],cd(validmoves[0],validmoves[1])[1],80,80],3)

def printChessBoard():
    """Duhh..."""
    for a in range(0,481,160):                                  #Creates the chess background.
        for y in range(0,481,160):
            pygame.draw.rect(screen, white, [a,y,80,80])
    for a in range(80,561,160):
        for y in range(80,561,160):
            pygame.draw.rect(screen, white, [a,y,80,80])

def printPieces():
    """Duhh duuhh..."""
    for element in pieces_in_play:      
        screen.blit(element.image,(cd(element.x,element.y)[0],cd(element.x,element.y)[1]))

def checkPositionToPieceDict((x,y)):
    """For searching in postionToPieceDict. Returns a piece if on (x,y) else returns None"""
    try:
        return (positionToPieceDict[(x,y)])
    except KeyError:
        return None

def kingKilled(piece):
    """Declares winner and sends the signal to end the game"""
    win="white" if piece.colour=="black" else black
    
    pygame.draw.rect(screen,black if win=="white" else white,[160,240,320,160])
    screen.blit(wking.image if win=="white" else bking.image,(280,320))
    text=font.render(" White wins..!!" if win=="white" else "Black wins..", True, white)
    screen.blit(text, [220, 265])
    global gamewon
    gamewon=True    

def sendData(pieceMoved, pieceKilled = None, SpecialMove = None):
    data = ""
    data += '+'.join([pieceMoved.name,str(pieceMoved.x),str(pieceMoved.y)])

    if not pieceKilled: data += "+NONE"
    else:
        data += "+" + pieceKilled.name

    if not SpecialMove: data += "+NONE"
    else:
        pass

    # print "SENDING: ",data
    authenticateAndSend(data)

def receiveData():
    dataStream = authenticateAndReceive()

    if dataStream == "RESIGN":
        quitGame(opponent_resign = True)
    elif dataStream == "EXIT":
        quitGame()

    [pieceMovedName,pieceMoved_x,pieceMoved_y,killedPieceName,SpecialMove] = dataStream.split('+')

    if killedPieceName != "NONE":
        
        actualPiece = nameToPieceDict[killedPieceName]

        del positionToPieceDict[(actualPiece.x,actualPiece.y)]
        del legal_moves_dict[actualPiece]
        pieces_in_play.remove(actualPiece)


    if pieceMovedName:
    
        actualPiece = nameToPieceDict[pieceMovedName]
        
        del positionToPieceDict[(actualPiece.x,actualPiece.y)]

        actualPiece.x = int(pieceMoved_x)
        actualPiece.y = int(pieceMoved_y)

        positionToPieceDict[(actualPiece.x,actualPiece.y)] = actualPiece
        refreshLegalMoves()

    

    global colour
    colour = "white"

#-----------------!!-------------classes for all pieces--------------!!-------------------#

class Piece(object):
    """Parent Class for all the chess pieces"""
    def __init__(self,colour=None,type=None,x=None,y=None,n=None,imageSource=None):
        self.name = (str(colour) + str(type) + str(n))
        self.colour = colour
        self.type = type
        self.survive = True
        self.x = x
        self.y = y
        self.image = pygame.image.load(imageSource)

"""Each of the piece classes have a check method which checks whether
   the move is valid according to the piece movement rules"""

class WhitePawn(Piece):
    n=1
    def __init__(self):
        super(WhitePawn,self).__init__(colour="white",type="pawn",x=WhitePawn.n,y=2,n=WhitePawn.n,imageSource="./images/pawn.png")
        WhitePawn.n+=1

    def check(self,X1,Y1,X2,Y2):
        if not (checkBoundaryCondition(X1,Y1,X2,Y2)): return False
        if (Y2<=Y1): return False
        if (Y2-Y1>2): return False
        if (Y2-Y1==2) and self.y!=2: return False 

        i=checkStraightMovement(self,X2,Y2)
        if i==(1,0): return True
        
        if abs(X1-X2)==1 and (Y2-Y1==1):
            i=checkDiagonalMovement(self,X2,Y2)
            if i==(1,1): return True
        return False

class BlackPawn(Piece):
    n=1
    def __init__(self):
        super(BlackPawn,self).__init__(colour="black",type="pawn",x=BlackPawn.n,y=7,n=BlackPawn.n,imageSource="./images/pawn_b.png")
        BlackPawn.n+=1

    def check(self,X1,Y1,X2,Y2):
        if not (checkBoundaryCondition(X1,Y1,X2,Y2)): return False
        if (Y2>=Y1): return False
        if (Y1-Y2>2): return False
        if (Y1-Y2==2) and self.y!=7: return False 

        i=checkStraightMovement(self,X2,Y2)
        if i==(1,0): return True
        
        if abs(X1-X2)==1 and (Y1-Y2==1):
            i=checkDiagonalMovement(self,X2,Y2)
            if i==(1,1): return True
        return False

class BlackBishop(Piece):       
    n=1
    def __init__(self):
        super(BlackBishop,self).__init__(colour="black",type="bishop",x=3 if BlackBishop.n==1 else 6,y=8,n=BlackBishop.n,imageSource="./images/bishop_b.png")
        BlackBishop.n+=1

    def check(self,X1,Y1,X2,Y2):
        if not (checkBoundaryCondition(X1,Y1,X2,Y2)): return False
        if checkDiagonalMovement(self,X2,Y2)[0]==True: return True
        return False

class WhiteBishop(Piece):       
    n=1
    def __init__(self):
        super(WhiteBishop,self).__init__(colour="white",type="bishop",x=3 if WhiteBishop.n==1 else 6,y=1,n=WhiteBishop.n,imageSource="./images/bishop.png")
        WhiteBishop.n+=1

    def check(self,X1,Y1,X2,Y2):
        if not (checkBoundaryCondition(X1,Y1,X2,Y2)): return False
        if checkDiagonalMovement(self,X2,Y2)[0]==True: return True
        return False

class BlackRook(Piece):     
    n=1
    def __init__(self):
        super(BlackRook,self).__init__(colour="black",type="rook",x=1 if BlackRook.n==1 else 8,y=8,n=BlackRook.n,imageSource="./images/rook_b.png")
        BlackRook.n+=1
            
    def check(self,X1,Y1,X2,Y2):
        if not (checkBoundaryCondition(X1,Y1,X2,Y2)): return False
        if checkStraightMovement(self,X2,Y2)[0]==True: return True
        return False

class WhiteRook(Piece):     
    n=1
    def __init__(self):
        super(WhiteRook,self).__init__(colour="white",type="rook",x=1 if WhiteRook.n==1 else 8,y=1,n=WhiteRook.n,imageSource="./images/rook.png")
        WhiteRook.n+=1
            
    def check(self,X1,Y1,X2,Y2):
        if not (checkBoundaryCondition(X1,Y1,X2,Y2)): return False
        if checkStraightMovement(self,X2,Y2)[0]==True: return True
        return False

class BlackKnight(Piece):       
    n=1
    def __init__(self):
        super(BlackKnight,self).__init__(colour="black",type="knight",x=2 if BlackKnight.n==1 else 7,y=8,n=BlackKnight.n,imageSource="./images/knight_b.png")
        BlackKnight.n+=1
            
    def check(self,X1,Y1,X2,Y2):
        if not (checkBoundaryCondition(X1,Y1,X2,Y2)): return False
        if checkKnightMovement(self,X2,Y2): return True
        return False

class WhiteKnight(Piece):       
    n=1
    def __init__(self):
        super(WhiteKnight,self).__init__(colour="white",type="knight",x=2 if WhiteKnight.n==1 else 7,y=1,n=WhiteKnight.n,imageSource="./images/knight.png")
        WhiteKnight.n+=1
            
    def check(self,X1,Y1,X2,Y2):
        if not (checkBoundaryCondition(X1,Y1,X2,Y2)): return False
        if checkKnightMovement(self,X2,Y2): return True
        return False    

class BlackQueen(Piece):
    n=1       
    def __init__(self):
        super(BlackQueen,self).__init__(colour="black",type="queen",x=5,y=8,imageSource="./images/queen_b.png",n=BlackQueen.n)
        BlackQueen.n+=1

    def check(self,X1,Y1,X2,Y2):
        if not (checkBoundaryCondition(X1,Y1,X2,Y2)): return False
        if checkStraightMovement(self,X2,Y2)[0]==True: return True
        if checkDiagonalMovement(self,X2,Y2)[0]==True: return True
        return False

class WhiteQueen(Piece):
    n=1        
    def __init__(self):
        super(WhiteQueen,self).__init__(colour="white",type="queen",x=5,y=1,imageSource="./images/queen.png",n=WhiteQueen.n)
        WhiteQueen.n+=1
            
    def check(self,X1,Y1,X2,Y2):
        if not (checkBoundaryCondition(X1,Y1,X2,Y2)): return False
        if checkStraightMovement(self,X2,Y2)[0]==True: return True
        if checkDiagonalMovement(self,X2,Y2)[0]==True: return True
        return False

class BlackKing(Piece):     
    def __init__(self):
        super(BlackKing,self).__init__(colour="black",type="king",x=4,y=8,imageSource="./images/king_b.png")
                
    def check(self,X1,Y1,X2,Y2):
        if not(checkBoundaryCondition(X1,X2,Y1,Y2)): return False
        if not((abs(X1-X2)==1 and (abs(Y1-Y2)==1 or abs(Y1-Y2)==0)) or (abs(Y1-Y2)==1 and (abs(X1-X2)==1 or abs(X1-X2)==0))): return False
        if checkStraightMovement(self,X2,Y2)[0]==True or checkDiagonalMovement(self,X2,Y2)[0]==True: return True
        return False

class WhiteKing(Piece):     
    def __init__(self):
        super(WhiteKing,self).__init__(colour="white",type="king",x=4,y=1,imageSource="./images/king.png")
                
    def check(self,X1,Y1,X2,Y2):
        if not(checkBoundaryCondition(X1,X2,Y1,Y2)): return False
        if not((abs(X1-X2)==1 and (abs(Y1-Y2)==1 or abs(Y1-Y2)==0)) or (abs(Y1-Y2)==1 and (abs(X1-X2)==1 or abs(X1-X2)==0))): return False
        if checkStraightMovement(self,X2,Y2)[0]==True or checkDiagonalMovement(self,X2,Y2)[0]==True: return True
        return False

#---------------------!!--------------Creates objects for all pieces-----------------!!--------------------------#

wp1,wp2,wp3,wp4,wp5,wp6,wp7,wp8=(WhitePawn() for x in range(8))             #
bp1,bp2,bp3,bp4,bp5,bp6,bp7,bp8=(BlackPawn() for x in range(8))             #
bb1,bb2=(BlackBishop() for x in range(2))                                   #
wb1,wb2=(WhiteBishop() for x in range(2))                                   #
br1,br2=(BlackRook() for x in range(2))                                     # Initialising all objects
wr1,wr2=(WhiteRook() for x in range(2))                                     # and giving them the attributes
bk1,bk2=(BlackKnight() for x in range(2))                                   #
wk1,wk2=(WhiteKnight() for x in range(2))                                   #
bq1=BlackQueen()                                                            #
wq1=WhiteQueen()                                                            #
bking=BlackKing()                                                           #
wking=WhiteKing()                                                           #


#pieces in play is list of all the pieces alive.
pieces_in_play=[wp1,wp2,wp3,wp4,wp5,wp6,wp7,wp8,bp1,bp2,bp3,bp4,bp5,bp6,bp7,bp8,bb1,bb2,wb1,wb2,br1,br2,wr1,wr2,bk1,bk2,wk1,wk2,bq1,wq1,bking,wking]

positionToPieceDict={}      # This stores a hash map from all the co-ordinates to the pieces on them
createPositionToPieceDict() # initialise positionToPieceDict

nameToPieceDict = {}
for piece in pieces_in_play:           # Create the nameToPieceDictionary
    nameToPieceDict[piece.name] = piece

legal_moves_dict={}         # stores the legal moves co-ordinates in front of all pieces in play
refreshLegalMoves()         # initialise legal_moves_dict

colour="white"              #Current colour which has to make a move
m=[]                        # stores current co-ordinate inputs from mouse until its not recieved 2 valid inputs
pressed=False               # I have to keep a track if the button is kept pressed after the 1 cycle without getting lifted. MOST PROBABLY A BUG
gamewon=False               # flag for continuing the game
pawnSacrificed=False

#-----------------!!-------------Main Program Loop--------------!!-------------------#

while not gamewon:
    
    input_read=False
    
# -------- Handles input from the user -----------
    if len(m)==4:
        X1,Y1,X2,Y2 = m                         # assigning final co-ordinates
        m=[]                                    # empty the buffer input list
        input_read=True

    if not input_read:                              
        events=pygame.event.get()                   
        for event in events:

            if event.type == pygame.QUIT:       # Quitting
                quitGame(resign = True)

            if colour == "white":
                if event.type == pygame.MOUSEBUTTONUP: pressed= False       # get ready for next click
                if event.type ==  pygame.MOUSEBUTTONDOWN and not pressed:
                    pressed=True
                    if event.button == 1:
                        if len(m) == 2:                                       # add second click co-ordinates
                            pos = pygame.mouse.get_pos()    
                            x = pos[0]/80+1
                            y = pos[1]/80+1
                            m.extend([x,y])

                        else:
                            pos = pygame.mouse.get_pos()                    # add first click co-ordinates
                            x = pos[0]/80+1
                            y = pos[1]/80+1
                            j=checkPositionToPieceDict((x,y))               # Checks that the first click has a piece
                            if j:                                           # of your colour and selects it.
                                if j.colour == colour:
                                    selectedPiece = j
                                    m.extend([x,y])
                            if pawnSacrificed: m.extend([x,y])


        r,w,x = select([clientSocket],[],[],0.001)
        if r!=[]:
            receiveData()

# -------- Authenticates and moves the piece -----------
    if input_read == 1 and not pawnSacrificed:
        if (X2,Y2) in legal_moves_dict[selectedPiece]:              
            moveAndKill(selectedPiece,X2,Y2)
            colour = "black" if colour == "white" else "white"
            refreshLegalMoves()

# -------- Printing -----------
    screen.fill(black)
    printChessBoard()
    printPieces()
    if len(m) == 2:
        # creates the boundary of currently selected piece
        pygame.draw.rect(screen,red,[cd(m[0],m[1])[0],cd(m[0],m[1])[1],80,80],3)        
        printValidMoves(selectedPiece)
    
    if pawnSacrificed:
        """Pawn Sacrifice Event Chooser"""
        pygame.draw.rect(screen,(100,50,25),[160,240,320,160])
        screen.blit(vars(bq1)['image'] if selectedPiece.colour == "black" else vars(wq1)['image'],(160,320))
        screen.blit(vars(br1)['image'] if selectedPiece.colour == "black" else vars(wr1)['image'],(240,320))
        screen.blit(vars(bb1)['image'] if selectedPiece.colour == "black" else vars(wb1)['image'],(320,320))
        screen.blit(vars(bk1)['image'] if selectedPiece.colour == "black" else vars(wk1)['image'],(400,320))
        text = font.render(" Please choose a piece",True,white)
        screen.blit(text,[160,265])

        if len(m) == 2:

            """Creates a new object of the chosen piece and removes all traces of pawn"""
            x1,y1 = m
            m = []
            (x_temp,y_temp) = (selectedPiece.x,selectedPiece.y)
            pieces_in_play.remove(selectedPiece)
            del legal_moves_dict[selectedPiece]
            del positionToPieceDict[(selectedPiece.x,selectedPiece.y)]

            if (x1,y1) == (5,5): selectedPiece = WhiteBishop() if selectedPiece.colour == "white" else BlackBishop()
            elif (x1,y1) == (4,5): selectedPiece = WhiteRook() if selectedPiece.colour == "white" else BlackRook()
            elif (x1,y1) == (6,5): selectedPiece = WhiteKnight() if selectedPiece.colour == "white" else BlackKnight()
            elif (x1,y1) == (3,5): selectedPiece = WhiteQueen() if selectedPiece.colour == "white" else BlackQueen()
            else: 
                pawnSacrificed = True
                continue
            (selectedPiece.x,selectedPiece.y) = (x_temp,y_temp)
            pieces_in_play.append(selectedPiece)
            positionToPieceDict[(x_temp,y_temp)] = selectedPiece

            refreshLegalMoves()
            
            pawnSacrificed = False

# -------- Console -----------
    if console:
        pygame.draw.rect(screen,(100,50,25),[645,0,240,640])
        pygame.draw.rect(screen,(50,15,0),[640,0,5,640])
        screen.blit(font.render("Pieces Lost", True, black),[670,20])


    pygame.display.flip()
    clock.tick(50)

# -------- Exiting -----------
    if gamewon:
        from time import sleep
        sleep(3)
        quitGame()
        # Close the window and quit.
quitGame()