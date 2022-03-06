import copy
import math
import random
from tetromino import Tetromino

class Board:
    SPAWN_HEIGHT = 20
    SHAPES = ["O", "I", "T", "L", "J", "S", "Z"] # List of the available pieces
    SHAPE_MASKS = { # A dictionary of piece names to an array of masks for that piece (Each array contains 4 arrays of tuples, being the squares taken up by that shape rotated by an additional 90 degrees for each array)
            'O': [[(0, 1), (0, 0), (1, 1), (1, 0)], [(0, 1), (0, 0), (1, 1), (1, 0)], [(0, 1), (0, 0), (1, 1), (1, 0)], [(0, 1), (0, 0), (1, 1), (1, 0)]], 
            'I': [[(-1, 1), (0, 1), (1, 1), (2, 1)], [(1, 2), (1, 1), (1, 0), (1, -1)], [(-1, 0), (0, 0), (1, 0), (2, 0)], [(0, 2), (0, 1), (0, 0), (0, -1)]], 
            'T': [[(-1, 1), (0, 1), (1, 1), (0, 2)], [(0, 0), (0, 1), (1, 1), (0, 2)], [(-1, 1), (0, 1), (1, 1), (0, 0)], [(-1, 1), (0, 1), (0, 0), (0, 2)]], 
            'L': [[(-1, 1), (0, 1), (1, 1), (1, 2)], [(0, 2), (0, 1), (0, 0), (1, 0)], [(-1, 1), (0, 1), (1, 1), (-1, 0)], [(0, 2), (0, 1), (0, 0), (-1, 2)]], 
            'J': [[(-1, 1), (0, 1), (1, 1), (-1, 2)], [(0, 2), (0, 1), (0, 0), (1, 2)], [(-1, 1), (0, 1), (1, 1), (1, 0)], [(0, 2), (0, 1), (0, 0), (-1, 0)]], 
            'S': [[(-1, 1), (0, 1), (0, 2), (1, 2)], [(1, 1), (0, 1), (0, 2), (1, 0)], [(-1, 0), (0, 0), (0, 1), (1, 1)], [(0, 1), (-1, 1), (-1, 2), (0, 0)]], 
            'Z': [[(1, 1), (0, 1), (0, 2), (-1, 2)], [(1, 1), (0, 1), (0, 0), (1, 2)], [(1, 0), (0, 0), (0, 1), (-1, 1)], [(0, 1), (-1, 1), (-1, 0), (0, 2)]]
            }

    gameBeginFrame = -1 # this is set to the tick num on game start
    gameEndFrame = -1 # set on game end to calculate duration
    playing = False
    death = False

    tetrominoes = {} 
    tetrInPlay = -1
    tetrInHold = -1

    linesCleared = 0

    score = 0
    canHold = True


    def __init__(self, aiController):
        self.playing = False
        self.empty_board = []
        for i in range(0, 40):
            row = []
            for j in range(0, 10):
                row.append(0)
            self.empty_board.append(row)
        self.board = copy.deepcopy(self.empty_board)
        self.bag = random.sample(Board.SHAPES, len(Board.SHAPES))  
        self.nextBag = random.sample(Board.SHAPES, len(Board.SHAPES))  
        self.tetronimoes = []
        self.tetrInPlay = -1
        self.tetrInHold = -1
        if aiController is not None:
            self.aiController = aiController 
        else:
            self.aiController = None

    def startGame(self, now):
        self.gameBeginFrame = now
        self.spawnTetromino()
        self.playing = True

    def endGame(self, now):
        self.gameEndFrame = now
        self.playing = False

    def getAggregateHeights(self):
        heights = [0]*10
        for depth, row in enumerate(self.board):
            for col, piece in enumerate(row):
                if heights[col] < depth and piece != 0:
                    heights[col] = depth
        return heights

    def getBumpiness(self):
        heights = self.getAggregateHeights()
        diffs = 0
        for i in range(0, len(heights)-1):
            diffs += abs(heights[i] - heights[i+1])
        return diffs

    def countHoles(self):
        holes = 0
        heights = self.getAggregateHeights()
        for depth, row in enumerate(self.board):
            for col, piece in enumerate(row):
                if heights[col] > depth and piece == 0:
                    holes += 1
        return holes

    def calculateFitness(self):
        if self.gameEndFrame == -1:
            return -1
        lines = self.linesCleared
        height = sum(self.getAggregateHeights())
        bumpiness = self.getBumpiness()
        holes = self.countHoles()
        fitness = -0.31 * height + 1.76 * lines - 0.06 * holes - 0.38 * bumpiness + (self.gameEndFrame - self.gameBeginFrame) / 5.0
        return fitness
        # if self.death:
        #     return self.linesCleared*10 + (self.gameEndFrame - self.gameBeginFrame) / 100.0
        # else:
        #     return 400 + (50000/(self.gameEndFrame - self.gameBeginFrame))

    def spawnTetromino(self):
        self.canHold = True # Reset player ability to hold
        if len(self.bag) == 0:
            self.genBag()
        t = Tetromino(self.bag[0], self)
        self.bag.pop(0)
        if len(self.bag) == 0:
            self.genBag()
        self.tetrominoes[t.id]=t
        self.tetrInPlay = t.id

    def genBag(self): 
        self.bag = self.nextBag
        self.nextBag = random.sample(Board.SHAPES, len(Board.SHAPES))

    def updateBoard(self, tickCounter):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if self.board[i][j] == self.tetrInPlay:
                    self.board[i][j] = 0
                if self.board[i][j] != 0 and self.board[i][j] != self.tetrInPlay and self.board[i][j] != self.tetrInHold and i > 19 and tickCounter != -1:
                    self.death = True
                    self.endGame(tickCounter)
        t = self.tetrominoes[self.tetrInPlay] 
        for k in range(0, 4):
            self.board[t.y+Board.SHAPE_MASKS[t.type][t.rotation][k][1]][t.x+Board.SHAPE_MASKS[t.type][t.rotation][k][0]] = t.id
        


    def clearLine(self, i):
        self.score += 1000
        k=i
        while(k<len(self.board)-1):
            self.board[k]=copy.deepcopy(self.board[k+1])
            k += 1
        if self.tetrInHold != -1:
            self.tetrominoes[self.tetrInHold].y = Board.SPAWN_HEIGHT
        self.linesCleared += 1

    def hold(self):
        if not self.canHold:
            return
        self.canHold = False
        self.tetrominoes[self.tetrInPlay].y = 30
        self.updateBoard(-1)
        if self.tetrInHold == -1:
            self.tetrInHold = self.tetrInPlay
            self.spawnTetromino()
        else:
            temp = self.tetrInHold
            self.tetrInHold = self.tetrInPlay
            self.tetrInPlay = temp
        self.tetrominoes[self.tetrInPlay].x = 5
        self.tetrominoes[self.tetrInPlay].y = Board.SPAWN_HEIGHT

    def tickBoard(self, tickCounter): 
        if not self.playing:
            return
        if self.tetrInPlay != -1:
            self.tetrominoes[self.tetrInPlay].checkCollision()
            self.tetrominoes[self.tetrInPlay].y -= 1
        self.updateBoard(tickCounter)
        if self.linesCleared >= 3:
            self.endGame(tickCounter)
        if self.aiController is not None:
            self.aiController.perform(self)
