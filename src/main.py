import sys
import pygame
import pygame.locals
import neat
import os

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
    global renderFlag
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)
        if genome.fitness >= 20:
            renderFlag = True
            eval_genome(genome, config)


def eval_genome(genome, config):
    global tickCounter, renderFlag
    controller = aiController.aiController(genome, config)
    board = Board(controller) 
    board.startGame(tickCounter)
    running = True
    while running:
        if renderFlag:
            render(board)
        board.tickBoard(tickCounter)
        tickCounter += 1
        if board.gameEndFrame != -1:
            running = False
    fitness = board.calculateFitness()
    # print(f"Genome {genome.key} fitness: {fitness}")
    return fitness

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
