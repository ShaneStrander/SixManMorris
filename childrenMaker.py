from pprint import pprint, pformat
import copy
import math
import random

def test():
    print("Woo")

# This is our heuristic. Each combination of Red, Blue, or none on
# the sides of the inner and outer squares are labeled as to how much they are worth
scores = {
    'xxx': 0,
    'xxb': -1,
    'xxr': 1,
    'xbx': -1,
    'xbb': -3,
    'xbr': 0,
    'xrx': 1,
    'xrb': 0,
    'xrr': 3,
    'bxx': -1,
    'bxb': -3,
    'bxr': 0,
    'bbx': -3,
    'bbb': -10,
    'bbr': 2,
    'brx': 0,
    'brb': 2,
    'brr': -2,
    'rxx': 1,
    'rxb': 0,
    'rxr': 3,
    'rbx': 0,
    'rbb': 2,
    'rbr': -2,
    'rrx': 3,
    'rrb': -2,
    'rrr': 10,
}


class Node:
    def __init__(self, parent, boardState, lastMove):
        self.parent = parent
        self.boardState = boardState
        self.lastMove = lastMove

    def __str__(self, level):
        ret = "\t"*level +pformat(self.lastMove) + "\n\n"
        # ret = "\t"*level + "x" + "\n"
        if self.children:
            for child in self.children:
                ret = ret + child.__str__(level + 1)
        return ret

    parent = None
    children = []
    boardState =[]
    lastMove = { "color": "white", "pieceIdx": -1, "movePos": "a" }
    minimaxVal = 0

# This returns a list of the tiles on the board where the given color is
def getCurrColor(board, color):
	currColorList = []
	for x in board:
		if board[x] == color:
			currColorList.append(x)
	return currColorList


tiles={
	"a" : "Red",
	"b" : "none",
	"c" : "Red",
	"d" : "none",
	"e" : "none",
	"f" : "none",
	"g" : "none",
	"h" : "none",
	"i" : "none",
	"j" : "none",
	"k" : "Red",
	"l" : "none",
	"m" : "none",
	"n" : "none",
	"o" : "Blue",
	"p" : "none",
}

# The is a dictionary of every space on the board and every place a tile could move to
# from this location
def moveOptions(pos):
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
	return validMoves[pos]

def placeOptions(board):
    options = []
    for tile in board:
        if board[tile] == "none":
            options.append(tile)
    return options

# This checks if the most recent move is in a morris
def morrisChecker(tiles, most_recent_move):
	if tiles["a"] == tiles["b"] == tiles["c"] and tiles["a"] != "none":
		line = ["a", "b", "c"]
		if most_recent_move in line:
			return True

	if tiles["a"] == tiles["h"] == tiles["g"] and tiles["a"] != "none":
		line = ["a", "h", "g"]
		if most_recent_move in line:
			return True

	if tiles["c"] == tiles["d"] == tiles["e"] and tiles["e"] != "none":
		line = ["c", "d", "e"]
		if most_recent_move in line:
			return True

	if tiles["e"] == tiles["f"] == tiles["g"] and tiles["e"] != "none":
		line = ["e", "f", "g"]
		if most_recent_move in line:
			return True

	if tiles["j"] == tiles["k"] == tiles["l"] and tiles["j"] != "none":
		line = ["j", "k", "l"]
		if most_recent_move in line:
			return True

	if tiles["j"] == tiles["i"] == tiles["p"] and tiles["j"] != "none":
		line = ["j", "i", "p"]
		if most_recent_move in line:
			return True

	if tiles["l"] == tiles["m"] == tiles["n"] and tiles["n"] != "none":
		line = ["l", "m", "n"]
		if most_recent_move in line:
			return True

	if tiles["n"] == tiles["o"] == tiles["p"] and tiles["n"] != "none":
		line = ["n", "o", "p"]
		if most_recent_move in line:
			return True

	return False


class Tree:
    def __init__(self, parent, boardState, lastMove):
        self.root = Node(parent, boardState, lastMove)
        self.root.children = self.child(self.root, "Red", 0)

    def __str__(self):
        return self.root.__str__(0)

    root = None
    maxDepth = 4

    def child(self, node, color, depth):
        if depth == self.maxDepth:
            return None
        other = "Red"
        if color == "Red":
            other = "Blue"
        # tileColorTotal is a list of the tiles that are = color
        currTileColorTotal = getCurrColor(node.boardState.copy(), color)
        otherTileColorTotal = getCurrColor(node.boardState.copy(), other)
        possibleBoardStates = []
        childrenNodes = []
        for tile in currTileColorTotal:
            options = moveOptions(tile)
            for opt in options:

                if node.boardState[opt] == "none":

                    tmpBoardState = copy.deepcopy(node.boardState)
                    tmpBoardState[opt] = color
                    tmpBoardState[tile] = "none"
                    if morrisChecker(tmpBoardState, opt):
                        for otherTile in otherTileColorTotal:
                            tmpBoardState[otherTile] = "none"
                            childrenNodes.append(Node(parent=node, boardState=tmpBoardState, lastMove = { "color": color, "pieceIdx": tile, "movePos": opt, "deleted": otherTile }))
                            if depth == self.maxDepth:
                                childrenNodes[len(childrenNodes) - 1].children = None
                            else:
                                childrenNodes[len(childrenNodes) - 1].children = self.child(childrenNodes[len(childrenNodes) - 1], other, depth + 1)
                    else:
                        childrenNodes.append(Node(parent=node, boardState=tmpBoardState, lastMove = { "color": color, "pieceIdx": tile, "movePos": opt, "deleted": "none" }))
                        if depth == self.maxDepth:
                            childrenNodes[len(childrenNodes) - 1].children = None
                        else:
                            childrenNodes[len(childrenNodes) - 1].children = self.child(childrenNodes[len(childrenNodes) - 1], other, depth + 1)
        return(childrenNodes)

class PlacementTree:
    def __init__(self, parent, boardState, lastMove):
        self.root = Node(parent, boardState, lastMove)
        self.root.children = self.child(self.root, "Red", 0)

    def __str__(self):
        return self.root.__str__(0)

    root = None
    maxDepth = 3

    def child(self, node, color, depth):
        if depth == self.maxDepth:
            return None
        other = "Red"
        if color == "Red":
            other = "Blue"
        # tileColorTotal is a list of the tiles that are = color
        currTileColorTotal = getCurrColor(node.boardState.copy(), color)
        otherTileColorTotal = getCurrColor(node.boardState.copy(), other)
        childrenNodes = []
        options = placeOptions(node.boardState)
        for opt in options:
            tmpBoardState = copy.deepcopy(node.boardState)
            tmpBoardState[opt] = color
            if morrisChecker(tmpBoardState, opt):
                for otherTile in otherTileColorTotal:
                    tmpBoardState[otherTile] = "none"
                    childrenNodes.append(Node(parent=node, boardState=tmpBoardState, lastMove = { "color": color, "pieceIdx": opt, "movePos": opt, "deleted": otherTile }))
                    if depth == self.maxDepth:
                        childrenNodes[len(childrenNodes) - 1].children = None
                    else:
                        childrenNodes[len(childrenNodes) - 1].children = self.child(childrenNodes[len(childrenNodes) - 1], other, depth + 1)
            else:
                childrenNodes.append(Node(parent=node, boardState=tmpBoardState, lastMove = { "color": color, "pieceIdx": opt, "movePos": opt, "deleted": "none" }))
                if depth == self.maxDepth:
                    childrenNodes[len(childrenNodes) - 1].children = None
                else:
                    childrenNodes[len(childrenNodes) - 1].children = self.child(childrenNodes[len(childrenNodes) - 1], other, depth + 1)
        return(childrenNodes)

def score(boardState):
    sidesAlt = [["a", "b", "c"],
                ["c", "d", "e"],
                ["e", "f", "g"],
                ["g", "h", "a"],
                ["j", "k", "l"],
                ["l", "m", "n"],
                ["n", "o", "p"],
                ["p", "i", "j"]]

    score = 0
    for side in sidesAlt:
        str = ""
        for x in side:
            tmp = boardState[x]
            if tmp == "Red":
                str += "r"
            elif tmp == "Blue":
                str += "b"
            else:
                str += "x"
        score += scores[str]
    return score


def getLeafNodes(node, finalNodes = []):
    if node.children == None:
        finalNodes.append(node)
    else:
        for child in node.children:
            getLeafNodes(child, finalNodes)


def minimax(node, is_max_turn):
    if node.children == None or len(node.children) == 0:
        node.minimaxVal = score(node.boardState)
    else:
        if is_max_turn:
            maxNode = node
            maxNode.minimaxVal = -9999
            for child in node.children:
                minimax(child, False)
                maxNode.minimaxVal = max(maxNode.minimaxVal, child.minimaxVal)
            node.minimaxVal = maxNode.minimaxVal
        else:
            minNode = node
            minNode.minimaxVal = 9999
            for child in node.children:
                minimax(child, True)
                minNode.minimaxVal = min(minNode.minimaxVal, child.minimaxVal)
            node.minimaxVal = minNode.minimaxVal



def getBotBestBoardState(board):
    temp = { "color": "white", "pieceIdx": -1, "movePos": "a", "deleted": "none" }
    tree = Tree(None, board.copy(), temp)
    minimax(tree.root, True)
    nextMove =""
    for child in tree.root.children:
        if tree.root.minimaxVal == child.minimaxVal:
            nextMove = child.lastMove
            break
    return nextMove

def rearrangeBoard():
    freeTiles = []
    for tile in tiles:
        tiles[tile] = "none"
        freeTiles.append(tile)
    for _ in range(5):
        freeTiles = []
        for tile in tiles:
            if tiles[tile] == "none":
                freeTiles.append(tile)
        num = random.randint(0,len(freeTiles)-1)
        tiles[freeTiles[num]] = "Blue"
        move = getBotBestBoardStatePlacement(tiles)["movePos"]
        tiles[move] = "Red"

def runRandomBot():
    rearrangeBoard()

    exit = False
    maxTurns = 20
    turn = 0
    while len(getCurrColor(tiles, "Blue")) > 2 and len(getCurrColor(tiles, "Red")) > 2:
        if turn >= maxTurns:
            return 2
        turn = turn + 1
        curr = None
        blues = getCurrColor(tiles, "Blue")
        availableFound = False
        for blue in blues:
                for available in moveOptions(blue):
                    if not availableFound:
                        if tiles[available] == "none":
                            tiles[blue] = "none"
                            tiles[available] = "Blue"
                            curr = available
                            availableFound = True
        if not availableFound:
            print("None found")
            return 2
        if morrisChecker(tiles, curr):
            reds = getCurrColor(tiles, "Red")
            x = random.randint(0, len(reds)-1)
            rem = reds[x]
            tiles[rem] = "none"
            curr = "none"

        redMove = getBotBestBoardState(tiles)
        tiles[redMove["pieceIdx"]] = "none"
        tiles[redMove["movePos"]] = "Red"
        if redMove["deleted"] != "none":
            tiles[redMove["deleted"]] = "none"
    if len(getCurrColor(tiles, "Blue")) > 2:
        return 0
    else:
        return 1

def getBotBestBoardStatePlacement(board):
    temp = { "color": "white", "pieceIdx": -1, "movePos": "a", "deleted": "none" }
    tree = PlacementTree(None, board.copy(), temp)
    minimax(tree.root, True)
    nextMove =""
    for child in tree.root.children:
        if tree.root.minimaxVal == child.minimaxVal:
            nextMove = child.lastMove
            break
    return nextMove

def progressBar(current, total, barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

blueWins = 0
redWins = 0
draws = 0
print("Loading...")
iterations = 1000
for i in range(iterations):
    progressBar(i, iterations, 50)
    ret = runRandomBot()
    if ret == 0:
        blueWins = blueWins + 1
    elif ret == 1:
        redWins = redWins + 1
    else:
        draws = draws + 1

print("Blue won " + str(blueWins) + " times.")
print("Red won " + str(redWins) + " times.")
print("Red and Blue had " + str(draws) + " draws.")
total = redWins+blueWins+draws
if total == 0: total = 1
print("The win percentage for our bot is " + str(redWins*100 / (total)) + "%")
