import pygame
from pygame.locals import *

import board

screen_width = 1280
screen_height = 720

# Thanks to https://www.nordtheme.com/docs/colors-and-palettes
colours = [
        ("#2E3440"), ("#3B4252"), ("#434C5E"), ("#4C566A"),
        ("#D8DEE9"), ("#E5E9F0"), ("#ECEFF4"),
        ("#8FBCBB"), ("#88C0D0"), ("#81A1C1"), ("#5E81AC"),
        ("#BF616A"), ("#D08770"), ("#EBCB8B"), ("#A3BE8C"), ("#B48EAD")
        ]

shapeColours = {
    "O":colours[13],
    "I":colours[8],
    "T":colours[15],
    "L":colours[12],
    "J":colours[10],
    "S":colours[14],
    "Z":colours[11]
        }

board_scale = 30
board_padding = 4 

def initGfx():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("AI plays Tetris")
    clearScreen()
    swapBuffers()
    
def clearScreen():
    screen.fill(colours[0])

def swapBuffers():
    pygame.display.flip()

def renderBoard(board, tetronimoes, score):
    font = pygame.font.SysFont(None, 24) 
    img = font.render(f"Score: {score}", True, colours[4]) 
    screen.blit(img, (screen_width - 100, 50))
    for i in range(0, 21):
        for j in range(0, len(board[i])):
            currentColour = colours[1]
            if board[i][j] != 0:
                currentColour = shapeColours[tetronimoes[board[i][j]].type]
            pygame.draw.rect(screen, currentColour, 
                    Rect( j*board_scale + board_padding + (screen_width/2-board_scale/2*len(board[i])),
                        screen_height - 50 - i*board_scale + board_padding/2, 
                        board_scale - board_padding, board_scale - board_padding ) )

def renderBag(bag, nextBag):
    completeBag = bag + nextBag
    for i in range(0, 6):
        for k in range(0, 4):
            currentColour = shapeColours[completeBag[i]]
            pygame.draw.rect(screen, currentColour, 
                    Rect((screen_width/2+board_scale/2*10) + 50 + (board.Board.SHAPE_MASKS[completeBag[i]][0][k][0])*board_scale,
                         50+(board.Board.SHAPE_MASKS[completeBag[i]][0][k][1])*board_scale+3.5*i*board_scale,
                         board_scale,
                         board_scale) )
            
            
def renderHold(tetromino):
    for k in range(0, 4):
        currentColour = shapeColours[tetromino.type]
        pygame.draw.rect(screen, currentColour, 
                Rect((screen_width/2-board_scale/2*10) - 250 - (board.Board.SHAPE_MASKS[tetromino.type][0][k][0])*board_scale,
                     50+(board.Board.SHAPE_MASKS[tetromino.type][0][k][1])*board_scale+3.5*1*board_scale,
                     board_scale,
                     board_scale) )
            

