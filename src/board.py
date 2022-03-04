import copy
import random
from tetromino import Tetromino

class Board:
    SPAWN_HEIGHT = 20
    SHAPES = ["O", "I", "T", "L", "J", "S", "Z"]
    SHAPE_MASKS = { 
            'O': [[(0, 1), (0, 0), (1, 1), (1, 0)], [(0, 1), (0, 0), (1, 1), (1, 0)], [(0, 1), (0, 0), (1, 1), (1, 0)], [(0, 1), (0, 0), (1, 1), (1, 0)]], 
            'I': [[(-1, 1), (0, 1), (1, 1), (2, 1)], [(1, 2), (1, 1), (1, 0), (1, -1)], [(-1, 0), (0, 0), (1, 0), (2, 0)], [(0, 2), (0, 1), (0, 0), (0, -1)]], 
            'T': [[(-1, 1), (0, 1), (1, 1), (0, 2)], [(0, 0), (0, 1), (1, 1), (0, 2)], [(-1, 1), (0, 1), (1, 1), (0, 0)], [(-1, 1), (0, 1), (0, 0), (0, 2)]], 
            'L': [[(-1, 1), (0, 1), (1, 1), (1, 2)], [(0, 2), (0, 1), (0, 0), (1, 0)], [(-1, 1), (0, 1), (1, 1), (-1, 0)], [(0, 2), (0, 1), (0, 0), (-1, 2)]], 
            'J': [[(-1, 1), (0, 1), (1, 1), (-1, 2)], [(0, 2), (0, 1), (0, 0), (1, 2)], [(-1, 1), (0, 1), (1, 1), (1, 0)], [(0, 2), (0, 1), (0, 0), (-1, 0)]], 
            'S': [[(-1, 1), (0, 1), (0, 2), (1, 2)], [(1, 1), (0, 1), (0, 2), (1, 0)], [(-1, 0), (0, 0), (0, 1), (1, 1)], [(0, 1), (-1, 1), (-1, 2), (0, 0)]], 
            'Z': [[(1, 1), (0, 1), (0, 2), (-1, 2)], [(1, 1), (0, 1), (0, 0), (1, 2)], [(1, 0), (0, 0), (0, 1), (-1, 1)], [(0, 1), (-1, 1), (-1, 0), (0, 2)]]
            }

    tetrominoes = {} 
    tetrInPlay = -1
    tetrInHold = -1

    bag = random.sample(SHAPES, len(SHAPES))  

    nextBag = random.sample(SHAPES, len(SHAPES))  
    score = 0
    canHold = True

    def __init__(self):
        self.empty_board = []
        for i in range(0, 40):
            row = []
            for j in range(0, 10):
                row.append(0)
            self.empty_board.append(row)
        self.board = copy.deepcopy(self.empty_board)
        self.tetronimoes = []

    def spawnTetromino(self):
        self.canHold = True # Reset player ability to hold
        t = Tetromino(self.bag[0], self)
        self.bag.pop(0)
        if len(self.bag) == 0:
            self.genBag()
        self.tetrominoes[t.id]=t
        self.tetrInPlay = t.id

    def genBag(self): 
        self.bag = self.nextBag
        self.nextBag = random.sample(Board.SHAPES, len(Board.SHAPES))

    def updateBoard(self):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if self.board[i][j] == self.tetrInPlay:
                    self.board[i][j] = 0
        t = self.tetrominoes[self.tetrInPlay] 
        for k in range(0, 4):
            self.board[t.y+Board.SHAPE_MASKS[t.type][t.rotation][k][1]][t.x+Board.SHAPE_MASKS[t.type][t.rotation][k][0]] = t.id


    def clearLine(self, i):
        print("Tetris found! ")
        self.score += 1000
        k=i
        print(f"{k}, {i}, {len(self.board)}")
        while(k<len(self.board)-1):
            print(self.board[k])
            self.board[k]=copy.deepcopy(self.board[k+1])
            k += 1
        if self.tetrInHold != -1:
            self.tetrominoes[self.tetrInHold].y = Board.SPAWN_HEIGHT

    def hold(self):
        if not self.canHold:
            return
        self.canHold = False
        self.tetrominoes[self.tetrInPlay].y = 30
        self.updateBoard()
        if self.tetrInHold == -1:
            self.tetrInHold = self.tetrInPlay
            self.spawnTetromino()
        else:
            temp = self.tetrInHold
            self.tetrInHold = self.tetrInPlay
            self.tetrInPlay = temp
        self.tetrominoes[self.tetrInPlay].x = 5
        self.tetrominoes[self.tetrInPlay].y = Board.SPAWN_HEIGHT

    def tickBoard(self): 
        if self.tetrInPlay != -1:
            self.tetrominoes[self.tetrInPlay].checkCollision()
            self.tetrominoes[self.tetrInPlay].y -= 1
        self.updateBoard()

