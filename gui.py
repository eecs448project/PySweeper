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
        self.font = pg.font.SysFont(None, 18)
        self.board = board
        # Shouldn't Need toolbarOffset since we made a constant TOOLBARHEIGHT
        #self.toolbarOffset = 50
        self.width = ((CELLWIDTH + MARGIN) * board.columns) + (BORDER * 2)
        self.height = ((CELLHEIGHT + MARGIN) * board.rows) + (BORDER * 3) + TOOLBARHEIGHT
        #@todo: Set min/max values based on user input
        if self.width < 240:
            self.width = 240
        #print("Width: ", self.width, "Height: ", self.height)
        self.window = pg.display.set_mode((self.width, self.height))

    def drawBoard(self):
        for row in range(self.board.rows):
            for col in range(self.board.columns):
                cellX = ((MARGIN + CELLWIDTH) * col + MARGIN) + BORDER
                cellY = ((MARGIN + CELLHEIGHT) * row + MARGIN) + (BORDER * 2) + TOOLBARHEIGHT
                cellColor = COLOR['WHITE']
                if self.board.grid[row][col].revealed:
                    cellColor = COLOR['GRAY']
                    if self.board.grid[row][col].mine:
                        cellColor = COLOR['RED']
                        #mineImage = pg.image.load("mine.png")
                        #self.window.blit(mineImage,(((MARGIN + CELLWIDTH) * col + MARGIN) + BORDER, ((MARGIN + CELLHEIGHT) * row + MARGIN) + (BORDER * 2) + TOOLBARHEIGHT))
                elif self.board.grid[row][col].flagged:
                    cellColor = COLOR['GREEN']
                #cellX = ((MARGIN + CELLWIDTH) * col + MARGIN) + BORDER
                #cellY = ((MARGIN + CELLHEIGHT) * row + MARGIN) + (BORDER * 2) + TOOLBARHEIGHT
                cell = pg.Rect([cellX, cellY, CELLWIDTH, CELLHEIGHT])
                pg.draw.rect(self.window, cellColor, cell)

                #display nearby mines if the cell is revealed and not a mine
                if cellColor == COLOR['GRAY']:
                    nearbyMines = self.board.countNearbyMines(row, col)
                    if (nearbyMines > 0):
                        text = self.font.render(str(nearbyMines), True, COLOR['BLACK'])
                        self.window.blit(text, (cellX + CELLWIDTH // 3, cellY + CELLHEIGHT // 4))
                
                if cellColor == COLOR['RED']:
                    trumpImg = pg.image.load("trump.png")
                    self.window.blit(trumpImg,(cellX,cellY))
                    #mineImage = pg.image.load("mine.png")
                    #self.window.blit(mineImage,(cellX,cellY))
                if cellColor == COLOR['GREEN']:
                    flagImg = pg.image.load("flag.png")
                    self.window.blit(flagImg,(cellX,cellY))

    def uiElement(self, rectX, rectY, rectW, rectH, borderWidth, type="None", label="None"):
        """ Handles creation of all UI elements except board.
        """
        if type == "None" or type == "input":
            uiElement = pg.Rect([rectX, rectY, rectW, rectH])
            pg.draw.rect(self.window, COLOR['WHITE'], uiElement, borderWidth)
        elif type == "text" or type == "input":
            text = self.font.render(label, True, COLOR['WHITE'])
            self.window.blit(text, (rectX, rectY))

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
