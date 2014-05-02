# Simple 4x4 Dodgem Game
# By Andrew Mori
from random import randint

board = [["  " for x in range(6)] for y in range(6)]
gamePieces = {}
gamePieces["A1"] = (1,5)
gamePieces["A2"] = (2,5)
gamePieces["A3"] = (3,5)
gamePieces["B1"] = (5,1)
gamePieces["B2"] = (5,2)
gamePieces["B3"] = (5,3)

inValidA = [(5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(4,5),(0,0),(0,1),(0,2),(0,3),(0,4),(0,5)]
inValidB = [(0,5),(1,5),(2,5),(3,5),(4,5),(5,5),(5,4),(0,0),(1,0),(2,0),(3,0),(4,0),(5,0)]
#initializes a board 4x4 game
def setupBoard():
	board[1][5] = "A1"
	board[2][5] = "A2"
	board[3][5] = "A3"
	board[4][5] = "XX"
	board[5][5] = "XX"
	board[5][4] = "XX"
	board[5][1] = "B1"
	board[5][2] = "B2"
	board[5][3] = "B3"
	board[0][0] = "XX"
	board[0][5] = "XX"
	board[5][0] = "XX"



def getMoves(board,piece):
	curPos = gamePieces[piece]
	if curPos == "G":
		return []
	else:
		x = curPos[0]
		y = curPos[1]
		validPositions = []
		if piece[0]=="A":
			left = board[x+1][y]
			right = board[x-1][y]
			up = board[x][y-1]

			if left=="  " and not (x+1,y) in inValidA:
				validPositions.append((x+1,y))
			if right == "  " and not (x-1,y) in inValidA:
				validPositions.append((x-1,y))
			if up== "  " and not (x,y-1) in inValidA:
				validPositions.append((x,y-1))
			#print validPositions
			return validPositions
		else:
			left = board[x][y-1]
			right = board[x][y+1]
			up = board[x-1][y]
			if left=="  " and not (x,y-1) in inValidB:
				validPositions.append((x,y-1))
			if right == "  " and not (x,y+1) in inValidB:
				validPositions.append((x,y+1))
			if up== "  " and not (x-1,y) in inValidB:
				validPositions.append((x-1,y))
			#print validPositions
			return validPositions


#prints the board state
def printBoardState(board):
	print "   1    2    3    4    5"
	for i in range(5):
		print "%s [%s] [%s] [%s] [%s] [%s]" % (i+1,board[i+1][1],board[i+1][2],board[i+1][3],board[i+1][4],board[i+1][5])

#returns true if valid or false if not valid
#params piece is string newpos is a tuple
# input = "A1 x,y"
def validMove(resp):
	try:
		move = resp.split(" ")
		piece = move[0]
		x = move[1][0]
		y = move[1][2]
		valid = getMoves(board,piece)
		if (int(x),int(y)) in valid:
			return True
		else:
			return False
	except:
		return False

def makeMove(resp):
	try:
		move = resp.split(" ")
		piece = move[0]
		curPos = gamePieces[piece]
		board[curPos[0]][curPos[1]] = "  "
		if (int(move[1][0]),int(move[1][2])) in [(0,1),(0,2),(0,3),(0,4),(4,0),(3,0),(2,0),(1,0)]:
			board[int(move[1][0])][int(move[1][2])] = "  "
			gamePieces[piece] = "G"
		else:
			board[int(move[1][0])][int(move[1][2])] = piece
			gamePieces[piece] = (int(move[1][0]),int(move[1][2]))
		return True
	except:
		return False

def computerMove(board):
	validMoves = []
	if gamePieces["B1"] != "G":
		moves = getMoves(board,"B1")
		if len(moves) > 0:
			for move in moves:
				validMoves.append("B1 %s,%s" % (move[0],move[1]))
				if move in [(0,1),(0,2),(0,3),(0,4)]:
					return "B1 %s,%s" % (move[0],move[1])
	if gamePieces["B2"] != "G":
		moves = getMoves(board,"B2")
		if len(moves) > 0:
			for move in moves:
				validMoves.append("B2 %s,%s" % (move[0],move[1]))
				if move in [(0,1),(0,2),(0,3),(0,4)]:
					return "B1 %s,%s" % (move[0],move[1])
	if gamePieces["B3"] != "G":
		moves = getMoves(board,"B3")
		if len(moves) > 0:
			for move in moves:
				validMoves.append("B3 %s,%s" % (move[0],move[1]))
				if move in [(0,1),(0,2),(0,3),(0,4)]:
					return "B1 %s,%s" % (move[0],move[1])
	return validMoves[randint(0,len(validMoves)-1)]


def isWinner(player):
	if player=="A":
		if gamePieces["A1"]=="G" and gamePieces["A2"]=="G" and gamePieces["A3"]=="G":
			return True
		else:
			return False
	else:
		if gamePieces["B1"]=="G" and gamePieces["B2"]=="G" and gamePieces["B3"]=="G":
			return True
		else:
			return False

def playerHasValidMoves(player):
	validMoves = []
	if player=="A":
		p1 = getMoves(board,"A1")
		p2 = getMoves(board,"A2")
		p3 = getMoves(board,"A3")
		validMoves.append(p1)
		validMoves.append(p2)
		validMoves.append(p3)
		if len(validMoves) > 0:
			return True
		else:
			return False
	else:
		p1 = getMoves(board,"B1")
		p2 = getMoves(board,"B2")
		p3 = getMoves(board,"B3")
		validMoves.append(p1)
		validMoves.append(p2)
		validMoves.append(p3)
		if len(validMoves) > 0:
			return True
		else:
			return False


def play():
	winner = None
	setupBoard()
	print "Welcome to DinoDodgem! \nRules: 2 players, 3 pieces each, 4x4 board \nWin if you move all pieces off the board or your opponent cant make a move"
	# run while there is no winner
	printBoardState(board)
	while winner== None:
		if playerHasValidMoves("A"):
			#check to see if human has valid moves

			# begin with asking the human to player to make a move
			resp = raw_input("Input Move: ")
			# check if inputted move is legal, prompt user again if illegal move
			if validMove(resp):
				# make human move
				if makeMove(resp):
					print "Updating board"
					printBoardState(board)
					if isWinner("A"):
						winner = "A"
						continue
					else:
						# check if ai has valid move
						if playerHasValidMoves("B"):
							# make valid move
							if makeMove(computerMove(board)):
								print "Updating board"
								printBoardState(board)
								if isWinner("B"):
									winner = "B"
									continue	
			else:
				print "Illegal move, please make a legal move"
				continue
	if winner=='A':
		print "You win!"
	else:
		print "You lose, sorry :("

play()