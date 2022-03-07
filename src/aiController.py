import random
import copy
import neat

class aiController:
    ACTIONS = ["left", "right", "drop", "hard_drop", "hold", "spin_cw", "spin_ccw", "spin2", "nil"]

    genome = ""
    def __init__(self, genome, config):
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, config)

    # def returnAction(self, board):
    #     inputs = []
    #     for i,v in enumerate(board.board):
    #         for j,x in enumerate(board.board[i]):
    #             inputs.append(0 if board.board[i][j] == 0 or board.board[i][j] == board.tetrInPlay else 1)
    #     for i in board.SHAPES:
    #         inputs.append(1 if board.tetrominoes[board.tetrInPlay].type == i else 0)
    #     outputs = self.net.activate(inputs)
    #     action = outputs.index(max(outputs))
        # return aiController.ACTIONS[action]

    def tryPos(self, board, pos):
        x = pos // 4
        r = pos % 4
        copyBoard = copy.deepcopy(board)
        copyBoard.tetrominoes[copyBoard.tetrInPlay].x = x
        copyBoard.tetrominoes[copyBoard.tetrInPlay].rotation = r
        copyBoard.updateBoard(-1)
        copyBoard.tetrominoes[copyBoard.tetrInPlay].hardDrop()
        copyBoard.updateBoard(-1)
        inputs = [sum(board.getAggregateHeights()), board.countHoles(), board.linesCleared, board.getBumpiness()]
        outputs = self.net.activate(inputs)
        return outputs[0]
    
    def getEval(self, board):
        inputs = []
        for i,v in enumerate(board.board):
            for j,x in enumerate(board.board[i]):
                inputs.append(0 if board.board[i][j] == 0 or board.board[i][j] == board.tetrInPlay else 1)
        for i in board.SHAPES:
            inputs.append(1 if board.tetrominoes[board.tetrInPlay].type == i else 0)
        inputs = [sum(board.getAggregateHeights()), board.countHoles(), board.linesCleared, board.getBumpiness()]
        outputs = self.net.activate(inputs)
        return outputs[0]

    def getX(self, board):
        return self.getEval(board)//4

    def getRot(self, board):
        return self.getEval(board) % 4

    def performSkilled(self, board):
        pos = 0
        fits = []
        for i in range(0,32):
            fits.append(self.tryPos(board, i))
        pos = fits.index(max(fits))
        if pos == 0:
            pos = random.randint(0, 31)
        board.tetrominoes[board.tetrInPlay].rotation = pos % 4
        board.tetrominoes[board.tetrInPlay].x = pos // 4

    def perform(self, board):
        board.tetrominoes[board.tetrInPlay].rotation = random.randint(0, 3)
        board.tetrominoes[board.tetrInPlay].x = random.randint(0, 7)


    # def perform(self, board):
    #     action = self.returnAction(board)
    #     if action == "nil":
    #         pass
    #     elif action == "left":
    #         board.tetrominoes[board.tetrInPlay].moveLeft()
    #     elif action == "right":
    #         board.tetrominoes[board.tetrInPlay].moveRight()
    #     elif action == "hard_drop":
    #         board.tetrominoes[board.tetrInPlay].hardDrop()
    #     elif action == "hold":
    #         board.hold()
    #     elif action == "spin_cw":
    #         board.tetrominoes[board.tetrInPlay].rotate(True)
    #     elif action == "spin_ccw":
    #         board.tetrominoes[board.tetrInPlay].rotate(False)
    #     elif action == "spin2":
    #         board.tetrominoes[board.tetrInPlay].rotate(True)
    #         board.tetrominoes[board.tetrInPlay].rotate(True)
