# importing the required libraries
import pygame as pg
import sys
import time
from pygame.locals import *

import random

from minimaxAlgorithm import *


# set width and height of the game window
w = 800
h = 800

# set offset and game board size
os = 50
gw = w-os
gh = h-os
ogw = (gw-os)
ogh = (gh-os)

# colors
white = (255, 255, 255)
boardColor = (255, 235, 179)
black = (0, 0, 0)
gray = (100,100,100)
red = (173, 54, 54)
blue = (87, 117, 140)
yellow = (255, 255, 0)

# initializing necessities
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((w, h), 0, 32)
pg.display.set_caption("Six Men's Morris")


# Coordinates of tiles
coordDict={
	"a" : (os, os),
	"b" : (os+ogw/2, os),
	"c" : (gw, os),
	"d" : (gw, os+ogh/2),
	"e" : (gw, gh),
	"f" : (os+ogw/2, gh),
	"g" : (os, gh),
	"h" : (os, os+ogh/2),
	"i" : (os+ogw/4, os+ogh/2),
	"j" : (os+ogw/4, os+ogh/4),
	"k" : (os+ogw/2, os+ogh/4),
	"l" : (os+3*ogw/4, os+ogh/4),
	"m" : (os+3*ogw/4, os+ogh/2),
	"n" : (os+3*ogw/4, os+3*ogh/4),
	"o" : (os+ogw/2, os+3*ogh/4),
	"p" : (os+ogw/4, os+3*ogh/4),
}

#list of tiles and what color player is currently occupying that spot
tiles={
	"a" : "none",
	"b" : "none",
	"c" : "none",
	"d" : "none",
	"e" : "none",
	"f" : "none",
	"g" : "none",
	"h" : "none",
	"i" : "none",
	"j" : "none",
	"k" : "none",
	"l" : "none",
	"m" : "none",
	"n" : "none",
	"o" : "none",
	"p" : "none",
}

def getCurrTiles():
	return tiles

#This function draws everything every game loop
def draw():
	screen.fill(boardColor)

	if(turn % 2 == 1):
		player = "Red"
	else:
		player = "Blue"

	#This is all for displaying text in the center of the screen
	winCheck = winner()
	if winCheck == "none" or turn < 12:
		font = pg.font.Font('freesansbold.ttf', 32)
		text1 = font.render('Turn = ' + str(turn + 1), True, black, boardColor)
		text2 = font.render('It is ' + player + '\'s turn' , True, black, boardColor)
		textRect1 = text1.get_rect()
		textRect2 = text2.get_rect()
		textRect1.center = ((w // 2) + 17, (h // 2) + 17)
		textRect2.center = ((w // 2) - 17, (h // 2) - 17)

		screen.blit(text1, textRect1)
		screen.blit(text2, textRect2)
	else:
		font = pg.font.Font('freesansbold.ttf', 32)
		text3 = font.render(winCheck + ' wins!', True, black, boardColor)
		textRect3 = text3.get_rect()
		textRect3.center = ((w // 2) + 17, (h // 2) + 17)
		screen.blit(text3, textRect3)


	# drawing outter Box
	pg.draw.line(screen, black, coordDict["a"], coordDict["c"], 7)
	pg.draw.line(screen, black, coordDict["c"], coordDict["e"], 7)
	pg.draw.line(screen, black, coordDict["e"], coordDict["g"], 7)
	pg.draw.line(screen, black, coordDict["g"], coordDict["a"], 7)
	#drawing connecting lines
	pg.draw.line(screen, black, coordDict["b"], coordDict["k"], 7)
	pg.draw.line(screen, black, coordDict["d"], coordDict["m"], 7)
	pg.draw.line(screen, black, coordDict["f"], coordDict["o"], 7)
	pg.draw.line(screen, black, coordDict["h"], coordDict["i"], 7)
	# drawing inner box
	pg.draw.line(screen, black, coordDict["j"], coordDict["l"], 7)
	pg.draw.line(screen, black, coordDict["l"], coordDict["n"], 7)
	pg.draw.line(screen, black, coordDict["n"], coordDict["p"], 7)
	pg.draw.line(screen, black, coordDict["p"], coordDict["j"], 7)

	x, y = pg.mouse.get_pos()

	#This is for drawing the tiles in their correct positions
	for tile in tiles:
		if(tiles[tile] == "Blue"):
			pg.draw.circle(screen, blue, coordDict[tile], 40)
		elif(tiles[tile] == "Red"):
			pg.draw.circle(screen, red, coordDict[tile], 40)

	#This is for highlighting the selected tile
	if(selected != "none"):
		pg.draw.circle(screen, yellow, selected, 40, width = 10)

curr = "none"
turn = 0
#This function is for placing down tiles
def place():
	global curr
	global turn
	for key in coordDict:
		if tiles[key] == "none":
			if coordDict[key][0]-40 <= x <= coordDict[key][0]+40 and coordDict[key][1]-40 <= y <= coordDict[key][1]+40:
				curr = (list(coordDict.keys())[list(coordDict.values()).index(coordDict[key])])
				if(turn % 2 == 0):
					tiles[key] = "Blue"
				else:
					tiles[key] = "Red"
				if morrisChecker(curr) == False:
					turn = turn + 1


selected = "none"
#This function picks which tile the user has selected
def moveSelecter():
	global selected
	x, y = pg.mouse.get_pos()
	for key in coordDict:
		if tiles[key] != "none":
			if coordDict[key][0]-40 <= x <= coordDict[key][0]+40 and coordDict[key][1]-40 <= y <= coordDict[key][1]+40:
				global turn
				if(turn % 2 == 1):
					if(tiles[key]) == "Red":
						selected = coordDict[key]
				else:
					if(tiles[key]) == "Blue":
						selected = coordDict[key]


#This function draws a tile where the user chooses to move to as well as removing the tile from the old spot
def moveHelper():
	global selected
	global turn
	if(selected != "none"):
		x, y = pg.mouse.get_pos()
		for key in coordDict:
			if tiles[key] == "none":
				if coordDict[key][0]-40 <= x <= coordDict[key][0]+40 and coordDict[key][1]-40 <= y <= coordDict[key][1]+40:
					global curr
					curr = (list(coordDict.keys())[list(coordDict.values()).index(coordDict[key])])
					prev = (list(coordDict.keys())[list(coordDict.values()).index(selected)])
					if key in moveOptions(prev):
						for coord in coordDict:
							if(selected == coordDict[coord]):
								tiles[coord] = "none"
						if(turn % 2 == 0):
							tiles[key] = "Blue"
						else:
							tiles[key] = "Red"

						selected = "none"
						if morrisChecker(curr) == False:
							turn = turn + 1


#This functions return whether or not a move is valid or not
def moveOptions(prev):
	validMoves={
		"a" : ["b", "h"],
		"b" : ["a", "c", "k"],
		"c" : ["b", "d"],
		"d" : ["c", "e", "m"],
		"e" : ["d", "f"],
		"f" : ["e", "g", "o"],
		"g" : ["f", "h"],
		"h" : ["a", "g", "i"],
		"i" : ["h", "j", "p"],
		"j" : ["i", "k"],
		"k" : ["b", "j", "l"],
		"l" : ["k", "m"],
		"m" : ["d", "l", "n"],
		"n" : ["m", "o"],
		"o" : ["f", "n", "p"],
		"p" : ["i", "o"],
	}
	return validMoves[prev]


#This function picks which tile the user has selected
def deletion():
	global curr
	global turn
	x, y = pg.mouse.get_pos()
	for key in coordDict:
		if tiles[key] != "none":
			if coordDict[key][0]-40 <= x <= coordDict[key][0]+40 and coordDict[key][1]-40 <= y <= coordDict[key][1]+40:
				global turn
				if event.type == pg.MOUSEBUTTONDOWN:
					if(turn % 2 == 1):
						if(tiles[key]) == "Blue":
							tiles[key] = "none"
							curr = "none"
							turn = turn + 1
					else:
						if(tiles[key]) == "Red":
							tiles[key] = "none"
							curr = "none"
							turn = turn + 1


#[WORK IN PROGRESS]
def morrisChecker(tile):
	piece = tile
	line = []
	global curr

	if tiles["a"] == tiles["b"] == tiles["c"] and tiles["a"] != "none":
		line = ["a", "b", "c"]
		if curr in line:
			return True

	if tiles["a"] == tiles["h"] == tiles["g"] and tiles["a"] != "none":
		line = ["a", "h", "g"]
		if curr in line:
			return True

	if tiles["c"] == tiles["d"] == tiles["e"] and tiles["e"] != "none":
		line = ["c", "d", "e"]
		if curr in line:
			return True

	if tiles["e"] == tiles["f"] == tiles["g"] and tiles["e"] != "none":
		line = ["e", "f", "g"]
		if curr in line:
			return True

	if tiles["j"] == tiles["k"] == tiles["l"] and tiles["j"] != "none":
		line = ["j", "k", "l"]
		if curr in line:
			return True

	if tiles["j"] == tiles["i"] == tiles["p"] and tiles["j"] != "none":
		line = ["j", "i", "p"]
		if curr in line:
			return True

	if tiles["l"] == tiles["m"] == tiles["n"] and tiles["n"] != "none":
		line = ["l", "m", "n"]
		if curr in line:
			return True

	if tiles["n"] == tiles["o"] == tiles["p"] and tiles["n"] != "none":
		line = ["n", "o", "p"]
		if curr in line:
			return True

	return False


def winner():
	blueTotal = 0
	redTotal = 0
	victor = "none"
	for x in coordDict:
		if tiles[x] == "Blue":
			blueTotal = blueTotal + 1
		elif tiles[x] == "Red":
			redTotal = redTotal + 1
	if blueTotal == 2 or redTotal == 2:
		if blueTotal == 2:
			victor = "Red"
		else:

			victor = "Blue"
	return victor


def getCurrColor(color):
	currColorList = []
	for x in tiles:
		if tiles[x] == color:
			currColorList.append(x)
	return currColorList


# def minimaxPlace():
# 	global turn
# 	global curr
# 	x = random.randint(0, 15)
# 	temp = []
# 	for y in tiles:
# 		temp.append(y)
# 	next = temp[x]
# 	if tiles[next] == "none":
# 		tiles[next] = "Red"
# 		curr = next
# 		if morrisChecker(curr) == False:
# 			turn = turn + 1
# 	else:
# 		minimaxPlace()

# def minimaxMove():
# 	global turn
# 	global curr
# 	reds = getCurrColor("Red")
# 	x = random.randint(0, len(reds)-1)
# 	sel = reds[x]
# 	available = moveOptions(sel)
# 	y = random.randint(0, len(available)-1)
# 	tar = available[y]
# 	if tiles[tar] == "none":
# 		tiles[tar] = "Red"
# 		curr = tar
# 		tiles[sel] = "none"
# 		if morrisChecker(curr) == False:
# 			turn = turn + 1
# 	else:
# 		minimaxMove()
#
# def minimaxDeletion():
# 	global turn
# 	global curr
# 	blues = getCurrColor("Blue")
# 	x = random.randint(0, len(blues)-1)
# 	rem = blues[x]
# 	tiles[rem] = "none"
# 	curr = "none"
# 	turn = turn + 1


def minimaxMove():
	global turn

	decisions = getBotBestBoardState(tiles)

	nextMove = decisions["movePos"]
	prevMove = decisions["pieceIdx"]
	toDelete = decisions["deleted"]

	curr = nextMove

	tiles[nextMove] = "Red"
	tiles[prevMove] = "none"

	if toDelete != "none":
		tiles[toDelete] = "none"

	turn = turn + 1


def minimaxPlace():
	global turn

	placements = getBotBestBoardStatePlacement(tiles)

	placeDelete = placements["deleted"]
	place = placements["movePos"]
	tiles[place] = "Red"

	curr = place

	if placeDelete != "none":
		tiles[placeDelete] = "none"

	turn = turn + 1


while(True):

	for event in pg.event.get():
		if event.type == QUIT:
			pg.quit()
			sys.exit()

	x, y = pg.mouse.get_pos()

	draw()

	if morrisChecker(curr):
		if turn % 2 == 0:
			deletion()
		else:
			if turn < 12:
				minimaxPlace()
			else:
				minimaxMove()

	elif event.type == pg.MOUSEBUTTONDOWN:
		if(turn < 12):
			if turn % 2 == 0:
				place()
			else:
				minimaxPlace()
		else:
			winCheck = winner()
			if winCheck == "none":
				if turn % 2 == 0:
					moveSelecter()
					moveHelper()
				else:
					minimaxMove()

			else:
				screen.fill(boardColor)

	# This is drawing black dots and making them gray when hovered
	for key in coordDict:
		if tiles[key] == "none":
			if coordDict[key][0]-40 <= x <= coordDict[key][0]+40 and coordDict[key][1]-40 <= y <= coordDict[key][1]+40:
				pg.draw.circle(screen, gray, coordDict[key], 16)
			else:
				pg.draw.circle(screen, black, coordDict[key], 16)


	pg.display.update()
	CLOCK.tick(fps)
