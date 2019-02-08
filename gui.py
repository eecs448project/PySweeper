import pygame as pg
from constants import (CELLWIDTH, CELLHEIGHT,
                      MARGIN, BORDER, COLOR, TOOLBARHEIGHT)
class GUI():
    """ GUI Class:
        Handles all window elements.
    """
    def __init__(self, board):
        """ Constructor
            Calculate the game window based on board size.
            Defaults: ROWS=10, COLS=10
            PARAMS need to be changed to (self, board). Board object
            will have all the sizes we need.
        """
        #@todo: Generate dynamically based on uiElements
        self.board = board
        self.toolbarOffset = 50
        self.width = ((CELLWIDTH + MARGIN) * board.columns) + (BORDER * 2)
        self.height = ((CELLHEIGHT + MARGIN) * board.rows) + (BORDER * 3) + TOOLBARHEIGHT
        #@todo: Set min/max values based on user input
        if True:
            self.size = self.width, self.height
        elif False:
            pass
        print("Width: ", self.width, "Height: ", self.height)
        self.window = pg.display.set_mode(self.size)

    def drawBoard(self):
        for row in range(self.board.rows):
            for col in range(self.board.columns):
                cellColor = COLOR['WHITE']
                if self.board.grid[row][col].revealed:
                    cellColor = COLOR['BLUE']
                    if self.board.grid[row][col].mine:
                        cellColor = COLOR['RED']
                elif self.board.grid[row][col].flagged:
                    cellColor = COLOR['GREEN']
                cellX = ((MARGIN + CELLWIDTH) * col + MARGIN) + BORDER
                cellY = ((MARGIN + CELLHEIGHT) * row + MARGIN) + (BORDER * 2) + self.toolbarOffset
                cell = pg.Rect([cellX, cellY, CELLWIDTH, CELLHEIGHT])

                pg.draw.rect(self.window, cellColor, cell)

    def uiElement(self, rectX, rectY, rectW, rectH, borderWidth, type='None', label='None'):
        """ Handles creation of all UI elements except board.
        """
        uiElement = pg.Rect([rectX, rectY, rectW, rectH])
        pg.draw.rect(self.window, COLOR['WHITE'], uiElement, borderWidth)

    def mouseClick(self, event):
        """ Handles any mouse event inside the window.
        """
        if True:
            mousePosition = pg.mouse.get_pos()
            column = (mousePosition[0] - BORDER) // (CELLWIDTH + MARGIN)
            row = (mousePosition[1] - (BORDER * 2) - TOOLBARHEIGHT) // (CELLHEIGHT + MARGIN)
            if event.button == 1:
                self.board.revealCell(row, column)
            elif event.button == 3:
                self.board.flagCell(row, column)
