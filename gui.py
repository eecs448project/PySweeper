import pygame as pg
from constants import (ROWS, COLS, CELLWIDTH, CELLHEIGHT,
                      MARGIN, BORDER, COLOR)
class GUI():
    """ GUI Class:
        Handles all window elements.
    """
    def __init__(self, ROWS, COLS, CELLWIDTH, CELLHEIGHT, MARGIN, BORDER):
        """ Constructor
            Calculate the game window based on board size.
            Defaults: ROWS=10, COLS=10
            PARAMS need to be changed to (self, board). Board object
            will have all the sizes we need.
        """
        #@todo: Generate dynamically based on uiElements
        self.toolbarOffset = 50
        self.width = ((CELLWIDTH + MARGIN) * ROWS) + BORDER
        self.height = ((CELLHEIGHT + MARGIN) * COLS) + BORDER + self.toolbarOffset
        self.size = self.width, self.height
        print("Width: ", self.width, "Height: ", self.height)
        self.window = pg.display.set_mode(self.size)
    
    def update(self, screen, cell):
        """ Updates the window. Called every frame.
            screen = screen to update
            cell = info about cell sizes
        """
        pass
    
    def uiElement(self, x, y, w, h, type='None', label='None'):
        """ Handles creation of all UI elements except board.
        """
        pass