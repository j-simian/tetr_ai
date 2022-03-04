import sys
import pygame
from pygame.locals import *
import time
from threading import Timer

from board import Board
from tetromino import Tetromino
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
    if len(sys.argv) > 2: # If cli argument -s is used, enable the saveOutput flag
        if sys.argv[1] == "-s":
            saveOutput = True
            saveDir = sys.argv[2]
    board = Board()
    board.spawnTetromino()
    gfx.initGfx()
    clock = pygame.time.Clock()
    running = True
    while running:
        render(board)
        clock.tick(60)
        if tickCounter % drop_rate == 0 or (ui.softDrop and tickCounter % soft_drop_rate == 0): # 48/60 = 0.8s per update
            board.tickBoard()
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
        pygame.image.save(gfx.screen, saveDir+"img"+str(tickCounter).zfill(3)+".png", "")


if __name__ == "__main__":
    main()
