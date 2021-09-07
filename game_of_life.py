###############################################################################
################################# IMPORTS #####################################
###############################################################################

import numpy as np
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

def update_step(grid):
    """
    Compute an iteration of the game of life
    """

    # For all the cells of the grid
    for l in range(MAX_SIZE_GRID):
        for c in range(MAX_SIZE_GRID):
            nb_neighbors = 0
            current_cell = grid[l][c]

            # Count the number of neighbors
            for neighbor_x, neighbor_y in NEIGHBORS:
                if 0 <= l+neighbor_y < MAX_SIZE_GRID and 0 <= c+neighbor_x < MAX_SIZE_GRID:
                    neighbor = grid[l+neighbor_y][c+neighbor_x]
                    if neighbor.current_state == ALIVE:
                        nb_neighbors += 1

            # Apply the game of life's rules
            if current_cell.current_state == ALIVE:
                if nb_neighbors < UNDERPOPULATION or nb_neighbors > OVERPOPULATION:
                    current_cell.next_state = DEAD
                else:
                    current_cell.next_state = ALIVE
            elif nb_neighbors == REPRODUCTION:
                current_cell.next_state = ALIVE

    # Apply the update state
    for line in grid:
        for cell in line:
            cell.current_state = cell.next_state

    return grid

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
MID_SIZE_GRID = MAX_SIZE_GRID // 2
NEIGHBORS = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
UNDERPOPULATION, OVERPOPULATION, REPRODUCTION = 2, 3, 3
UPDATE_TIME = 500
FPS = 100

nb_cells = 25
grid = np.array([[Cell(DEAD, DEAD) for x in range(MAX_SIZE_GRID)] for y in range(MAX_SIZE_GRID)])
grid[72][72].current_state = ALIVE
grid[72][73].current_state = ALIVE
grid[72][74].current_state = ALIVE
active_game = True
time = 0

###############################################################################
################################## MAIN #######################################
###############################################################################

pygame.init()

window = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption("Game of life")


surface = draw_grid(nb_cells, grid[MID_SIZE_GRID - nb_cells//2:MID_SIZE_GRID + nb_cells//2 + 1, MID_SIZE_GRID - nb_cells//2:MID_SIZE_GRID + nb_cells//2 + 1])
window.blit(surface, (0, 0))

clock = pygame.time.Clock()

while active_game:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            active_game = False
        elif event.type == MOUSEWHEEL:
            if event.y == SCROLL_UP and nb_cells > MIN_SIZE_GRID:
                nb_cells -= 2
            elif event.y == SCROLL_DOWN and nb_cells < MAX_SIZE_GRID:
                nb_cells += 2

    time += clock.get_time()
    if time > UPDATE_TIME:
        time = 0
        grid = update_step(grid)

    nb_cells_to_show = nb_cells//2

    surface = draw_grid(nb_cells, grid[MID_SIZE_GRID - nb_cells_to_show:MID_SIZE_GRID + nb_cells_to_show + 1, MID_SIZE_GRID - nb_cells_to_show:MID_SIZE_GRID + nb_cells_to_show + 1])
    window.blit(surface, (0, 0))

    pygame.display.flip()

pygame.quit()