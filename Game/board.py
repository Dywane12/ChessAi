import itertools

import pygame
import time

'''
Draws the board of the game
Still needs improvements
'''
pygame.init()

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
screen = pygame.display.set_mode((1000, 1000))

colors = itertools.cycle((WHITE,BLACK))
tile_size = 100
width,height = 8 * tile_size, 8 * tile_size
background = pygame.Surface((width,height))

for y in range(0,height,tile_size):
    for x in range(0,width,tile_size):
        rect = (x,y,tile_size,tile_size)
        pygame.draw.rect(background, next(colors), rect)
    next(colors)



def startGame():
    '''
    Starts the game and ends when the user closes the window opened
    :return:
    '''
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((60,70,90))
        screen.blit(background,(100, 100))

        pygame.display.flip()

    pygame.quit()
