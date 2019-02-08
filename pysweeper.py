import os, sys
import random
import pygame as pg

from board import Board
from cell import Cell
from gui import GUI

from constants import (ROWS, COLS, CELLWIDTH, CELLHEIGHT,
                      MARGIN, BORDER, COLOR)

# PyGame Initializing
pg.init()
clock = pg.time.Clock()

# Initialize screen/windows
#@todo: Start the GUI here
gameBoard = Board()
screen = GUI(ROWS, COLS, CELLWIDTH, CELLHEIGHT, MARGIN, BORDER)

# Main game loop
done = False

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        #@todo: Add event handler here
        elif event.type == pg.MOUSEBUTTONDOWN:
            pass

    # Fill window and redraw toolbar and board.
    #@todo:
    screen.window.fill(COLOR['WHITE'])
    pass
    # Redraw entire window each frame. Good enough for Minesweeper.
    pg.display.flip()
    clock.tick(20)

# Cleanup
pg.quit()
