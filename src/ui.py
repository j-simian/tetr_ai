from threading import Timer
import pygame
import state

key_pause = pygame.K_ESCAPE
key_hold = pygame.K_LSHIFT
key_left = pygame.K_a
key_right = pygame.K_d
key_drop = pygame.K_s
key_hard_drop = pygame.K_SPACE
key_rotate = pygame.K_w

softDrop = False

def checkHeld(left):
    if pygame.key.get_pressed()[key_left if left else key_right]:
        for i in range(0, 10):
            if left:
                state.tetrominoes[state.tetrInPlay].moveLeft() 
            else:
                state.tetrominoes[state.tetrInPlay].moveRight() 

def handleUI(events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == key_rotate:
                state.tetrominoes[state.tetrInPlay].rotate()
            if event.key == key_left:
                state.tetrominoes[state.tetrInPlay].moveLeft()
                r = Timer(0.30, checkHeld, [True])
                r.start()
            if event.key == key_right:
                state.tetrominoes[state.tetrInPlay].moveRight()
                r = Timer(0.30, checkHeld, [False])
                r.start()
            if event.key == key_hard_drop:
                state.tetrominoes[state.tetrInPlay].hardDrop()
            if event.key == key_hold:
                state.hold()
            if event.key == key_drop:
                softDrop = True
        if event.type == pygame.KEYUP:
            if event.key == key_drop:
                softDrop = False
        if event.type == pygame.QUIT:
            running = False
