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
from gui import GUI, InputBox
# from inputbox import InputBox

# Imports the needed variables, capitalized due to being constants, from the constants.py file
from constants import (CELLWIDTH, CELLHEIGHT,
                      MARGIN, BORDER, COLOR, TOOLBARHEIGHT)

# Initializes all imported pygame modules, as opposed to initalizing them one by one manually.
pg.init()
# Initializes font, must be called after pygame.init to avoid issues.
pg.font.init()
# Initalizes time, by invoking the Clock class. Set equal to a variable called clock.
# Is used to control framerate and avoid flashing images on the screen.
clock = pg.time.Clock()

# Initialize screen/windows
#@todo: Start the GUI here
# Defines a Board() object called gameBoard.
gameBoard = Board()
# Defines a GUI object with parameter gameBoard called screen.
screen = GUI(gameBoard)

# Defines inputBoxes that display on the screen, one each for row, column, and mines.
# InputBox takes parameters as such InputBox(x position, y position, length of box, width of box,
#  surface to display onto, text to take from user input converted to a string from an int)
inputRowBox = InputBox(BORDER + 66, BORDER + 3, 40, 20, screen.window, str(gameBoard.rows))
inputColumnBox = InputBox(BORDER + 66, BORDER + 27, 40, 20, screen.window, str(gameBoard.columns))
inputMineBox = InputBox(BORDER + 163, BORDER + 3, 40, 20, screen.window, str(gameBoard.mines))

# Places the inputRowBox, inputColumnBox, and inputMineBox into an array called input_boxes.
input_boxes = [inputRowBox, inputColumnBox, inputMineBox]

# Defines a boolean value done that is used to control the main game loop.
done = False

# Defines a while loop that represents the main game loop
# While done is false the game will continue. All code indented from this point is in this while loop.
while not done:
    # Keep the game running until the user decides to quit the game.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        # An event handler for when the user presses a mouse button.
        elif event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicks the mouse on the screen, pass the event into mouseClick (in the gui.py)
            screen.mouseClick(event)

        # Sets input(Rows, Cols, or Mines) equal to input(Rows, Cols, or Mines)Box.handle_event with
        # rows passed in as a parameter.  handle_event is a definition within the Inputbox class (inputbox.py) 
        inputRows = inputRowBox.handle_event(event)
        inputCols = inputColumnBox.handle_event(event)
        inputMines = inputMineBox.handle_event(event)

        # Executes if the user puts input into the inputbox for Rows, inputRowBox.
        if (inputRows != None):
            # If the input the user puts into the inputRowBox, check if its a number. 
            # If its not a number, nothing executes.
            if (inputRows.isnumeric()):
                # If the input is a number, convert it to an integer as its currently read in as as string.
                # If the int is over 32, then change it to 32. This limits the size of the board to, 
                # hopefully, fit on a normal 17 inch monitor.
                if (int(inputRows) > 32):
                    inputRows = 32
                # Minimum bounds checking for rows
                if (int(inputRows) < 2):
                    inputRows = 2
                # If the input is under 32 and above 2, this portion will execute without changing the rows.
                # Set the gameBoard variable rows, within the Board class, to the user input, inputRows. 
                # The inputRows must be converted to an int from a string so the Board class can use it.
                gameBoard.rows = int(inputRows)
                # Calls the generateGrid definition on the gameBoard, within Board class.
                gameBoard.generateGrid()
                # Creates a GUI object by passing in gameBoard, names the object screen.
                screen = GUI(gameBoard)
                # Creates a variable inputRowBox.text, that holds a string value of the varaible gameBoard.rows.
                inputRowBox.text = str(gameBoard.rows)
                # Renders font onto the surface of the screen in the inputRowBox.
                # The font.render function takes parameters as such (the text to be displated, antialias, color of text)
                inputRowBox.txt_surface = inputRowBox.font.render(inputRowBox.text, True, COLOR['WHITE'])

        # Most of the code is the same as the above block for inputRowBox.
        # Executes if the user puts input into the inputbox for cols, inputColumnBox.
        if (inputCols != None):
            # If the input the user puts into the inputColBox, check if its a number. 
            # If its not a number, nothing executes.
            if (inputCols.isnumeric()):
                # If the input is a number, convert it to an integer as its currently read in as as string.
                # If the int is over 32, then change it to 32. This limits the size of the board to, 
                # hopefully, fit on a normal 17 inch monitor.
                if (int(inputCols) > 32):
                    inputCols = 32
                # Minimum bounds checking for columns
                if (int(inputCols) < 2):
                    inputCols = 2
                # If the input is under 32 and above 2, this portion will execute without changing the cols.
                # Set the gameBoard variable cols, within the Board class, to the user input, inputCols. 
                # The inputCols must be converted to an int from a string so the Board class can use it.
                gameBoard.columns = int(inputCols)
                # Calls the generateGrid definition on the gameBoard, within Board class.
                gameBoard.generateGrid()
                # recreates a GUI object by passing in gameBoard, names the object screen.
                screen = GUI(gameBoard)
                # Creates a variable inputColumnBox.text, that holds a string value of the varaible gameBoard.columns.
                inputColumnBox.forceSetText(str(gameBoard.columns))


        # Again, most of the code is the same as the above blocks for inputRowBox and inputColumnBox.
        # Executes if the user puts input into the inputbox for mines, inputMineBox.
        if (inputMines != None):
            # If the input the user puts into the inputMineBox, check if its a number. 
            # If its not a number, nothing executes.
            if (inputMines.isnumeric()):
                # If the input is a number, convert it to an integer as its currently read in as as string.
                # If the int is over or ewual to rows*cols on the gameBaord, then change it to 
                # rows*cols-1. This limits the mines on the board so the user won't automatically lose.
                if (int(inputMines) >= gameBoard.rows * gameBoard.columns):
                    inputMines = gameBoard.rows * gameBoard.columns - 1
                # Minimum bounds checking for mines
                if (int(inputMines) < 1):
                    inputMines = 1
                # If the input is under rows*cols for the defined gameBoard size and above 1,
                # this portion will execute without changing the mines.
                # Set the gameBoard variable mines, within the Board class, to the user input, inputMines. 
                # The inputMines must be converted to an int from a string so the Board class can use it.
                gameBoard.mines = int(inputMines)
                # Calls the generateGrid definition on the gameBoard, within Board class.
                gameBoard.generateGrid()
                # Creates a GUI object by passing in gameBoard, names the object screen.
                screen = GUI(gameBoard)
                # Creates a variable inputMineBox.text, that holds a string value of the varaible gameBoard.mines.
                inputMineBox.text = str(gameBoard.mines)
                 # Renders font onto the surface of the screen in the inputMineBox.
                # The font.render function takes parameters as such (the text to be displated, antialias, color of text)
                inputMineBox.txt_surface = inputMineBox.font.render(inputMineBox.text, True, COLOR['WHITE'])

    # Using box, from the InputBox class, call the update definition on each element in the input_boxes array.
    # This will change the width if the user inputs something that doesn't fit in the box but,
    # as you may have noticed from the above boxes, a value too large will not be kept.
    # for box in input_boxes:
    #     box.update()

    # Fills the screen with a single color, we chose black, every other element will be drawn ontop of this.
    screen.window.fill(COLOR['BLACK'])

    # Using box, from the InputBox class, call the draw definition on each element in the input_boxes array.
    # This will blit the box onto the screen.
    # Blit works by drawing something onto the surface of something else.
    # In this case, we draw the inputbox onto the screen, which why we pass the screen as a parameter.
    for box in input_boxes:
        box.draw()

    # Using screen, from the GUI class, call the uiElement defintion passing in parameters for 
    # X position, Y position, width, height, borderWidth, type to display (text), label to show on screen.
    screen.uiElement(BORDER, BORDER, screen.width - (BORDER * 2), TOOLBARHEIGHT, 1)
    screen.uiElement(BORDER + 6, BORDER + 8, 0, 0, 0, "text", "Rows:")
    screen.uiElement(BORDER + 6, BORDER + 33, 0, 0, 0, "text", "Columns:")
    screen.uiElement(BORDER + 120, BORDER + 8, 0, 0, 0, "text", "Mines:")
    screen.uiElement(BORDER + 120, BORDER + 33, 0, 0, 0, "text", "Flags:    " + str(gameBoard.mines - gameBoard.flagsPlaced))
    # Call the drawBoard definition on screen.
    screen.drawBoard()

    # display.flip will redraw entire window each frame. Good enough for Minesweeper.
    pg.display.flip()
    # clock.tick limits the fps of the program.  Using 20 as a parameter runs the program at 20 fps.
    # We do this to limit flashes on the screen or tearing of an image.  Minesweeper doesn't need much.
    clock.tick(20)

# Quits the game when the user closes the window the game is displayed in.
pg.quit()
