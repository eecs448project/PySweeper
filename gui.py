import pygame as pg
from constants import (CELLWIDTH, CELLHEIGHT,
                      MARGIN, BORDER, COLOR, TOOLBARHEIGHT)
""" 
"""
class GUI():
    """ The GUI Class handles all window elements.
        It is divided into a main GUI class which is used to display
        the game board and handle mouse click events,
        a UIElement subclass which handles drawing
        static user interface aspects to the screen,
        an InputBox subclass which generates boxes that the user can type into,
        and an InputButton subclass which generates buttons with specified
        on-click functionality.
    """
    def __init__(self, board):
        """ Constructor for GUI class
            Parameter board is a Board class object. The board object
            will have all the information (rows by columns) we need to generate
            the appropriate window size.
            Postconditions: The window size will be set a game window will be
            displayed on the screen.
        """
        pg.display.set_caption("Minesweeper")
        self.font = pg.font.SysFont(None, 18)
        self.board = board
        self.width = ((CELLWIDTH + MARGIN) * board.columns) + \
                      (BORDER * 2)
        self.height = ((CELLHEIGHT + MARGIN) * board.rows) + \
                      (BORDER * 3) + TOOLBARHEIGHT
        if self.width < 284:
            self.width = 284
        self.window = pg.display.set_mode((self.width, self.height))

    def drawBoard(self):
        """ Draw Board
            Preconditions: Constructor must have been called before calling
            drawBoard so that there is a window to draw it on.
            This method iterates over each cell object on the board's 2D grid
            and displays each cell with colors and images that depend
            on the state of the cell.
            Postconditions: the game board will be drawn on the window in its
            current state.
        """
        for row in range(self.board.rows):
            for col in range(self.board.columns):
                # Calucate the x-offset for each box.
                cellX = ((MARGIN + CELLWIDTH) * col + MARGIN) + BORDER
                # Calculate the y-offset for each box.
                cellY = ((MARGIN + CELLHEIGHT) * row + MARGIN) \
                        + (BORDER * 2) \
                        + TOOLBARHEIGHT # Toolbar offset from the top of window
                cellColor = COLOR['WHITE']
                if self.board.grid[row][col].revealed:
                    cellColor = COLOR['GRAY']
                    if self.board.grid[row][col].mine:
                        cellColor = COLOR['RED']
                elif self.board.grid[row][col].flagged:
                    cellColor = COLOR['GREEN']
                cell = pg.Rect([cellX, cellY, CELLWIDTH, CELLHEIGHT])
                pg.draw.rect(self.window, cellColor, cell)

                #display nearby mines if the cell is revealed and not a mine
                if cellColor == COLOR['GRAY']:
                    nearbyMines = self.board.countNearbyMines(row, col)
                    if (nearbyMines > 0):
                        text = self.font.render(str(nearbyMines), \
                                                True, \
                                                COLOR['BLACK'])
                        # Need offsets in x,y to prevent text being centered
                        #+on 0,0.
                        self.window.blit(text, (cellX + CELLWIDTH // 3, \
                                                cellY + CELLHEIGHT // 4))

                if cellColor == COLOR['RED']:
                    mineImage = pg.image.load("resources/trump.png")
                    self.window.blit(mineImage,(cellX,cellY))
                if cellColor == COLOR['GREEN']:
                    flagImg = pg.image.load("resources/flag.png")
                    self.window.blit(flagImg,(cellX,cellY))

    def mouseClick(self, event):
        """ Mouse Click
        Preconditions: a board object and GUI object have been defined and
        drawBoard has been called before mouseClick is called.
        Parameter event is an instance of a pygame recorded mouse-click event.
        This method handles any mouse click from the user on the drawn board
        object, and interfaces between the front and back-end of the program.
        The starting column and row positions are adjusted for the tool bar
        and margin. The 0,0 coordinate is the first cell generated on the board.
        Postconditions: revealCell() from the board class is called
        when the user clicks the left mouse button. flagCell() from
        the board class is called when the user clicks the right mouse button.
        """
        mousePosition = pg.mouse.get_pos()
        column = (mousePosition[0] - BORDER) // \
                 (CELLWIDTH + MARGIN)
        row = (mousePosition[1] - (BORDER * 2) - TOOLBARHEIGHT) // \
              (CELLHEIGHT + MARGIN)
        if event.button == 1:
            self.board.revealCell(row, column)
        elif event.button == 3:
            self.board.flagCell(row, column)
    

class UIElement():
    """ Handles creation of all user interface elements.
    This includes background, splash screen, and text.
    """
    def __init__(self, x, y, w, h, screen, text=''):
        """ Constructor for UIElement class
        Parameter x  is the horizontal postion of the top left corner
        of the UIElement.
        Parameter y  is the vertical position of the top left corner
        of the UIElement.
        Parameter w is the width of the object in pixels.
        Parameter h is the height of the object in pixels.
        Parameter screen is the window screen to draw the UIElement onto.
        Parameter text is the string of text to be displayed on the UIElement.
        Note: Use an empty string if there is no text to display
        Postconditions: a UIElement object will be initialized with the
        specified values and a pygame rect object will be generated.
        """
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR['WHITE']
        self.screen = screen
        self.text = text
        self.active = False

    def draw(self):
        """ Draw
            Preconditions: The UIElement must have a rect object which
            gets generated by its constructor.
            This method draws the UIElement on top of the window screen.
            Postconditions: The UIElement and text will be drawn
            on the top of the screen over any other existing UIElements.
        """
        pg.draw.rect(self.screen.window, COLOR['BLACK'], self.rect)
        self.txt_surface = self.screen.font.render(self.text, True, self.color)
        self.screen.window.blit(self.txt_surface, (self.rect.x, self.rect.y))

class InputBox(UIElement):
    """ The InputBox class handles the creation of any fields that take input
    from the user.
    These fields will have a box drawn around them.
    Derrives from UIElement class.
    """
    def __init__(self, x, y, w, h, screen, maxValue=0, minValue=0, text=''):
        """ Constructor for the InputBox class
        Parameter x  is the horizontal postion of the top left corner
        of the InputBox.
        Parameter y  is the vertical position of the top left corner
        of the InputBox.
        Parameter w is the width of the object in pixels.
        Parameter h is the height of the object in pixels.
        Parameter screen is the window screen to draw the InputBox onto.
        Parameter maxValue is the maximum value that the inputBox accepts.
        Parameter minValue is the minimum value that the inputBox accepts.
        Parameter text is the string of text to be displayed and
        edited on the InputBox.
        Postconditions: an InputBox object is initialized with
        the specified values.
        """
        super().__init__(x, y, w, h, screen, text)
        self.maxValue = maxValue
        self.minValue = minValue

    def update(self, field, value=0):
        """ Update
            Preconditions: An input box object has been created.
            Parameters field defines what attribute the inputBox is used to
            edit (rows, columns, or mines).
            This is accomplished with the getattr and setattr functions.
            This method updates the inputBox text fields and any game attribute
            associated with that field. The text is displayed while the user
            types in it. When the user confirms their entry (presses enter) then
            the board object will generate a new grid based on the
            user specified values and a new GUI screen window will be drawn.
            Postconditions: If the user inputs a numeric value, this value is
            taken as a string then converted to an integer, then InputBox object
            will accept the user input and update the Board and GUI objects
            accordingly, else the user enters a non-numeric value then the
            inputBox text is reset to its previous value.
        """
        if value.isnumeric():
            if (int(value) > self.maxValue):
                value = self.maxValue
            if (int(value) < self.minValue):
                value = self.minValue
            setattr(self.screen.board, field, int(value))
            self.screen.board.generateGrid()
            self.screen = GUI(self.screen.board)
            self.text = str(getattr(self.screen.board, field))
            self.draw()
        else:
            self.text = str(getattr(self.screen.board, field))
            self.draw()

    def draw(self):
        """ Draw
            Preconditions: The InputBox must have a rect object which
            gets generated by its constructor.
            This method draws the inputBox on top of the window screen.
            Its color is set to white if inactive, otherwise red if active.
            Postconditions: The inputBox will be drawn on the top of the
            screen over any existing UIElements.
        """
        self.txt_surface = self.screen.font.render(self.text, True, COLOR['WHITE'])
        self.screen.window.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        self.color = COLOR['RED'] if self.active else COLOR['WHITE']
        pg.draw.rect(self.screen.window, self.color, self.rect, 1)

class InputButton(UIElement):
    """ The InputButton class is utilized to draw user interface elements
        to the screen that the user can click on, with on-click functionality.
    """
    def __init__(self, x, y, w, h, screen, text):
        """ Constructor for the InputButton class
            Parameter x is the horizontal position of the
            top left corner of the button.
            Parameter y is the vertical position of the
            top left corner of the button.
            Parameter w is the width of the button.
            Parameter h is the height of the button.
            Parameter screen is the window screen to draw the button onto.
            Parameter text is the string of text to be displayed on the button.
            Postconditions: a Button object will be created, but not yet drawn.
        """
        super().__init__(x, y, w, h, screen, text)

    def restart(self, gui, board):
        """ Restart
            Preconditions: The game must already be over and the user clicks on
            the restart button for this method to be called.
            Parameter gui is the overarching GUI object.
            Parameter board is the game board object.
            This method restarts the game by calling generateGrid() to generate
            a new gameBoard, resetting the game state to the initial state,
            and then recalling the GUI constructor to redraw the entire window.
            Postconditions: The game will be reset to an initial state with
            a new GUI window and a newly generated game game board.
        """
        self.active = False
        board.generateGrid()
        gui = GUI(board)

    def draw(self):
        """ Draw
            Preconditions: The InputButton must have a rect object which
            gets generated by its constructor.
            This method draws the inputButton on top of the window screen.
            Postconditions: The inputButton will be drawn on the top of the
            screen over any existing UIElements.
        """
        self.txt_surface = self.screen.font.render(self.text, True, COLOR['WHITE'])
        self.screen.window.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        self.color = COLOR['RED'] if self.active else COLOR['WHITE']
        pg.draw.rect(self.screen.window, self.color, self.rect, 1)

class Sound():
    """The Sound class class is used to add .wav sound files into the 
       project.  These sounds play when the user wins, loses, or
       asks for help.
    """
    def __init__(self):
        """ Constructor for the Sound class
            Postconditions a Sound is initalized and the win, loss,
            and help sound .wav files are loaded in.
        """
        self.winSound = pg.mixer.Sound("resources/goodjob.wav")
        self.lossSound = pg.mixer.Sound("resources/trumplosers.wav")
        self.helpSound = pg.mixer.Sound("resources/support.wav")

    def wins(self):
        """ Handles the win sound when the player wins.
            Precondition the winSound must have loaded in with
            no errors and a Sound() object created
            Postcodition the winSound will play when the user
            wins the game
        """
        self.winSound.play()
    
    def loss(self):
        """ Handles the loss sound when the player loses.
            Precondition the lossSound must have loaded in with
            no errors and a Sound() object created
            Postcodition the lossSound will play when the user
            wins the game
        """
        self.lossSound.play()

    def helps(self):
        """ Handles the help sound when the player asks for help.
            Precondition the helpSound must have loaded in with
            no errors and a Sound() object created
            Postcodition the helpSound will play when the user
            wins the game
        """
        self.helpSound.play()

