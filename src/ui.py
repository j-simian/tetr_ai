from threading import Timer
import pygame

key_pause = pygame.K_ESCAPE
key_hold = pygame.K_LSHIFT
key_left = pygame.K_a
key_right = pygame.K_d
key_drop = pygame.K_s
key_hard_drop = pygame.K_SPACE
key_rotate = pygame.K_w
key_rotate_counter = pygame.K_q

softDrop = False

def checkHeld(left, board):
    if pygame.key.get_pressed()[key_left if left else key_right]:
        for i in range(0, 10):
            if left:
                board.tetrominoes[board.tetrInPlay].moveLeft() 
            else:
                board.tetrominoes[board.tetrInPlay].moveRight() 

def handleUI(events, board):
    global softDrop
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == key_rotate:
                board.tetrominoes[board.tetrInPlay].rotate(True)
            if event.key == key_rotate_counter:
                board.tetrominoes[board.tetrInPlay].rotate(False)
            elif event.key == key_left:
                board.tetrominoes[board.tetrInPlay].moveLeft()
                r = Timer(0.30, checkHeld, [True, board])
                r.start()
            elif event.key == key_right:
                board.tetrominoes[board.tetrInPlay].moveRight()
                r = Timer(0.30, checkHeld, [False, board])
                r.start()
            elif event.key == key_hard_drop:
                board.tetrominoes[board.tetrInPlay].hardDrop()
            elif event.key == key_hold:
                board.hold()
            elif event.key == key_drop:
                softDrop = True
        elif event.type == pygame.KEYUP:
            if event.key == key_drop:
                softDrop = False
        elif event.type == pygame.QUIT:
            pygame.quit()
