#Input box code based on https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame/46390412
import os, sys
import random
import pygame as pg

from board import Board
from cell import Cell
from gui import GUI
from inputbox import InputBox

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
inputRowBox = InputBox(BORDER + 66, BORDER + 3, 40, 20, screen.window, str(gameBoard.rows))
inputColumnBox = InputBox(BORDER + 66, BORDER + 27, 40, 20, screen.window, str(gameBoard.columns))

input_boxes = [inputRowBox, inputColumnBox]

# Main game loop
done = False

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        #@todo: Add event handler here
        elif event.type == pg.MOUSEBUTTONDOWN:
            screen.mouseClick(event)

        inputRows = inputRowBox.handle_event(event)
        inputCols = inputColumnBox.handle_event(event)

        if (inputRows != None):
            if (inputRows.isnumeric()):
                gameBoard.rows = int(inputRows)
                gameBoard.generateGrid()
                screen = GUI(gameBoard)

        if (inputCols != None):
            if (inputCols.isnumeric()):
                gameBoard.columns = int(inputCols)
                gameBoard.generateGrid()
                screen = GUI(gameBoard)


    for box in input_boxes:
        box.update()

    # Fill window and redraw toolbar and board.
    #@todo:
    screen.window.fill(COLOR['BLACK'])
    # UI elements here

    for box in input_boxes:
        box.draw(screen)

    screen.uiElement(BORDER, BORDER, screen.width - (BORDER * 2), TOOLBARHEIGHT, 1)
    screen.uiElement(BORDER + 6, BORDER + 8, 0, 0, 0, "text", "Rows:")
    screen.uiElement(BORDER + 6, BORDER + 33, 0, 0, 0, "text", "Columns:")
    screen.drawBoard()

    # Redraw entire window each frame. Good enough for Minesweeper.
    pg.display.flip()
    clock.tick(20)

# Cleanup
pg.quit()
