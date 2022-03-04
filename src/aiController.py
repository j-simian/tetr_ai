import random
import neat

class aiController:
    ACTIONS = ["left", "right", "drop", "hard_drop", "hold", "spin_cw", "spin_ccw", "spin2", "nil"]

    genome = ""
    def __init__(self, genome, config):
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, config)

    def returnAction(self, board):
        inputs = []
        for i,v in enumerate(board.board):
            for j,x in enumerate(board.board[i]):
                inputs.append(0 if board.board[i][j] == 0 or board.board[i][j] == board.tetrInPlay else 1)
        outputs = self.net.activate(inputs)
        action = outputs.index(max(outputs))
        return aiController.ACTIONS[action]

    def perform(self, board):
        action = self.returnAction(board)
        if action == "nil":
            pass
        elif action == "left":
            board.tetrominoes[board.tetrInPlay].moveLeft()
        elif action == "right":
            board.tetrominoes[board.tetrInPlay].moveRight()
        elif action == "hard_drop":
            board.tetrominoes[board.tetrInPlay].hardDrop()
        elif action == "hold":
            board.hold()
        elif action == "spin_cw":
            board.tetrominoes[board.tetrInPlay].rotate(True)
        elif action == "spin_ccw":
            board.tetrominoes[board.tetrInPlay].rotate(False)
        elif action == "spin2":
            board.tetrominoes[board.tetrInPlay].rotate(True)
            board.tetrominoes[board.tetrInPlay].rotate(True)
