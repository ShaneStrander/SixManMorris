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

sidesAlt = [["a", "b", "c", "k"],
            ["c", "d", "e", "m"],
            ["e", "f", "g", "o"],
            ["g", "h", "a", "i"],
            ["j", "k", "l", "b"],
            ["l", "m", "n", "d"],
            ["n", "o", "p", "f"],
            ["p", "i", "j", "h"]]

sides = [["a", "b", "c"],
         ["c", "d", "e"],
         ["e", "f", "g"],
         ["g", "h", "a"],
         ["j", "k", "l"],
         ["l", "m", "n"],
         ["n", "o", "p"],
         ["p", "i", "j"]]

# RRR
def morris(board, sides, color):
    score = 0

    for side in sides:
        if tiles[side[0]] == tiles[side[1]] == tiles[side[2]] == color:
            score = score + 10

    return(score)

# RRE or ERR
def two_fill_one_empty(board, sides, color):
    score = 0

    for side in sides:
        if tiles[side[0]] == tiles[side[1]] == color and tiles[side[2]] == "none":
            score = score + 8
        elif tiles[side[1]] == tiles[side[2]] == color and tiles[side[0]] == "none":
            score = score + 8

    return(score)


def one_fill_one_emp_one_fill(board, sides, color):
    score = 0

    for side in sidesAlt:
        if tiles[side[0]] == color and tiles[side[1]] == "none" and tiles[side[2]] == color:
            if tiles[side[3]] == color:
                score = score + 10
            elif tiles[side[3]] == "none":
                score = score + 8
            else:
                score = score - 2

    return(score)


def two_same_one_diff(board, sides, color):
    score = 0

    for side in sides:
        if tiles[side[0]] != "none" and tiles[side[1]] != "none" and tiles[side[2]] != "none":
            counter = 0
            for tile in side:
                if tiles[tile] == color:
                    counter = counter + 1
            if counter == 2:
                score = score - 4

    return(score)




print(two_same_one_diff(tiles, sides, "Red"))
