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
    surf = pygame.Surface(GRID_DIMENSIONS)
    surf.fill(WHITE)
    
    # Grid
    if GRID_DIMENSIONS[WIDTH] < GRID_DIMENSIONS[HEIGHT]:
        cell_width = GRID_DIMENSIONS[WIDTH] // n
    else:
        cell_width = GRID_DIMENSIONS[HEIGHT] // n

    dx = (GRID_DIMENSIONS[WIDTH] - n*cell_width) // 2
    dy = (GRID_DIMENSIONS[HEIGHT] - n*cell_width) // 2

    for pixel_x in range(dx + cell_width, dx + n*cell_width, cell_width):
        for pixel_y in range(dy, dy + n*cell_width):
            surf.set_at((pixel_x, pixel_y), GREY)

    for pixel_y in range(dy + cell_width, dy + n*cell_width, cell_width):
        for pixel_x in range(dx, dx + n*cell_width):
            surf.set_at((pixel_x, pixel_y), GREY)

    # Living cells
    cell_surf = pygame.Surface((cell_width - 1, cell_width - 1))
    cell_surf.fill(DARK)

    for x in range(n):
        for y in range(n):
            if grid[x][y].current_state == ALIVE:
                surf.blit(cell_surf, (dx + x*cell_width + 1, dy + y*cell_width + 1))

    return surf


def draw_rounded_rectangle(width, height, color, radius):
    """
    Draw a rounded rectangle
    """

    surf = pygame.Surface((width, height), SRCALPHA)

    r = Rect(0, 0, width, height)
    pygame.draw.rect(surf, color, r, border_radius = radius)

    return surf


def play_symbol():
    """
    Draw a play symbol
    """

    surf = pygame.Surface(PLAY_PAUSE_SYMBOL_DIMENSIONS)
    surf.fill(WHITE)
    pygame.draw.polygon(surf, GREY, [[0, 0], [0, 70], [70, 35]])

    return surf


def pause_symbol():
    """
    Draw a pause symbol
    """

    # Draw a vertical line
    line_surf = draw_rounded_rectangle(20, 70, GREY, 10)

    # Create the pause symbol with two vertical lines
    surf = pygame.Surface(PLAY_PAUSE_SYMBOL_DIMENSIONS)
    surf.fill(WHITE)
    surf.blit(line_surf, (0, 0))
    surf.blit(line_surf, (50, 0))

    return surf


def draw_side_panel(pause):
    """
    Draw the control panel
    """

    # White background
    surf = pygame.Surface(PANEL_DIMENSIONS)
    surf.fill(WHITE)

    # Play / Pause symbol
    if pause:
        surf.blit(play_symbol(), (175, 35))
    else:
        surf.blit(pause_symbol(), (175, 35))

    # Step button
    surf.blit(draw_rounded_rectangle(140, 70, GREY, 10), (560, 35))
    fnt = pygame.font.Font(None, 70, bold=True)
    text = fnt.render("step", True, WHITE)
    surf.blit(text, (580, 45))

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

GRID_DIMENSIONS = (840, 840)
PANEL_DIMENSIONS = (840, 140)
PLAY_PAUSE_SYMBOL_DIMENSIONS = (70, 70)
DIMENSIONS = (840, 980)
DARK = (0, 0, 0)
GREY = (127, 127, 127)
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
pause = True
step = False

###############################################################################
################################## MAIN #######################################
###############################################################################

pygame.init()

window = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption("Game of life")


surface = draw_grid(nb_cells, grid[MID_SIZE_GRID - nb_cells//2:MID_SIZE_GRID + nb_cells//2 + 1, MID_SIZE_GRID - nb_cells//2:MID_SIZE_GRID + nb_cells//2 + 1])
panel = draw_side_panel(pause)
window.blit(surface, (0, 0))
window.blit(panel, (0, 840))

clock = pygame.time.Clock()

while active_game:

    clock.tick(FPS)

    for event in pygame.event.get():

        # Quit button
        if event.type == QUIT:
            active_game = False

        # Mouse wheel zoom in / out
        elif event.type == MOUSEWHEEL:
            if event.y == SCROLL_UP and nb_cells > MIN_SIZE_GRID:
                nb_cells -= 2
            elif event.y == SCROLL_DOWN and nb_cells < MAX_SIZE_GRID:
                nb_cells += 2

        # Play, Pause, Step buttons
        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if 175 <= mouse_x <= 245 and 875 <= mouse_y <= 945:
                pause = not pause
            if 560 <= mouse_x <= 700 and 875 <= mouse_y <= 945:
                step = True

    # Update the game continuously
    if not pause:
        time += clock.get_time()
        if time > UPDATE_TIME:
            time = 0
            grid = update_step(grid)

    # Update the game by one iteration only
    elif step:
        step = False
        grid = update_step(grid)

    # Update the grid surface
    nb_cells_to_show = nb_cells//2
    surface = draw_grid(nb_cells, grid[MID_SIZE_GRID - nb_cells_to_show:MID_SIZE_GRID + nb_cells_to_show + 1, MID_SIZE_GRID - nb_cells_to_show:MID_SIZE_GRID + nb_cells_to_show + 1])
    window.blit(surface, (0, 0))

    # Update the panel surface
    panel = draw_side_panel(pause)
    window.blit(panel, (0, 840))

    pygame.display.flip()

pygame.quit()