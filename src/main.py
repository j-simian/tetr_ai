import pygame
from pygame.locals import *
import time
from threading import Timer

from state import Tetromino
import state
import gfx
import ui

def checkHeld(left):
    if pygame.key.get_pressed()[ui.key_left if left else ui.key_right]:
        for i in range(0, 10):
            if left:
                state.tetrominoes[state.tetrInPlay].moveLeft() 
            else:
                state.tetrominoes[state.tetrInPlay].moveRight() 
        #state.tetrominoes[state.tetrInPlay].x = (0-state.tetrominoes[state.tetrInPlay].getLeftBoundary() if left else len(state.board[0])-1-state.tetrominoes[state.tetrInPlay].getRightBoundary())

def main():
    state.initBoard()
    state.spawnTetromino()
    gfx.initGfx()
    clock = pygame.time.Clock()
    running = True
    tickCounter = 0
    while running:
        render()
        clock.tick(60)
        if tickCounter % 48 == 0:
            state.tickBoard()
        tickCounter += 1
        tickCounter %= 1000
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ui.key_rotate:
                    state.tetrominoes[state.tetrInPlay].rotate()
                if event.key == ui.key_left:
                    state.tetrominoes[state.tetrInPlay].moveLeft()
                    r = Timer(0.30, checkHeld, [True])
                    r.start()
                if event.key == ui.key_right:
                    state.tetrominoes[state.tetrInPlay].moveRight()
                    r = Timer(0.30, checkHeld, [False])
                    r.start()
                if event.key == ui.key_hard_drop:
                    state.tetrominoes[state.tetrInPlay].hardDrop()
                if event.key == ui.key_hold:
                    state.hold()
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

def render():
    gfx.clearScreen()
    gfx.renderBoard(state.board, state.tetrominoes)
    gfx.renderBag(state.bag, state.nextBag)
    if state.tetrInHold != -1:
        gfx.renderHold(state.tetrominoes[state.tetrInHold])
    gfx.swapBuffers()


if __name__ == "__main__":
    main()
