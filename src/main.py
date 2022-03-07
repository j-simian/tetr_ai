import sys
import pygame
import pygame.locals
import neat
import os
import math

from board import Board
import gfx
import ui
import aiController

CORES = 0

saveOutput = False
saveDir = ""
tickCounter = 0

drop_rate = 36
soft_drop_rate = 18

renderFlag = True
skillFlag = False


def main():
    global saveOutput, saveDir, tickCounter, renderFlag
    if len(sys.argv) > 2: 
        if sys.argv[1] == "-s": # If cli argument -s is used, enable the saveOutput flag
            saveOutput = True
            saveDir = sys.argv[2]
    # board = Board(None)
    # board.startGame(tickCounter)
    # controller = aiController.aiController("")
    # ai_board = Board(controller)
    # ai_board.startGame(tickCounter)
    gfx.initGfx()
    # clock = pygame.time.Clock()
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, os.path.join(os.path.dirname(__file__), 'config-feedforward'))

    p = neat.Population(config)
    # p = neat.Checkpointer.restore_checkpoint("./neat-checkpoint-64")
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))
    winner = p.run(eval_genomes, 300)
    print(winner)
    # running = True
    # while running:
    #     renderFlag = True
    #     eval_genome(winner, config)
    # running = True
    # while running:
    #     render(ai_board if ui.whichBoard else board)
    #     clock.tick(60)
    #     if tickCounter % drop_rate == 0: # 48/60 = 0.8s per update.
    #         board.tickBoard(tickCounter, genomeFitnesses)
    #         ai_board.tickBoard(tickCounter, genomeFitnesses)
    #     tickCounter += 1
        # ui.handleUI(pygame.event.get(), board)
    pygame.quit()

def eval_genomes(genomes, config):
    global tickCounter, skillFlag
    board = Board() 
    board.startGame(tickCounter)
    avgFitness = 0
    for genome_id, genome in genomes:
        controller = aiController.aiController(genome, config)
        running = True
        fitness = []
        for i in range(0, 5):
            board.tickBoard(tickCounter)
            fitness.append(-(controller.getEval(board) - 1.0/(1 - math.exp(-board.calculateFitness())))**2)
            if not skillFlag:
                controller.perform(board)
            else:
                controller.performSkilled(board)
            board.updateBoard(tickCounter)
            board.tetrominoes[board.tetrInPlay].hardDrop()
            board.updateBoard(tickCounter)
            tickCounter += 1
            if board.gameEndFrame != -1:
                running = False
        if renderFlag:
            render(board)
        if not running:
            board = Board() 
            board.startGame(tickCounter)
        genome.fitness = sum(fitness)/len(fitness)
    genomefitnesses = [i.fitness for (k, i) in genomes]
    if sum(genomefitnesses)/len(genomefitnesses) >= -0.5:
        skillFlag = True


def render(board):
    gfx.clearScreen()
    gfx.renderBoard(board.board, board.tetrominoes, board.calculateFitness())
    gfx.renderBag(board.bag, board.nextBag)
    if board.tetrInHold != -1:
        gfx.renderHold(board.tetrominoes[board.tetrInHold])
    gfx.swapBuffers()
    if saveOutput:
        fileName = saveDir + "img" + str(tickCounter).zfill(3) + ".png"
        pygame.image.save(gfx.screen, fileName, "")


if __name__ == "__main__":
    main()
