class Tree:
    root = Node()

class Node:
    def __init__(parent, children, boardState, lastMove, minimaxVal):
        self.parent = parent
        self.children = children
        self.boardState = boardState
        self.lastMove = lastMove
        self.minimaxVal = minimaxVal
    
    parent = None
    children = []
    boardState =[]
    lastMove = { "color": "white", "pieceIdx": -1, "movePos": "a" }
    minimaxVal = 0