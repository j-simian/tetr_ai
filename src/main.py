import sys
import pygame
from pygame.locals import *
import time
from threading import Timer

from state import Tetromino
import state
import gfx
import ui

saveOutput = False
saveDir = ""
tickCounter = 0

def checkHeld(left):
    if pygame.key.get_pressed()[ui.key_left if left else ui.key_right]:
        for i in range(0, 10):
            if left:
                state.tetrominoes[state.tetrInPlay].moveLeft() 
            else:
                state.tetrominoes[state.tetrInPlay].moveRight() 
        #state.tetrominoes[state.tetrInPlay].x = (0-state.tetrominoes[state.tetrInPlay].getLeftBoundary() if left else len(state.board[0])-1-state.tetrominoes[state.tetrInPlay].getRightBoundary())


def main():
    global saveOutput
    global saveDir
    global tickCounter
    if len(sys.argv) > 2:
        if sys.argv[1] == "-s":
            saveOutput = True
            saveDir = sys.argv[2]

    state.initBoard()
    state.spawnTetromino()
    gfx.initGfx()
    clock = pygame.time.Clock()
    running = True
    while running:
        render()
        clock.tick(60)
        if tickCounter % 48 == 0: # 48/60 = 0.8s per update
            state.tickBoard()
        tickCounter += 1
        tickCounter %= 1000
        ui.handleUI(pygame.event.get())
    pygame.quit()

def render():
    gfx.clearScreen()
    gfx.renderBoard(state.board, state.tetrominoes)
    gfx.renderBag(state.bag, state.nextBag)
    if state.tetrInHold != -1:
        gfx.renderHold(state.tetrominoes[state.tetrInHold])
    gfx.swapBuffers()
    if saveOutput:
        pygame.image.save(gfx.screen, saveDir+"img"+str(tickCounter).zfill(3)+".png", "")


if __name__ == "__main__":
    main()
