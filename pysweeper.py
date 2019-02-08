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
inputMineBox = InputBox(BORDER + 163, BORDER + 3, 40, 20, screen.window, str(gameBoard.mines))

input_boxes = [inputRowBox, inputColumnBox, inputMineBox]

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
        inputMines = inputMineBox.handle_event(event)

        if (inputRows != None):
            if (inputRows.isnumeric()):
                if (int(inputRows) > 32):
                    inputRows = 32
                gameBoard.rows = int(inputRows)
                gameBoard.generateGrid()
                screen = GUI(gameBoard)
                inputRowBox.text = str(gameBoard.rows)
                inputRowBox.txt_surface = inputRowBox.font.render(inputRowBox.text, True, COLOR['WHITE'])

        if (inputCols != None):
            if (inputCols.isnumeric()):
                if (int(inputCols) > 32):
                    inputCols = 32
                gameBoard.columns = int(inputCols)
                gameBoard.generateGrid()
                screen = GUI(gameBoard)
                inputColumnBox.text = str(gameBoard.columns)
                inputColumnBox.txt_surface = inputColumnBox.font.render(inputColumnBox.text, True, COLOR['WHITE'])

        if (inputMines != None):
            if (inputMines.isnumeric()):
                if (int(inputMines) >= gameBoard.rows * gameBoard.columns):
                    inputMines = gameBoard.rows * gameBoard.columns - 1
                gameBoard.mines = int(inputMines)
                gameBoard.generateGrid()
                screen = GUI(gameBoard)
                inputMineBox.text = str(gameBoard.mines)
                inputMineBox.txt_surface = inputMineBox.font.render(inputMineBox.text, True, COLOR['WHITE'])


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
    screen.uiElement(BORDER + 120, BORDER + 8, 0, 0, 0, "text", "Mines:")
    screen.uiElement(BORDER + 120, BORDER + 33, 0, 0, 0, "text", "Flags:    " + str(gameBoard.mines - gameBoard.flagsPlaced))
    screen.drawBoard()

    # Redraw entire window each frame. Good enough for Minesweeper.
    pg.display.flip()
    clock.tick(20)

# Cleanup
pg.quit()
