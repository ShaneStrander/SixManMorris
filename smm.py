# importing the required libraries
import pygame as pg
import sys
import time
from pygame.locals import *

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

#This function draws everything every game loop
def draw():
	screen.fill(boardColor)

	if(turn % 2 == 1):
		player = "Red"
	else:
		player = "Blue"

	#This is all fro displaying text in the center of the screen
	font = pg.font.Font('freesansbold.ttf', 32)
	text1 = font.render('Turn = ' + str(turn + 1), True, black, boardColor)
	text2 = font.render('It is ' + player + '\'s turn' , True, black, boardColor)
	textRect1 = text1.get_rect()
	textRect2 = text2.get_rect()
	textRect1.center = ((w // 2) + 17, (h // 2) + 17)
	textRect2.center = ((w // 2) - 17, (h // 2) - 17)

	screen.blit(text1, textRect1)
	screen.blit(text2, textRect2)

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

	#This is for drawing the selected tile
	if(selected != "none"):
		pg.draw.circle(screen, yellow, selected, 40, width = 10)


turn = 0
#This function is for placing down tiles
def place():
	for key in coordDict:
		if tiles[key] == "none":
			if coordDict[key][0]-40 <= x <= coordDict[key][0]+40 and coordDict[key][1]-40 <= y <= coordDict[key][1]+40:
				global turn
				turn = turn + 1
				if(turn % 2 == 1):
					tiles[key] = "Blue"
				else:
					tiles[key] = "Red"


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
					curr = (list(coordDict.keys())[list(coordDict.values()).index(coordDict[key])])
					prev = (list(coordDict.keys())[list(coordDict.values()).index(selected)])
					print(curr)
					if key in moveOptions(prev):
						for coord in coordDict:
							if(selected == coordDict[coord]):
								tiles[coord] = "none"
						if(turn % 2 == 0):
							tiles[key] = "Blue"
						else:
							tiles[key] = "Red"

						selected = "none"
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

#[WORK IN PROGRESS]
def morrisChecker(tile):
	piece = tile
	morris = "none"

	if tiles["a"] == tiles["b"] == tiles["c"] and tiles["a"] != "none":
		morris = tiles["a"]

	if tiles["a"] == tiles["h"] == tiles["g"] and tiles["a"] != "none":
		morris = tiles["a"]

	if tiles["c"] == tiles["d"] == tiles["e"] and tiles["e"] != "none":
		morris = tiles["e"]

	if tiles["e"] == tiles["f"] == tiles["g"] and tiles["e"] != "none":
		morris = tiles["e"]

	if tiles["j"] == tiles["k"] == tiles["l"] and tiles["j"] != "none":
		morris = tiles["j"]

	if tiles["j"] == tiles["i"] == tiles["p"] and tiles["j"] != "none":
		morris = tiles["j"]

	if tiles["l"] == tiles["m"] == tiles["n"] and tiles["n"] != "none":
		morris = tiles["n"]

	if tiles["n"] == tiles["o"] == tiles["p"] and tiles["n"] != "none":
		morris = tiles["n"]

	return morris




while(True):
	for event in pg.event.get():
		if event.type == QUIT:
			pg.quit()
			sys.exit()

	x, y = pg.mouse.get_pos()

	draw()

	if event.type == pg.MOUSEBUTTONDOWN:
		if(turn < 6):
			place()
		elif(turn < 16):
			moveSelecter()
			moveHelper()

	# This is drawing black dots and making them gray when hovered
	for key in coordDict:
		if tiles[key] == "none":
			if coordDict[key][0]-40 <= x <= coordDict[key][0]+40 and coordDict[key][1]-40 <= y <= coordDict[key][1]+40:
				pg.draw.circle(screen, gray, coordDict[key], 16)
			else:
				pg.draw.circle(screen, black, coordDict[key], 16)


	pg.display.update()
	CLOCK.tick(fps)
