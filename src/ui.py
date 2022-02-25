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
key_rotate_counter = pygame.K_q

softDrop = False

def checkHeld(left):
    if pygame.key.get_pressed()[key_left if left else key_right]:
        for i in range(0, 10):
            if left:
                state.tetrominoes[state.tetrInPlay].moveLeft() 
            else:
                state.tetrominoes[state.tetrInPlay].moveRight() 

def handleUI(events):
    global softDrop
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == key_rotate:
                state.tetrominoes[state.tetrInPlay].rotate(True)
            if event.key == key_rotate_counter:
                state.tetrominoes[state.tetrInPlay].rotate(False)
            elif event.key == key_left:
                state.tetrominoes[state.tetrInPlay].moveLeft()
                r = Timer(0.30, checkHeld, [True])
                r.start()
            elif event.key == key_right:
                state.tetrominoes[state.tetrInPlay].moveRight()
                r = Timer(0.30, checkHeld, [False])
                r.start()
            elif event.key == key_hard_drop:
                state.tetrominoes[state.tetrInPlay].hardDrop()
            elif event.key == key_hold:
                state.hold()
            elif event.key == key_drop:
                softDrop = True
        elif event.type == pygame.KEYUP:
            if event.key == key_drop:
                softDrop = False
        elif event.type == pygame.QUIT:
            pygame.quit()
