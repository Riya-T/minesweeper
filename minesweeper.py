import random

def checkSurroundings(array, x, y): #determine how many mines are around a given square
	answer = 0
	if x > 0:
		if array[x - 1][y] == "m":
			answer += 1
	if x < 8:
		if array[x + 1][y] == "m":
			answer += 1
	if y > 0:
		if array[x][y - 1] == "m":
			answer += 1
	if y < 8:
		if array[x][y + 1] == "m":
			answer += 1
	if x > 0 and y > 0:
		if array[x - 1][y - 1] == "m":
			answer += 1
	if x < 8 and y < 8:
		if array[x + 1][y + 1] == "m":
			answer += 1
	if x < 8 and y > 0:
		if array[x + 1][y - 1] == "m":
			answer += 1
	if x > 0 and y < 8:
		if array[x - 1][y + 1] == "m":
			answer += 1
	return answer

def output(array): #outputs board
	print ("  A B C D E F G H I")
	letters = ["J ", "K ", "L ", "M ", "N ", "O ", "P ", "Q ", "R "]
	for i in range(9):
		line = letters[i]
		for j in array[i]:
			line = line + str(j) + " "
		print(line)

def revealCoords(external, internal, x, y): #check coordinates
	if internal[x][y] == "m": #player clicked on mine, game over
		external[x][y] = internal[x][y]
		return True
	elif internal[x][y] > 0: #normal square
		external[x][y] = internal[x][y]
	else: #0 square, requires recursion
		external[x][y] = internal[x][y]
		if x > 0:
			if external[x - 1][y] == "#" or external[x - 1][y] == "f":
				revealCoords(external, internal, x - 1, y)
		if x < 8:
			if external[x + 1][y] == "#" or external[x + 1][y] == "f":
				revealCoords(external, internal, x + 1, y)
		if y > 0:
			if external[x][y - 1] == "#" or external[x][y - 1] == "f":
				revealCoords(external, internal, x, y - 1)
		if y < 8:
			if external[x][y + 1] == "#" or external[x][y + 1] == "f":
				revealCoords(external, internal, x, y + 1)
		if x > 0 and y > 0:
			if external[x - 1][y - 1] == "#" or external[x - 1][y - 1] == "f":
				revealCoords(external, internal, x - 1, y - 1)
		if x < 8 and y < 8:
			if external[x + 1][y + 1] == "#" or external[x + 1][y + 1] == "f":
				revealCoords(external, internal, x + 1, y + 1)
		if x < 8 and y > 0:
			if external[x + 1][y - 1] == "#" or external[x + 1][y - 1] == "f":
				revealCoords(external, internal, x + 1, y - 1)
		if x > 0 and y < 8:
			if external[x - 1][y + 1] == "#" or external[x - 1][y + 1] == "f":
				revealCoords(external, internal, x - 1, y + 1)
	return False

def checkWin(external, internal): #check if won
	for i in range(9):
		for j in range(9):
			if external[i][j] == "#" or external[i][j] == "f":
				if internal[i][j] != "m":
					return False
	return True

#minefield for internal reference
internal = [["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"]]
#minefield shown to player
external = [["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"]]

#generate mines
counter = 10
while counter > 0:
	x = random.randint(0, 8)
	y = random.randint(0, 8)
	if internal[x][y] != "m":
		internal[x][y] = "m"
		counter -= 1

#finish generating internal	
checked = 0
for i in range(9):
	for j in range(9):
		if internal[i][j] != "m":
			checked = checkSurroundings(internal, i, j)
			internal[i][j] = checked
			
lose = False #game over, loss
win = False #game over, win
action = "" #cfr
coords = "" #coordinates
cx = {"j":0, "k":1, "l":2, "m":3, "n":4, "o":5, "p":6, "q":7, "r":8} #dictionary for x coordinates
cy = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8} #dictionary for y coordinates

#gameplay
while lose == False and win == False:
	output(external)
	print()
	action = input("Would you like to reveal a square (C), place a flag (F), or remove a flag (R)? ")
	action = action.lower()
	
	if action == "c": #reveal a square
		coords = input('Input coordinates with no punctuation or spaces (ex. "aj"). ')
		print()
		coords = coords.lower()
		if len(coords) > 1:
			if coords[0] in cy and coords[1] in cx:
				y = cy[coords[0]]
				x = cx[coords[1]]
				if external[x][y] == "#": #empty square, call function
					lose = revealCoords(external, internal, x, y)
				elif external[x][y] == "f": #flagged square, ask for permission
					confirm = input('You have already placed a flag in that spot. Are you sure you want to reveal it? Type "yes" to confirm, anything else to go back. ')
					print()
					if confirm == "yes":
						lose = revealCoords(external, internal, x, y)
				else: #this square has already been revealed
					print("That square has already been revealed")
					print()
			else:
				print("Sorry, those coordinates don't make sense")
				print()
		else:
			print("Sorry, those coordinates don't make sense")
			print()
		win = checkWin(external, internal)
		
	elif action == "f": #place flag
		coords = input('Input coordinates with no punctuation or spaces (ex. "aj"). ')
		print()
		coords = coords.lower()
		if len(coords) > 1:
			if coords[0] in cy and coords[1] in cx:
				y = cy[coords[0]]
				x = cx[coords[1]]
				if external[x][y] == "#": #empty square, place flag
					external[x][y] = "f"
				elif external[x][y] == "f": #flagged square
					print("That square already has a flag on it")
					print()
				else: #this square has already been revealed
					print("That square has already been revealed")
					print()
			else:
				print("Sorry, those coordinates don't make sense")
				print()
		else:
			print("Sorry, those coordinates don't make sense")
			print()
				
	elif action == "r": #remove flag
		coords = input('Input coordinates with no punctuation or spaces (ex. "aj"). ')
		print()
		coords = coords.lower()
		if len(coords) > 1:
			if coords[0] in cy and coords[1] in cx:
				y = cy[coords[0]]
				x = cx[coords[1]]
				if external[x][y] == "f": #flagged square, remove flag
					external[x][y] = "#"
				else: #this square already doesn't have a flag
					print("That square already doesn't have a flag")
					print()
			else:
				print("Sorry, those coordinates don't make sense")
				print()
		else:
			print("Sorry, those coordinates don't make sense")
			print()
	else:
		print("That doesn't make sense. Your options are C, F, or R")
			
if win == True: #win
	output(internal)
	print()
	print("Congratulations! You won!")
else: #lose
	output(external)
	print()
	print("Sorry, you lost.")