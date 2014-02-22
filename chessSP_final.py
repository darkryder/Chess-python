###################################################################
#	Created by: Sambhav Satija
#	Alias: Dark Ryder
#	For: Introduction to Programming Final Project Submission
#	Date: November, 2013
#	Insititute: IIIT-D
###################################################################

#---------------------!!----------------Initialisation----------------------!!---------------------------#
import pygame
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
pygame.init()

size = [860,640] #for using without console[640,640]
font = pygame.font.Font(None, 40)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Chess")

clock = pygame.time.Clock()

done = False
gamewon=0
"""
import time
time_change_var=time.asctime().split()[3].split(":")[2]
time_elapsed=0
"""


killcount_wp=0
killcount_wb=0
killcount_wr=0
killcount_wk=0
killcount_wq=0
killcount_bp=0
killcount_bb=0
killcount_br=0
killcount_bk=0
killcount_bq=0



"""
I had to implement the function to keep a track of the pieces killed. 
As the inbuilt check function of the pieces automatically kill the opponents 
piece. It was the easiest way to implement the feature of keeping a 
track of the killed pieces without changing a huge amount of code.
"""

def killcount(piece,kill=True):
	global killcount_wp
	global killcount_wb
	global killcount_wr
	global killcount_wk
	global killcount_wq
	global killcount_bp
	global killcount_bb
	global killcount_br
	global killcount_bk
	global killcount_bq
	if kill==True:
		if piece.colour==0:
			if piece.type==1:
				killcount_bp+=1
			if piece.type==2:
				killcount_bb+=1
			if piece.type==3:
				killcount_br+=1
			if piece.type==4:
				killcount_bk+=1
			if piece.type==5:
				killcount_bq+=1
		if piece.colour==1:
			if piece.type==1:
				killcount_wp+=1
			if piece.type==2:
				killcount_wb+=1
			if piece.type==3:
				killcount_wr+=1
			if piece.type==4:
				killcount_wk+=1
			if piece.type==5:
				killcount_wq+=1
	else:
		if piece.colour==0:
			if piece.type==1:
				killcount_bp-=1
			if piece.type==2:
				killcount_bb-=1
			if piece.type==3:
				killcount_br-=1
			if piece.type==4:
				killcount_bk-=1
			if piece.type==5:
				killcount_bq-=1
		if piece.colour==1:
			if piece.type==1:
				killcount_wp-=1
			if piece.type==2:
				killcount_wb-=1
			if piece.type==3:
				killcount_wr-=1
			if piece.type==4:
				killcount_wk-=1
			if piece.type==5:
				killcount_wq-=1


#-----------------!!-------------classes for all pieces--------------!!-------------------#

def cd(x,y):	#takes input as coordinate number of box and outputs the required pixel numbers to print
	if x>8 or y>8:
		return 0
	else:
		return ((x-1)*80,(y-1)*80)	

	
class WhitePawn(object):				#ALL CLASSES HAVE ATTRIBUTES AND REQUIRED LOGICS
		n=1
		def __init__(self):
			self.name=int("1"+str(WhitePawn.n)+"1")
			self.colour = 1
			self.type = 1
			self.survive = 1
			self.y=2
			self.x=WhitePawn.n
			WhitePawn.n += 1
			self.image = pygame.image.load("./images/pawn.png")
	
		def check(self,X1,Y1,X2,Y2):


			if (1<=X1<=8 and 1<=Y1<=8 and 1<=X2<=8 and 1<=Y2<=8):
				if X1==X2:
					if (Y2==Y1+1 or (Y1==2 and Y2==Y1+2)):
						for t in pieces_in_play:
							if t!= self:
								if t.y==3 and t.x==X1 and self.y==2:
									return 0
								if t.x==X2 and t.y==Y2:
									
									return 0
						else: 
							return 1
				if (X2==X1-1 or X2==X1+1) and Y2==Y1+1:					#diagonal implementation
					for t in pieces_in_play:
						if t.x==X2 and t.y==Y2:
							if t.colour==0:
								t.survive=0
								killcount(t)
								return 1

				else:
					return 0
			else:
				return -1

class BlackPawn(object):		#ALL CLASSES HAVE ATTRIBUTES OF NAME, COLOUR, TYPE, SURVIVE, X,Y, IMAGE SOURCE
		n=1
		def __init__(self):
			self.name=int("1"+str(BlackPawn.n)+"0")
			self.colour = 0
			self.type = 1
			self.survive = 1
			self.y=7
			self.x=BlackPawn.n
			BlackPawn.n += 1
			self.image = pygame.image.load("./images/pawn_b.png")
			
		def check(self,X1,Y1,X2,Y2):
		
			if (1<=X1<=8 and 1<=Y1<=8 and 1<=X2<=8 and 1<=Y2<=8):
				if X1==X2:
					if (Y2==Y1-1 or (Y1==7 and Y2==Y1-2)):
						for t in pieces_in_play:
							if t!= self:
								if t.y==6 and t.x==X1 and self.y==7:
									return 0
								if t.x==X2 and t.y==Y2:
									
									return 0
						else: 
							return 1
				if (X2==X1-1 or X2==X1+1) and Y2==Y1-1:					#diagonal implementation
					for t in pieces_in_play:
						if t.x==X2 and t.y==Y2:
							if t.colour==1:
								t.survive=0
								killcount(t)
								return 1
				
				else:
					return 0
			else:
				return -1

class BlackBishop(object):		
		n=1
		def __init__(self):
			self.name=int("2"+str(BlackBishop.n)+"0")
			self.colour = 0
			self.type = 2
			self.survive = 1
			self.y=8
			if BlackBishop.n==1:	
				self.x=3
			else:
				self.x=6
			BlackBishop.n += 1
			self.image = pygame.image.load("./images/bishop_b.png")
			
		def check(self,X1,Y1,X2,Y2):

			if (1<=X1<=8 and 1<=Y1<=8 and 1<=X2<=8 and 1<=Y2<=8):
				if abs(Y2-Y1)==abs(X2-X1):
					m=(Y2-Y1)/(X2-X1)
					q=[]
					t=[]
					if X2>X1:
						x=X1
						if Y2>Y1:
							y=Y1
							q.append((x,y))
							while (x!=X2 and y!=Y2)and(x>0 and y>0):
								x+=1
								y+=1
								q.append((x,y))
								
						else:
							y=Y1
							q.append((x,y))
							while (x!=X2 and y!=Y2)and(x>0 and y>0):
								x+=1
								y-=1
								q.append((x,y))
								
					else:
						x=X1
						if Y2>Y1:
							y=Y1
							q.append((x,y))
							while (x!=X2 and y!=Y2)and(x>0 and y>0):
								x-=1
								y+=1
								q.append((x,y))
								
						else:
							y=Y1
							q.append((x,y))
							while(x!=X2 and y!=Y2)and(x>0 and y>0):
								x-=1
								y-=1
								q.append((x,y))
								
					for coordinate in q:
						for check_piece in pieces_in_play:
							if coordinate==(check_piece.x,check_piece.y):
								if check_piece!=self:
									if check_piece.colour==0:
										return 0
									elif check_piece.colour==1 and coordinate==(X2,Y2):
										check_piece.survive=0
										killcount(check_piece)
										return 1
									else:
										return 0
					else:
						return 1
				else:
					return 0
			else:
				return -1

class WhiteBishop(object):		
		n=1
		def __init__(self):
			self.name=int("2"+str(WhiteBishop.n)+"1")
			self.colour = 1
			self.type = 2
			self.survive = 1
			self.y=1
			if WhiteBishop.n==1:
				self.x=3
			else:
				self.x=6
			WhiteBishop.n += 1
			self.image = pygame.image.load("./images/bishop.png")
			
		def check(self,X1,Y1,X2,Y2):
			
			if (1<=X1<=8 and 1<=Y1<=8 and 1<=X2<=8 and 1<=Y2<=8):
				if abs(Y2-Y1)==abs(X2-X1):
					m=(Y2-Y1)/(X2-X1)
					q=[]
					t=[]
					if X2>X1:
						x=X1
						if Y2>Y1:
							y=Y1
							q.append((x,y))
							while (x!=X2 and y!=Y2)and(x>0 and y>0):
								x+=1
								y+=1
								q.append((x,y))
								
						else:
							y=Y1
							q.append((x,y))
							while (x!=X2 and y!=Y2)and(x>0 and y>0):
								x+=1
								y-=1
								q.append((x,y))
								
					else:
						x=X1
						if Y2>Y1:
							y=Y1
							q.append((x,y))
							while (x!=X2 and y!=Y2)and(x>0 and y>0):
								x-=1
								y+=1
								q.append((x,y))
									
						else:
							y=Y1
							q.append((x,y))
							while(x!=X2 and y!=Y2)and(x>0 and y>0):
								x-=1
								y-=1
								q.append((x,y))
								
					for coordinate in q:
						for check_piece in pieces_in_play:
							if coordinate==(check_piece.x,check_piece.y):
								if check_piece!=self:
									if check_piece.colour==1:
										return 0
									elif check_piece.colour==0 and coordinate==(X2,Y2):
										check_piece.survive=0
										killcount(check_piece)
										return 1
									else:
										return 0
					else:
						return 1
				else:
					return 0
			else:
				return -1

class BlackRook(object):		
		n=1
		def __init__(self):
			self.name=int("3"+str(BlackRook.n)+"0")
			self.colour = 0
			self.type = 3
			self.survive = 1
			self.y=8
			if BlackRook.n==1:
				self.x=1
			else:
				self.x=8
			BlackRook.n += 1
			self.image = pygame.image.load("./images/rook_b.png")
			
		def check(self,X1,Y1,X2,Y2):
			
			if (1<=X1<=8 and 1<=Y1<=8 and 1<=X2<=8 and 1<=Y2<=8):
				if (X2==X1):
					if Y1<Y2:
						q=[]
						for y_check in range(Y1,Y2+1):
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(X1,y_check):
										q.append(check_piece)
									
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==1 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0					
					
					else:
						q=[]
						for y_check in range(Y2,Y1+1):
							
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(X1,y_check):
										q.append(check_piece)
									
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==1 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0
					
					
				if (Y2==Y1):
					if X1<X2:
						q=[]
						for x_check in range(X1,X2+1):
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(x_check,Y1):
										q.append(check_piece)
										
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==1 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0					

					else:
						q=[]
						for x_check in range(X2,X1+1):
							
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(x_check,Y1):
										q.append(check_piece)
									
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==1 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0
				
			
			
			else:
				return 0

class WhiteRook(object):		
		n=1
		def __init__(self):
			self.name=int("3"+str(WhiteRook.n)+"1")
			self.colour = 1
			self.type = 3
			self.survive = 1
			self.y=1
			if WhiteRook.n==1:
				self.x=1
			else:
				self.x=8
			WhiteRook.n += 1
			self.image = pygame.image.load("./images/rook.png")
			
		def check(self,X1,Y1,X2,Y2):

			if (1<=X1<=8 and 1<=Y1<=8 and 1<=X2<=8 and 1<=Y2<=8):
				if (X2==X1):
					if Y1<Y2:
						q=[]
						for y_check in range(Y1,Y2+1):
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(X1,y_check):
										q.append(check_piece)
									
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==0 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0					
					
					else:
						q=[]
						for y_check in range(Y2,Y1+1):
							
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(X1,y_check):
										q.append(check_piece)
									
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==0 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0
					
					
				if (Y2==Y1):
					if X1<X2:
						q=[]
						for x_check in range(X1,X2+1):
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(x_check,Y1):
										q.append(check_piece)
										
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==0 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0					

					else:
						q=[]
						for x_check in range(X2,X1+1):
							
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(x_check,Y1):
										q.append(check_piece)
									
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==0 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0
				
			
			
			else:
				return 0

class BlackKnight(object):		
		n=1
		def __init__(self):
			self.name=int("4"+str(BlackKnight.n)+"0")
			self.colour = 0
			self.type = 4
			self.survive = 1
			self.y=8
			self.image = pygame.image.load("./images/knight_b.png")
			if BlackKnight.n==1:
				self.x=2
			else:
				self.x=7
			BlackKnight.n += 1
			
		def check(self,X1,Y1,X2,Y2):
			
			if (1<=X1<=8 and 1<=Y1<=8 and 1<=X2<=8 and 1<=Y2<=8):
				if (abs(Y2-Y1)==2 and abs (X2-X1)==1) or (abs(Y2-Y1)==1 and abs(X2-X1)==2):
					for check_piece in pieces_in_play:
						if check_piece!=self:
							if (check_piece.x,check_piece.y)==(X2,Y2):
								if check_piece.colour==0:
									return 0
								if check_piece.colour==1:
									check_piece.survive=0
									killcount(check_piece)
									return 1
					else:
						return 1
				else:
					return 0
			else:
				return 0

class WhiteKnight(object):		
		n=1
		def __init__(self):
			self.name=int("4"+str(WhiteKnight.n)+"1")
			self.colour = 1
			self.type = 4
			self.survive = 1
			self.y=1
			self.image = pygame.image.load("./images/knight.png")
			if WhiteKnight.n==1:
				self.x=2
			else:
				self.x=7
			WhiteKnight.n += 1
			
		def check(self,X1,Y1,X2,Y2):
			
			if (1<=X1<=8 and 1<=Y1<=8 and 1<=X2<=8 and 1<=Y2<=8):
				if (abs(Y2-Y1)==2 and abs (X2-X1)==1) or (abs(Y2-Y1)==1 and abs(X2-X1)==2):
					for check_piece in pieces_in_play:
						if check_piece!=self:
							if (check_piece.x,check_piece.y)==(X2,Y2):
								if check_piece.colour==1:
									return 0
								if check_piece.colour==0:
									check_piece.survive=0
									killcount(check_piece)
									return 1
					else:
						return 1
				else:
					return 0
			else:
				return 0
					
class BlackQueen(object):		
		n=1
		def __init__(self):
			self.name=int("5"+str(BlackQueen.n)+"0")
			self.colour = 0
			self.type = 5
			self.survive = 1
			self.y=8
			self.image = pygame.image.load("./images/queen_b.png")
			self.x=5
			BlackQueen.n += 1
			
		def check(self,X1,Y1,X2,Y2):
			
			if (1<=X1<=8 and 1<=Y1<=8 and 1<=X2<=8 and 1<=Y2<=8):
				if (X2==X1):
					if Y1<Y2:
						q=[]
						for y_check in range(Y1,Y2+1):
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(X1,y_check):
										q.append(check_piece)
									
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==1 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0					
					
					else:
						q=[]
						for y_check in range(Y2,Y1+1):
							
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(X1,y_check):
										q.append(check_piece)
									
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==1 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0
					
					
				if (Y2==Y1):
					if X1<X2:
						q=[]
						for x_check in range(X1,X2+1):
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(x_check,Y1):
										q.append(check_piece)
										
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==1 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0					

					else:
						q=[]
						for x_check in range(X2,X1+1):
							
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(x_check,Y1):
										q.append(check_piece)
									
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==1 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0
				
				if abs(Y2-Y1)==abs(X2-X1):
					m=(Y2-Y1)/(X2-X1)
					q=[]
					t=[]
					if X2>X1:
						x=X1
						if Y2>Y1:
							y=Y1
							q.append((x,y))
							while (x!=X2 and y!=Y2)and(x>0 and y>0):
								x+=1
								y+=1
								q.append((x,y))
								
						else:
							y=Y1
							q.append((x,y))
							while (x!=X2 and y!=Y2)and(x>0 and y>0):
								x+=1
								y-=1
								q.append((x,y))
								
					else:
						x=X1
						if Y2>Y1:
							y=Y1
							q.append((x,y))
							while (x!=X2 and y!=Y2)and(x>0 and y>0):
								x-=1
								y+=1
								q.append((x,y))
							
						else:
							y=Y1
							q.append((x,y))
							while(x!=X2 and y!=Y2)and(x>0 and y>0):
								x-=1
								y-=1
								q.append((x,y))
							
					for coordinate in q:
						for check_piece in pieces_in_play:
							if coordinate==(check_piece.x,check_piece.y):
								if check_piece!=self:
									if check_piece.colour==0:
										return 0
									elif check_piece.colour==1 and coordinate==(X2,Y2):
										check_piece.survive=0
										killcount(check_piece)
										return 1
									else:
										return 0
					else:
						return 1
				
				
			else:
				return 0
		
class WhiteQueen(object):		
		n=1
		def __init__(self):
			self.name=int("5"+str(WhiteQueen.n)+"1")
			self.colour = 1
			self.type = 5
			self.survive = 1
			self.y=1
			self.image = pygame.image.load("./images/queen.png")
			self.x=5
			WhiteQueen.n += 1
			
		def check(self,X1,Y1,X2,Y2):
			
			if (1<=X1<=8 and 1<=Y1<=8 and 1<=X2<=8 and 1<=Y2<=8):
				if (X2==X1):
					if Y1<Y2:
						q=[]
						for y_check in range(Y1,Y2+1):
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(X1,y_check):
										q.append(check_piece)
									
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==0 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])

							return 1
						else: return 0					
					
					else:
						q=[]
						for y_check in range(Y2,Y1+1):
							
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(X1,y_check):
										q.append(check_piece)
									
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==0 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0
					
					
				if (Y2==Y1):
					if X1<X2:
						q=[]
						for x_check in range(X1,X2+1):
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(x_check,Y1):
										q.append(check_piece)
										
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==0 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0					

					else:
						q=[]
						for x_check in range(X2,X1+1):
							
							for check_piece in pieces_in_play:
								if check_piece!=self:	
									if (check_piece.x,check_piece.y)==(x_check,Y1):
										q.append(check_piece)
									
						if q==[]:
							return 1
						if len(q)>=2: return 0
						if q[0].colour==0 and (q[0].x==X2 and q[0].y==Y2):
							q[0].survive=0
							killcount(q[0])
							return 1
						else: return 0
				
				if abs(Y2-Y1)==abs(X2-X1):
					m=(Y2-Y1)/(X2-X1)
					q=[]
					t=[]
					if X2>X1:
						x=X1
						if Y2>Y1:
							y=Y1
							q.append((x,y))
							while (x!=X2 and y!=Y2)and(x>0 and y>0):
								x+=1
								y+=1
								q.append((x,y))
								
						else:
							y=Y1
							q.append((x,y))
							while (x!=X2 and y!=Y2)and(x>0 and y>0):
								x+=1
								y-=1
								q.append((x,y))
								
					else:
						x=X1
						if Y2>Y1:
							y=Y1
							q.append((x,y))
							while (x!=X2 and y!=Y2)and(x>0 and y>0):
								x-=1
								y+=1
								q.append((x,y))
								
						else:
							y=Y1
							q.append((x,y))
							while(x!=X2 and y!=Y2)and(x>0 and y>0):
								x-=1
								y-=1
								q.append((x,y))
								
					for coordinate in q:
						for check_piece in pieces_in_play:
							if coordinate==(check_piece.x,check_piece.y):
								if check_piece!=self:
									if check_piece.colour==1:
										return 0
									elif check_piece.colour==0 and coordinate==(X2,Y2):
										check_piece.survive=0
										killcount(check_piece)
										return 1
									else:
										return 0
					else:
						return 1
				
				
			else:
				return 0

class BlackKing(object):		
		def __init__(self):
			self.name=610
			self.colour = 0
			self.type = 6
			self.survive = 1
			self.y=8
			self.x=4
			self.image = pygame.image.load("./images/king_b.png")
			
		def check(self,X1,Y1,X2,Y2):
			
			if (1<=X1<=8 and 1<=Y1<=8 and 1<=X2<=8 and 1<=Y2<=8):
				n=-1
				if (X1==X2 and (Y2==Y1-1 or Y2==Y1+1)) or (Y1==Y2 and (X2==X1-1 or X2==X1+1)):
					n = 1
				elif (X2==X1+1 and(Y2==Y1-1 or Y2==Y1+1)) or (X2==X1-1 and(Y2==Y1-1 or Y2==Y1+1)):
					n = 1
				else:
					return 0
				if n==1:
					q=[]
					for check_piece in pieces_in_play:
						if check_piece!=self:
							if (check_piece.x,check_piece.y)==(X2,Y2):
								q.append(check_piece)
							
					if len(q)==0:
						return 1
					else:						
						if q[0].colour==0:
							return 0
						if q[0].colour==1:
							q[0].survive=0
							killcount(q[0])
							return 1
			else:
				return 0

class WhiteKing(object):		
		def __init__(self):
			self.name=611
			self.colour = 1
			self.type = 6
			self.survive = 1
			self.y=1
			self.x=4
			self.image = pygame.image.load("./images/king.png")
			
		def check(self,X1,Y1,X2,Y2):
		
			if (1<=X1<=8 and 1<=Y1<=8 and 1<=X2<=8 and 1<=Y2<=8):
				n=-1
				if (X1==X2 and (Y2==Y1-1 or Y2==Y1+1)) or (Y1==Y2 and (X2==X1-1 or X2==X1+1)):
					n = 1
				elif (X2==X1+1 and(Y2==Y1-1 or Y2==Y1+1)) or (X2==X1-1 and(Y2==Y1-1 or Y2==Y1+1)):
					n = 1
				else:
					return 0
				if n==1:
					q=[]
					for check_piece in pieces_in_play:
						if check_piece!=self:
							if (check_piece.x,check_piece.y)==(X2,Y2):
								q.append(check_piece)
							
					if len(q)==0:
						return 1
					else:						
						if q[0].colour==1:
							return 0
						if q[0].colour==0:
							q[0].survive=0
							killcount(q[0])
							return 1
			else:
				return 0


#---------------------!!--------------Creates objects for all pieces-----------------!!--------------------------#

wp1,wp2,wp3,wp4,wp5,wp6,wp7,wp8=(WhitePawn() for x in range(8))				#
bp1,bp2,bp3,bp4,bp5,bp6,bp7,bp8=(BlackPawn() for x in range(8))				#
bb1,bb2=(BlackBishop() for x in range(2))									#
wb1,wb2=(WhiteBishop() for x in range(2))									#
br1,br2=(BlackRook() for x in range(2))										# Initialising all objects
wr1,wr2=(WhiteRook() for x in range(2))										# and giving them the attributes
bk1,bk2=(BlackKnight() for x in range(2))									#
wk1,wk2=(WhiteKnight() for x in range(2))									#
bq1=BlackQueen()															#
wq1=WhiteQueen()															#
bking=BlackKing()															#
wking=WhiteKing()															#

#pieces in play is list of all the pieces alive.
pieces_in_play=[wp1,wp2,wp3,wp4,wp5,wp6,wp7,wp8,bp1,bp2,bp3,bp4,bp5,bp6,bp7,bp8,bb1,bb2,wb1,wb2,br1,br2,wr1,wr2,bk1,bk2,wk1,wk2,bq1,wq1,bking,wking]

t_x = 0				# CHECK IF THE "SACRIFICE PAWN FOR A NEW PIECE" EVENT IS TRIGGERED
x1=0 				#co-ordinate inputs from mouse
y1=0
x2=0
col=1 				#Current colour which has to make a move
X1=0
Y1=0
m=[] 				#stores current co-ordinate inputs from mouse until its not recieved 2 valid inputs
moves=[]

legal_moves_refreshed=0 	#bool



# -------- Main Program Loop -----------
while done == False:
	
	screen.fill(black)
	
	
	input_read=0	
	
	if len(m)==4:
		X1=m[0]							#assigning final inputs
		Y1=m[1]
		X2=m[2]
		Y2=m[3]
		m=[] 							# empty the buffer input list
		input_read=1

	if not input_read:								
		event=pygame.event.wait()					# User did something
		if event.type == pygame.QUIT: 				# If user clicked close
			done = True 							# exit this loop
		if event.type ==  pygame.MOUSEBUTTONDOWN:	#taking input
			if len(m)==2:
				if event.button==1:
					x1,y1=-1,-1
					pos = pygame.mouse.get_pos()	
					x2 = pos[0]/80+1                                            #
					y2 = pos[1]/80+1
					m += [x2] + [y2]
					moves=[]
					
			else:
				if event.button==1:
					pos = pygame.mouse.get_pos()
					x1 = pos[0]/80+1
					y1 = pos[1]/80+1
					for elements in pieces_in_play:
						if x1 == elements.x and y1 == elements.y:
							if elements.colour==col:
								f=elements
								m += [x1] + [y1]




	for a in range(0,481,160):									#Creates the chess background.
		for y in range(0,481,160):
			pygame.draw.rect(screen, white, [a,y,80,80])
	for a in range(80,561,160):
		for y in range(80,561,160):
			pygame.draw.rect(screen, white, [a,y,80,80])
	
	
	
	pygame.draw.rect(screen,red,[cd(x1,y1)[0],cd(x1,y1)[1],80,80],5)	 	# creates the boundary of currently selected piece

	if not legal_moves_refreshed:										# keeps a track of all the moves allowed by all the pieces
		legal_moves_dict={}			
		for p in pieces_in_play:
			tem=[]
			for x_temp in range(1,9):
				for y_temp in range(1,9):
					try:
						if p.check(p.x,p.y,x_temp,y_temp):				#checks if it is possible for the player to move at all the locations and stores all the locations
							if (p.x,p.y)!=(x_temp,y_temp):
								tem+=[(x_temp,y_temp)]
								for a in pieces_in_play:
									#if it is possible to kill the other opponent. My function automatically kills the opponent while checking for valid moves. 
									#Hence I had to make the kill_count function to ensure that the opponent stays alive even 
									#when his box is checked for a possible move.
									if (a.x,a.y)==(x_temp,y_temp):		
										a.survive=1
										killcount(a,kill=False)
					except ZeroDivisionError:
						pass
			legal_moves_dict[p]=tem
		legal_moves_refreshed=1		
		

	if input_read==1:
		move=1
		for element in pieces_in_play:
			if (element.x==X2 and element.y==Y2):
				if element.colour==col:						# Checks that input has a piece on it of your colour
					move=0
	
				
			
			
		if move==1:
			if f.check(X1,Y1,X2,Y2):						#MOVES THE PIECE TO NEW LOCATION AFTER CHECKING LEGAL MOVE
			# if (X2,Y2) in legal_moves_dict[f]:				
				f.x=X2
				f.y=Y2
				if col==0: col=1
				else: col=0
				legal_moves_refreshed=0
		

		#CHECKS FOR THE "sacrifice pawn for other piece" EVENT
		if f.type==1 and f.y==8 and f.colour==1:
			t_x = 1
			f.survive=0
	

		if f.type==1 and f.y==1 and f.colour==0:
			t_x = 2
			f.survive=0

	if input_read==1:
		temp=[]													#
		for element in pieces_in_play:							# creates list of pieces_in_play
			if (element.survive==1):							#
				temp.append(element)							#
		pieces_in_play=temp[:]

		

	
	for element in pieces_in_play:																# PRINTS IMAGES ON
		screen.blit(element.image,(cd(element.x,element.y)[0],cd(element.x,element.y)[1]))		#    THE SCREEN
	

	#You have to KILL the king to win the game
	if bking not in pieces_in_play:
		pygame.draw.rect(screen,black,[160,240,320,160])
		screen.blit(wking.image,(280,320))
		text=font.render(" White wins..!!", True, white)
		screen.blit(text, [220, 265])
		gamewon=True

	if wking not in pieces_in_play:
		pygame.draw.rect(screen,white,[160,240,320,160])
		screen.blit(bking.image,(280,320))
		text=font.render(" Black wins..!!", True, black)
		screen.blit(text, [220, 265])
		gamewon=True

	#sacrifice pawn event
	if t_x == 1:
		if not gamewon:
			pygame.draw.rect(screen,(100,50,25),[160,240,320,160])
			screen.blit(wq1.image,(160,320))
			screen.blit(wr1.image,(240,320))
			screen.blit(wb1.image,(320,320))
			screen.blit(wk1.image,(400,320))
			text=font.render(" Please choose a piece", True, white)
			screen.blit(text, [160, 265])
		
			if x1==5 and y1==5:
				wb3=WhiteBishop()
				wb3.x,wb3.y=X2,Y2
				pieces_in_play += [wb3]
				t_x = 0
			if x1==4 and y1==5:
				wr3=WhiteRook()
				wr3.x,wr3.y=X2,Y2
				pieces_in_play += [wr3]
				t_x = 0
			if x1==6 and y1==5:
				wk3=WhiteKnight()
				wk3.x,wk3.y=X2,Y2
				pieces_in_play += [wk3]
				t_x = 0
			if x1==3 and y1==5:
				wq2=WhiteQueen()
				wq2.x,wq2.y=X2,Y2
				pieces_in_play += [wq2]
				t_x = 0

	if t_x == 2:
		if not gamewon:
			pygame.draw.rect(screen,(100,50,25),[160,220,320,160])
			screen.blit(bq1.image,(160,320))
			screen.blit(br1.image,(240,320))
			screen.blit(bb1.image,(320,320))
			screen.blit(bk1.image,(400,320))
			text=font.render(" Please choose a piece", True, white)
			screen.blit(text, [160, 265])
			
			if x1==5 and y1==5:
				bb3=BlackBishop()
				bb3.x,bb3.y=X2,Y2
				pieces_in_play += [bb3]
				t_x = 0
			if x1==4 and y1==5:
				br3=BlackRook()
				br3.x,br3.y=X2,Y2
				pieces_in_play += [br3]
				t_x = 0
			if x1==6 and y1==5:
				bk3=BlackKnight()
				bk3.x,bk3.y=X2,Y2
				pieces_in_play += [bk3]
				t_x = 0
			if x1==3 and y1==5:
				bq2=BlackQueen()
				bq2.x,bq2.y=X2,Y2
				pieces_in_play += [bq2]
				t_x = 0


	if len(m)==2:
		moves=[]
		moves=legal_moves_dict[f]
		for validmoves in moves:
			# prints a boundary over the boxes where moves are possible.
			pygame.draw.rect(screen,blue,[cd(validmoves[0],validmoves[1])[0],cd(validmoves[0],validmoves[1])[1],80,80],4)




	#---------------!!-------CONSOLE----------!!-------------

	# text=font.render(" Please choose a piece", True, white)
	# screen.blit(text, [160, 265])

	pygame.draw.rect(screen,(100,50,25),[645,0,240,640])
	pygame.draw.rect(screen,(50,15,0),[640,0,5,640])
	screen.blit(font.render("Pieces Lost", True, black),[670,20])

	screen.blit(bp1.image,(642,80))
	screen.blit(font.render("%d"%killcount_bp,True,black),[715,100])
	screen.blit(bk1.image,(642,160))
	screen.blit(font.render("%d"%killcount_bk,True,black),[715,180])
	screen.blit(bb1.image,(642,240))
	screen.blit(font.render("%d"%killcount_bb,True,black),[715,260])
	screen.blit(br1.image,(642,320))
	screen.blit(font.render("%d"%killcount_br,True,black),[715,340])
	screen.blit(bq1.image,(642,400))
	screen.blit(font.render("%d"%killcount_bq,True,black),[715,420])
	screen.blit(wp1.image,(775,80))
	screen.blit(font.render("%d"%killcount_wp,True,black),[760,100])
	screen.blit(wk1.image,(775,160))
	screen.blit(font.render("%d"%killcount_wk,True,black),[760,180])
	screen.blit(wb1.image,(775,240))
	screen.blit(font.render("%d"%killcount_wb,True,black),[760,260])
	screen.blit(wr1.image,(775,320))
	screen.blit(font.render("%d"%killcount_wr,True,black),[760,340])
	screen.blit(wq1.image,(775,400))
	screen.blit(font.render("%d"%killcount_wq,True,black),[760,420])

	# shows timer
	"""
	time_change_check=time.asctime().split()[3].split(":")[2]								
	if time_change_var!=time_change_check:
		time_elapsed+=1
		time_change_var=time_change_check
	time_elapsed_print=font.render("%d:%d"%(time_elapsed/60,time_elapsed%60),True,white)
	screen.blit(time_elapsed_print,[730,600])
	screen.blit(font.render("Time Elapsed",True,black),[660,565])
	"""
		
	pygame.display.flip()

	if gamewon:
		time.sleep(3)
		done=True
	clock.tick(60)	

# Close the window and quit.
pygame.quit()