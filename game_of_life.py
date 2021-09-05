###############################################################################
################################# IMPORTS #####################################
###############################################################################

import pygame
from pygame.locals import *

from cell import Cell

###############################################################################
################################ FUNCTIONS ####################################
###############################################################################

def draw_grid(n, grid):
    """
    Draw the map of the game
    """

    # White background
    surf = pygame.Surface(DIMENSIONS)
    surf.fill(WHITE)
    
    # Grid
    if DIMENSIONS[WIDTH] < DIMENSIONS[HEIGHT]:
        cell_width = DIMENSIONS[WIDTH] // n
    else:
        cell_width = DIMENSIONS[HEIGHT] // n

    dx = (DIMENSIONS[WIDTH] - n*cell_width) // 2
    dy = (DIMENSIONS[HEIGHT] - n*cell_width) // 2

    for pixel_x in range(dx + cell_width, dx + n*cell_width, cell_width):
        for pixel_y in range(dy, dy + n*cell_width):
            surf.set_at((pixel_x, pixel_y), DARK)

    for pixel_y in range(dy + cell_width, dy + n*cell_width, cell_width):
        for pixel_x in range(dx, dx + n*cell_width):
            surf.set_at((pixel_x, pixel_y), DARK)

    # Living cells
    cell_surf = pygame.Surface((cell_width, cell_width))
    cell_surf.fill(DARK)

    for x in range(n):
        for y in range (n):
            if grid[y][x].current_state == ALIVE:
                surf.blit(cell_surf, (dx + x*cell_width, dy + y*cell_width))

    return surf

###############################################################################
############################### GLOBAL VARIABLES ##############################
###############################################################################

DIMENSIONS = (640, 640)
DARK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 0, 1
DEAD, ALIVE = 0, 1
FPS = 100

nb_cells = 25
grid = [[Cell(DEAD, DEAD) for x in range(nb_cells)] for y in range(nb_cells)]
grid[0][4].current_state = ALIVE
grid[4][0].current_state = ALIVE
grid[4][4].current_state = ALIVE
active_game = True

###############################################################################
################################## MAIN #######################################
###############################################################################

pygame.init()

window = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption("Game of life")


surface = draw_grid(nb_cells, grid)
window.blit(surface, (0, 0))

clock = pygame.time.Clock()

while active_game:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            active_game = False

    pygame.display.flip()

pygame.quit()