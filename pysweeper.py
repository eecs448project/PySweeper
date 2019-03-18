# External imports needed for PySweeper
import pygame as pg

# Internal imports needed for PySweeper
from board import Board
from cell import Cell
from gui import GUI, UIElement, InputBox, InputButton, Sound
# from inputbox import InputBox


# GLOBAL constants
from constants import (CELLWIDTH, CELLHEIGHT,
                       MARGIN, BORDER,
                       COLOR, TOOLBARHEIGHT)

def main():
    """ PySweeper main() function.
        The main function is broken down into 3 sections.

        1. Initialization: Initialize pygame and our own pysweeper objects.
        2. Declare all the UI elements we need for the game.
        3. Run a while loop and listen for events. The while loop is broken down
           into two subsections.
           a. Listen for events provided by pygame. event.type is continually
              populated by pygame.
           b. Draw our elements based on current state of game and button states.
    """
    # 1. Initialization: Pygame objects
    pg.init()
    pg.font.init()
    pg.mixer.pre_init(44100, -16, 2, 512)
    pg.mixer.init()
    gameSound = Sound()
    #These bools are used so that sounds don't play more than once per click.
    winBool = True
    lossBool = True
    helpBool = True
    cheatBool = False
    # PySweeper objects
    gameBoard = Board()
    screen = GUI(gameBoard)

    # 2. Declarations
    # Our text elements.
    toolbarRowsText = UIElement(BORDER + 6, BORDER + 8, 0, 0, screen, "Rows:")
    toolbarColumnsText = UIElement(BORDER + 6, BORDER + 33, 0, 0, screen, "Columns:")
    toolbarMinesText = UIElement(BORDER + 120, BORDER + 8, 0, 0, screen, "Mines:")
    # Help bar that is drawn when help is pushed.
    toolbarHelpLMB = UIElement(BORDER + 6, BORDER + 5, 0, 0, screen, "Left click to reveal space.")
    toolbarHelpRMB = UIElement(BORDER + 6, BORDER + 22, 0, 0, screen, "Right click to flag space.")
    toolbarHelpWin = UIElement(BORDER + 6, BORDER + 40, 0, 0, screen, "Flag all mines to win game.")
    inputHelpButton = InputButton(BORDER + 218, BORDER + 5, 45, 20, screen, "Help ")
    # Cheat Button that will call Cheat Mode
    inputCheatButton = InputButton(BORDER + 218, BORDER + 30, 45, 20, screen, "Cheat ")
    toolbarCheat = UIElement(BORDER + 6, BORDER + 5, 0, 0, screen, "You are currently in Cheat Mode.")
    toolbarCheat2 = UIElement(BORDER + 6, BORDER + 22, 0, 0, screen, "Click Cheat again to Return.")
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
    uiCheatElements = [toolbarCheat, toolbarCheat2]
    input_boxes = [inputRowBox, inputColumnBox, inputMineBox, inputHelpButton, inputCheatButton]
    input_buttons = [inputQuitButton, inputRestartButton]

    done = False
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
                                helpBool = True
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
        # Only draw elements based on game state.
        if gameBoard.gameOver:              # Gameover
            if gameBoard.wonGame:
                toolbarGameOverWon.draw()
                if winBool:
                    gameSound.wins()
                    winBool = False
            else:
                toolbarGameOverLost.draw()
                if lossBool:
                    gameSound.loss()
                    lossBool = False
            for button in input_buttons:
                button.draw()
            if inputQuitButton.active == True:
                done = True
            if inputRestartButton.active == True:
                inputRestartButton.restart(screen, gameBoard)
                winBool = True
                lossBool = True
        elif inputHelpButton.active:        # Help active
            for element in uiHelpElements:
                element.draw()
            inputHelpButton.draw()
            if helpBool:
                gameSound.helps()
                helpBool = False
        if inputCheatButton.active:
            for element in uiCheatElements:
                element.draw()
            inputCheatButton.draw()
            gameBoard.generateCheatGrid()
            cheatBool = True
        else:                               # Default UI elements
            for element in uiElements:
                element.draw()
            #todo: These flags need to be updated dynamically. How do we do that?
            flagsRemaining = str(gameBoard.mines - gameBoard.flagsPlaced)
            toolbarFlagsText = UIElement(BORDER + 120, BORDER + 33, 0, 0, screen, "Flags:    " + flagsRemaining)
            toolbarFlagsText.draw()
            for box in input_boxes:
                box.draw()
            inputHelpButton.draw()
            if cheatBool == True:
                gameBoard.removeCheatGrid()
                cheatBool = False

        screen.drawBoard()
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    main()
