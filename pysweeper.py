# Input box code based on https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame/46390412

# Imports system and operating system specific parameters and functions.
import os, sys

# Imports the pygame library, makes use of the SDL library for easy multimedia applications.
# as pg allows us to just type pg, instead of pygame, to invoke a pygame function.
import pygame as pg

# Imports each class from the .py file, our files and classes used identical names.
# It is convention in python to capitalize all class names.
from board import Board
from cell import Cell
from gui import GUI, UIElement, InputBox, InputButton
# from inputbox import InputBox

# Imports the needed variables, capitalized due to being constants, from the constants.py file
from constants import (CELLWIDTH, CELLHEIGHT,
                      MARGIN, BORDER, COLOR, TOOLBARHEIGHT)

pg.mixer.pre_init(44100, -16, 2, 512)
pg.mixer.init()
winBool = True
# Initializes all imported pygame modules, as opposed to initalizing them one by one manually.
pg.init()
# Initializes font, must be called after pygame.init to avoid issues.
pg.font.init()
# Initalizes time, by invoking the Clock class. Set equal to a variable called clock.
# Is used to control framerate and avoid flashing images on the screen.
clock = pg.time.Clock() 

# Initialize screen/windows
gameBoard = Board()
screen = GUI(gameBoard)

# Declare the basic UI elements.
toolbarRowsText = UIElement(BORDER + 6, BORDER + 8, 0, 0, screen, "Rows:")
toolbarColumnsText = UIElement(BORDER + 6, BORDER + 33, 0, 0, screen, "Columns:")
toolbarMinesText = UIElement(BORDER + 120, BORDER + 8, 0, 0, screen, "Mines:")
# Declare the help UI elements.

toolbarHelpLMB = UIElement(BORDER + 6, BORDER + 5, 0, 0, screen, "Left click to reveal space.")
toolbarHelpRMB = UIElement(BORDER + 6, BORDER + 22, 0, 0, screen, "Right click to flag space.")
toolbarHelpWin = UIElement(BORDER + 6, BORDER + 40, 0, 0, screen, "Flag all mines to win game.")
inputHelpButton = InputButton(BORDER + 218, BORDER + 15, 40, 20, screen, "Help")
# Declare input UI elements.
inputRowBox = InputBox(BORDER + 66, BORDER + 3, 40, 20, screen, 30, 2,  str(gameBoard.rows))
inputColumnBox = InputBox(BORDER + 66, BORDER + 27, 40, 20, screen, 30, 2, str(gameBoard.columns))
inputMineBox = InputBox(BORDER + 163, BORDER + 3, 40, 20, screen, 10, 1, str(gameBoard.mines))
# Declare button UI elements.
inputQuitButton = InputButton(BORDER + 60, BORDER + 30, 40, 20, screen, "Quit")
inputRestartButton = InputButton(BORDER + 110, BORDER + 30, 55, 20, screen, "Restart")
# Declare gameOver UI elements.

toolbarGameOverLost = UIElement(BORDER + 75, BORDER + 10, 0, 0, screen, "GAME OVER")
toolbarGameOverWon = UIElement(BORDER + 85, BORDER + 10, 0, 0, screen, "WINNER!")

# Arrays of elements need to be grouped by rendering order.
uiElements = [toolbarRowsText, toolbarColumnsText, toolbarMinesText]
uiHelpElements = [toolbarHelpLMB, toolbarHelpRMB, toolbarHelpWin]
input_boxes = [inputRowBox, inputColumnBox, inputMineBox, inputHelpButton]
input_buttons = [inputQuitButton, inputRestartButton]

# Defines a boolean value done that is used to control the main game loop.
done = False

# This while loop is required by pygame. See # for more info.
while not done:
    # Keep the game running until the user decides to quit the game.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            screen.mouseClick(event)
            # Handle input boxes here.
            if event.button == 1 or 3:
                if gameBoard.gameOver:
                    for button in input_buttons:
                        if button.rect.collidepoint(event.pos):
                            button.active = True
                if not gameBoard.gameOver:
                    for box in input_boxes:
                        # If the user clicked on the input box, toggle state.
                        if box.rect.collidepoint(event.pos):
                            box.active = not box.active
                        else:
                            box.active = False
        # Listen for key presses. Input boxes that are active take all inputs.
        elif event.type == pg.KEYDOWN:
            for box in input_boxes:
                # Always check mine max value incase board size is decreased
                if box.active:
                    if event.key == pg.K_RETURN:
                        box.active = not box.active
                        # Calling all 3 works for the time being.
                        inputRowBox.update("rows", inputRowBox.text)
                        inputColumnBox.update("columns", inputColumnBox.text)
                        inputMineBox.maxValue = (screen.board.rows * screen.board.columns) - 1
                        inputMineBox.update("mines", inputMineBox.text)
                    elif event.key == pg.K_BACKSPACE:
                        box.text = box.text[:-1]
                    else:
                        if len(box.text) < 4:
                            box.text += event.unicode

    # Pygame draws elements from back to front. Pygame is also double buffered. The surface
    #+you draw to is not shown to the user until the py.display.flip() flips the buffers.
    screen.window.fill(COLOR['BLACK'])

    if gameBoard.gameOver:
        if gameBoard.wonGame:
            toolbarGameOverWon.draw()
            if winBool:
                screen.winSound()
                winBool = False
        else:
            toolbarGameOverLost.draw()
        for button in input_buttons:
            button.draw()
        if inputQuitButton.active == True:
            done = True
        if inputRestartButton.active == True:
            inputRestartButton.restart(screen, gameBoard)
            winBool = True

    elif inputHelpButton.active:
        for element in uiHelpElements:
            element.draw()
        inputHelpButton.draw()

    else:
        for element in uiElements:
            element.draw()
        #todo: These flags need to be updated dynamically. How do we do that?
        flagsRemaining = str(gameBoard.mines - gameBoard.flagsPlaced)
        toolbarFlagsText = UIElement(BORDER + 120, BORDER + 33, 0, 0, screen, "Flags:    " + flagsRemaining)
        toolbarFlagsText.draw()
        for box in input_boxes:
            box.draw()
        inputHelpButton.draw()

    screen.drawBoard()

    pg.display.flip()

    # For minesweeper 20 fps is plenty.
    #clock.tick(20)

# Quits the game when the user closes the window the game is displayed in.
pg.quit()
