import os, sys
import random
import pygame as pg

from board import Board
from cell import Cell
from gui import GUI

from constants import (CELLWIDTH, CELLHEIGHT,
                      MARGIN, BORDER, COLOR, TOOLBARHEIGHT)

# PyGame Initializing
pg.init()
pg.font.init()
clock = pg.time.Clock()

# Initialize screen/windows
#@todo: Start the GUI here
gameBoard = Board()
screen = GUI(gameBoard)

# Main game loop
done = False

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        #@todo: Add event handler here
        elif event.type == pg.MOUSEBUTTONDOWN:
            screen.mouseClick(event)

    # Fill window and redraw toolbar and board.
    #@todo:
    screen.window.fill(COLOR['BLACK'])
    # UI elements here
    screen.uiElement(BORDER, BORDER, screen.width - (BORDER * 2), TOOLBARHEIGHT, 1)
    screen.uiElement(BORDER + 6, BORDER + 8, 0, 0, 0, "text", "Rows:")
    screen.uiElement(BORDER + 66, BORDER + 3, 40, 20, 1, "input")
    screen.uiElement(BORDER + 66, BORDER + 3, 0, 0, 0, "text", str(gameBoard.rows))
    screen.uiElement(BORDER + 6, BORDER + 33, 0, 0, 0, "text", "Columns:")
    screen.uiElement(BORDER + 66, BORDER + 27, 40, 20, 1, "input")
    screen.uiElement(BORDER + 66, BORDER + 27, 0, 0, 0, "text", str(gameBoard.columns))
    screen.drawBoard()

    # Redraw entire window each frame. Good enough for Minesweeper.
    pg.display.flip()
    clock.tick(20)

# Cleanup
pg.quit()
