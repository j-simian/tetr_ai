import sys
import pygame
import pygame.locals

from board import Board
import gfx
import ui

saveOutput = False
saveDir = ""
tickCounter = 0

drop_rate = 36
soft_drop_rate = 18

def main():
    global saveOutput
    global saveDir
    global tickCounter
    if len(sys.argv) > 2: 
        if sys.argv[1] == "-s": # If cli argument -s is used, enable the saveOutput flag
            saveOutput = True
            saveDir = sys.argv[2]
    board = Board()
    board.spawnTetromino()
    ai_board = Board()
    ai_board.spawnTetromino()
    gfx.initGfx()
    clock = pygame.time.Clock()
    running = True
    while running:
        render(ai_board if ui.whichBoard else board)
        clock.tick(60)
        if tickCounter % drop_rate == 0 or (ui.softDrop and tickCounter % soft_drop_rate == 0): # 48/60 = 0.8s per update
            board.tickBoard()
            ai_board.tickBoard()
        tickCounter += 1
        tickCounter %= 1000
        ui.handleUI(pygame.event.get(), board)
    pygame.quit()

def render(board):
    gfx.clearScreen()
    gfx.renderBoard(board.board, board.tetrominoes)
    gfx.renderBag(board.bag, board.nextBag)
    if board.tetrInHold != -1:
        gfx.renderHold(board.tetrominoes[board.tetrInHold])
    gfx.swapBuffers()
    if saveOutput:
        fileName = saveDir + "img" + str(tickCounter).zfill(3) + ".png"
        pygame.image.save(gfx.screen, fileName, "")


if __name__ == "__main__":
    main()
