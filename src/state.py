import copy
import random

spawn_height = 20

empty_board = []
board = []
tetrominoes = {} 
tetrInPlay = -1
tetrInHold = -1
shapes = ["O", "I", "T", "L", "J", "S", "Z"]
bag = random.sample(shapes, len(shapes))  
nextBag = random.sample(shapes, len(shapes))  
score = 0
canHold = True

shapeMasks = { 
        'O': [[(0, 1), (0, 0), (1, 1), (1, 0)], [(0, 1), (0, 0), (1, 1), (1, 0)], [(0, 1), (0, 0), (1, 1), (1, 0)], [(0, 1), (0, 0), (1, 1), (1, 0)]], 
        'I': [[(-1, 1), (0, 1), (1, 1), (2, 1)], [(1, 2), (1, 1), (1, 0), (1, -1)], [(-1, 0), (0, 0), (1, 0), (2, 0)], [(0, 2), (0, 1), (0, 0), (0, -1)]], 
        'T': [[(-1, 1), (0, 1), (1, 1), (0, 2)], [(0, 0), (0, 1), (1, 1), (0, 2)], [(-1, 1), (0, 1), (1, 1), (0, 0)], [(-1, 1), (0, 1), (0, 0), (0, 2)]], 
        'L': [[(-1, 1), (0, 1), (1, 1), (1, 2)], [(0, 2), (0, 1), (0, 0), (1, 0)], [(-1, 1), (0, 1), (1, 1), (-1, 0)], [(0, 2), (0, 1), (0, 0), (-1, 2)]], 
        'J': [[(-1, 1), (0, 1), (1, 1), (-1, 2)], [(0, 2), (0, 1), (0, 0), (1, 2)], [(-1, 1), (0, 1), (1, 1), (1, 0)], [(0, 2), (0, 1), (0, 0), (-1, 0)]], 
        'S': [[(-1, 1), (0, 1), (0, 2), (1, 2)], [(1, 1), (0, 1), (0, 2), (1, 0)], [(-1, 0), (0, 0), (0, 1), (1, 1)], [(0, 1), (-1, 1), (-1, 2), (0, 0)]], 
        'Z': [[(1, 1), (0, 1), (0, 2), (-1, 2)], [(1, 1), (0, 1), (0, 0), (1, 2)], [(1, 0), (0, 0), (0, 1), (-1, 1)], [(0, 1), (-1, 1), (-1, 0), (0, 2)]]
        }


def initBoard():
    global board
    for i in range(0, 40):
        row = []
        for j in range(0, 10):
            row.append(0)
        empty_board.append(row)
    board = copy.deepcopy(empty_board)
    tetronimoes = []

def spawnTetromino():
    global tetrInPlay
    global canHold
    canHold = True # Reset player ability to hold
    t = Tetromino(bag[0]);
    bag.pop(0)
    if len(bag) == 0:
        genBag()
    tetrominoes[t.id]=t;
    tetrInPlay = t.id

def genBag(): 
    global bag
    global nextBag
    bag = nextBag
    nextBag = random.sample(shapes, len(shapes))

def updateBoard():
    global board
    global score
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == tetrInPlay:
                board[i][j] = 0
    t = tetrominoes[tetrInPlay] 
    for k in range(0, 4):
        board[t.y+shapeMasks[t.type][t.rotation][k][1]][t.x+shapeMasks[t.type][t.rotation][k][0]] = t.id


def tetris(i):
    global score
    global board
    print("Tetris found! ")
    score += 1000
    k=i
    print(f"{k}, {i}, {len(board)}")
    while(k<len(board)-1):
        print(board[k])
        board[k]=copy.deepcopy(board[k+1])
        k += 1
    if tetrInHold != -1:
        tetrominoes[tetrInHold].y = spawn_height

def hold():
    global tetrInHold
    global tetrInPlay
    global canHold
    if not canHold:
        return
    canHold = False
    tetrominoes[tetrInPlay].y = 30
    updateBoard()
    if tetrInHold == -1:
        tetrInHold = tetrInPlay
        spawnTetromino()
    else:
        temp = tetrInHold
        tetrInHold = tetrInPlay
        tetrInPlay = temp
    tetrominoes[tetrInPlay].x = 5
    tetrominoes[tetrInPlay].y = spawn_height

def tickBoard(): 
    if tetrInPlay != -1:
        tetrominoes[tetrInPlay].checkCollision()
        tetrominoes[tetrInPlay].y -= 1
    updateBoard()

class Tetromino:
    id = -1 #This should be set by a constructor
    x = -1 
    y = -1
    type = "err" # "err" | "O" | "I" | "T" | "L" | "J" | "S" | "Z"
    rotation = 0
    globalIDCounter = 0

    def rotate(self):
       self.rotation = (self.rotation+1)%4
       updateBoard()

    def getLowerBoundary(self):
        return min(shapeMasks[self.type][self.rotation], key=lambda i : i[1])[1]

    def getUpperBoundary(self):
        return max(shapeMasks[self.type][self.rotation], key=lambda i : i[1])[1]

    def getLeftBoundary(self):
        return min(shapeMasks[self.type][self.rotation], key=lambda i : i[0])[0]

    def getRightBoundary(self):
        return max(shapeMasks[self.type][self.rotation], key=lambda i : i[0])[0]

    def checkCollision(self):
        if self.y + self.getLowerBoundary() < 0:
            self.kill()
        if self.project() == 0:
            self.kill()

    def kill(self):
        updateBoard()
        for (i, row) in enumerate(board): # check for a line clear 
            if 0 not in row:
                tetris(i)
        spawnTetromino()

    def project(self):
        can = True
        i = 0
        while can:
            for k in range(0, 4):
                if self.y+shapeMasks[self.type][self.rotation][k][1]-i-1 < 0:
                    can = False
                    continue
                if board[self.y+shapeMasks[self.type][self.rotation][k][1]-i-1][self.x+shapeMasks[self.type][self.rotation][k][0]] not in [0, self.id]:
                    can = False
            if can:
                i += 1
        return i


    def hardDrop(self):
        self.y -= self.project() 
        self.checkCollision()

    def moveLeft(self):
        can = True
        for k in range(0, 4):
            if self.x+shapeMasks[self.type][self.rotation][k][0]-1 < 0:
                can = False
                continue
            if board[self.y+shapeMasks[self.type][self.rotation][k][1]][self.x+shapeMasks[self.type][self.rotation][k][0]-1] not in [0, self.id]:
                can = False
        if can:
            self.x -= 1
        updateBoard()

    def moveRight(self):
        can = True
        for k in range(0, 4):
            if self.x+shapeMasks[self.type][self.rotation][k][0]+1 >= len(board[0]):
                can = False
                continue
            if board[self.y+shapeMasks[self.type][self.rotation][k][1]][self.x+shapeMasks[self.type][self.rotation][k][0]+1] not in [0, self.id]:
                can = False
        if can:
            self.x += 1
        updateBoard()

    def __init__(self, type):
        self.id = 0x00B00000+Tetromino.nextId()
        self.x = 4 
        self.y = spawn_height 
        self.type = type


    @staticmethod
    def nextId():
       Tetromino.globalIDCounter += 1 
       return Tetromino.globalIDCounter

