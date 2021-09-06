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
        for y in range(n):
            if grid[x][y].current_state == ALIVE:
                surf.blit(cell_surf, (dx + x*cell_width, dy + y*cell_width))

    return surf


def zoom_out(n, grid):
    """
    Zoom out by increasing the size of the grid: n -> n+2
    """

    if n < MAX_SIZE_GRID:
        # Add lines on the top and bottom
        grid.insert(0, [Cell(DEAD, DEAD) for x in range(n)])
        grid.append([Cell(DEAD, DEAD) for x in range(n)])

        # Add colums on the left and right
        for y in range(len(grid)):
            grid[y].insert(0, Cell(DEAD, DEAD))
            grid[y].append(Cell(DEAD, DEAD))

        # The new grid is now of size n+2 * n+2
        n += 2

    return n, grid


def zoom_in(n, grid):
    """
    Zoom in by decreasing the size of the grid: n -> n-2
    """

    if n > MIN_SIZE_GRID:
        # Remove the leftmost and rightmost colums
        for y in range(n):
            grid[y] = grid[y][1:-1]

        # Remove the top and bottom lines
        grid = grid[1:-1]

        # The new grid is now of size n-2 * n-2
        n -= 2

    return n, grid

###############################################################################
############################### GLOBAL VARIABLES ##############################
###############################################################################

DIMENSIONS = (640, 640)
DARK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 0, 1
DEAD, ALIVE = 0, 1
SCROLL_DOWN, SCROLL_UP = -1, 1
MIN_SIZE_GRID, MAX_SIZE_GRID = 3, 101
FPS = 100

nb_cells = 25
grid = [[Cell(DEAD, DEAD) for x in range(nb_cells)] for y in range(nb_cells)]
grid[12][12].current_state = ALIVE
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
        elif event.type == MOUSEWHEEL:
            if event.y == SCROLL_UP:
                nb_cells, grid = zoom_in(nb_cells, grid)
            elif event.y == SCROLL_DOWN:
                nb_cells, grid = zoom_out(nb_cells, grid)
            
            surface = draw_grid(nb_cells, grid)
            window.blit(surface, (0, 0))

    pygame.display.flip()

pygame.quit()