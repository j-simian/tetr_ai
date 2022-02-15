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

def main():
    global saveOutput
    global saveDir
    global tickCounter
    if len(sys.argv) > 2: # If cli argument -s is used, enable the saveOutput flag
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
        if tickCounter % 48 == 0 or (ui.softDrop and tickCounter % 24 == 0): # 48/60 = 0.8s per update
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
