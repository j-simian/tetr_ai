import board as Board

class Tetromino:
    globalIDCounter = 0
    id = -1 #This should be set by a constructor
    x = -1 
    y = -1
    type = "err" # "err" | "O" | "I" | "T" | "L" | "J" | "S" | "Z"
    rotation = 0

    def __init__(self, type, board):
        self.id = 0x00B00000+Tetromino.nextId()
        self.x = 4 
        self.y = Board.Board.SPAWN_HEIGHT
        self.type = type
        self.board = board

    def rotate(self, clockw):
        self.rotation = (self.rotation+1 if clockw else self.rotation-1)%4
        if self.x + self.getRightBoundary() >= len(self.board.board[0]) or self.x + self.getLeftBoundary() < 0 or self.getLowerBoundary() < 0:
            self.rotation = (self.rotation-1 if clockw else self.rotation+1)%4
        else:
            self.board.updateBoard(-1)


    def getLowerBoundary(self):
        return min(Board.Board.SHAPE_MASKS[self.type][self.rotation], key=lambda i : i[1])[1]

    def getUpperBoundary(self):
        return max(Board.Board.SHAPE_MASKS[self.type][self.rotation], key=lambda i : i[1])[1]

    def getLeftBoundary(self):
        return min(Board.Board.SHAPE_MASKS[self.type][self.rotation], key=lambda i : i[0])[0]

    def getRightBoundary(self):
        return max(Board.Board.SHAPE_MASKS[self.type][self.rotation], key=lambda i : i[0])[0]

    def checkCollision(self):
        if self.y + self.getLowerBoundary() < 0:
            self.kill()
        if self.project() == 0:
            self.kill()

    def kill(self):
        self.board.updateBoard(-1)
        for (i, row) in enumerate(self.board.board): # check for a line clear 
            if 0 not in row:
                self.board.clearLine(i)
        self.board.spawnTetromino()

    def project(self):
        can = True
        i = 0
        while can:
            for k in range(0, 4):
                if self.y+Board.Board.SHAPE_MASKS[self.type][self.rotation][k][1]-i-1 < 0:
                    can = False
                    continue
                if self.board.board[self.y+Board.Board.SHAPE_MASKS[self.type][self.rotation][k][1]-i-1][self.x+Board.Board.SHAPE_MASKS[self.type][self.rotation][k][0]] not in [0, self.id]:
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
            if self.x+Board.Board.SHAPE_MASKS[self.type][self.rotation][k][0]-1 < 0:
                can = False
                continue
            if self.board.board[self.y+Board.Board.SHAPE_MASKS[self.type][self.rotation][k][1]][self.x+Board.Board.SHAPE_MASKS[self.type][self.rotation][k][0]-1] not in [0, self.id]:
                can = False
        if can:
            self.x -= 1
        self.board.updateBoard(-1)

    def moveRight(self):
        can = True
        for k in range(0, 4):
            if self.x+Board.Board.SHAPE_MASKS[self.type][self.rotation][k][0]+1 >= len(self.board.board[0]):
                can = False
                continue
            if self.board.board[self.y+Board.Board.SHAPE_MASKS[self.type][self.rotation][k][1]][self.x+Board.Board.SHAPE_MASKS[self.type][self.rotation][k][0]+1] not in [0, self.id]:
                can = False
        if can:
            self.x += 1
        self.board.updateBoard(-1)



    @staticmethod
    def nextId():
       Tetromino.globalIDCounter += 1 
       return Tetromino.globalIDCounter

