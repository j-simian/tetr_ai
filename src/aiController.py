import random

class aiController:
    ACTIONS = ["left", "right", "drop", "hard_drop", "hold", "spin_cw", "spin_ccw", "spin2", "nil"]

    def __init__(self, genome):
        self.genome = genome

    def returnAction(self):
        return random.choice(aiController.ACTIONS)

    def perform(self, board):
        action = self.returnAction()
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
