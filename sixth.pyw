from sixth import *
import pygame
import os
os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'
pygame.init()
screen = pygame.display.set_mode((1200, 900),pygame.SRCALPHA)
pygame.display.set_caption("sixth")
clock = pygame.time.Clock()
sto=storage()

class Object:
    pass

class Room:
    pass

class Grid(Object):
    pass

class Enrty(Room):
    pass

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
