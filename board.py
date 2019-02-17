from cell import Cell
import random
class Board():
    """ The Board class is in charge of managing a 2D grid of Cell objects
        to implement the main functionality of the minesweeper game.
        This class serves as the controller for the back-end of the game.
    """
    def __init__(self, rows=12, columns=12, mines=10):
        """ Constructor for Board class.
            Parameter rows determines the initial number of rows on the board.
            Parameter columns determines the initial number of columns on the board.
            Parameter mines determines the initial number of mines on the board.
            This constructor also sets member variables used throughout
            the Board class' methods to default values, such as setting
            flagsPlaced to 0, and setting the gameOver/wonGame variables used to track
            the end of the game both to False.
            This constructor finishes by calling generateGrid() to initialize the
            2D array of Cell objects which the game is based on.
            Postconditions: Every board class member variable will be initialized to a default value.
        """
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.flagsPlaced = 0
        self.gameOver = False
        self.wonGame = False
        self.generateGrid()

    def generateGrid(self):
        """ Generate Grid
            Preconditions: rows, columns, and mines must be set to positive integer values.
            Gets called by Board constructor
            This method generates a 2D array of Cell objects to be stored in grid[][].
            This method is also used to reset the game, and so recalling this method
            Postconditions: generates a new grid and sets the end game variables both to false again.
        """
        #Generate a grid of rows by columns cells.
        self.grid = []
        for row in range(self.rows):
            self.grid.append([])
            for col in range(self.columns):
                defaultCell = Cell()
                self.grid[row].append(defaultCell)

        #Populate grid with mines
        locs = [(row, col) for row in range(self.rows) for col in range(self.columns)]
        random.shuffle(locs)
        for row, col in locs[:self.mines]:
            self.grid[row][col].mine = True
            #test print
            #print("Mine added: ", row, col)

        self.flagsPlaced = 0
        self.gameOver = False
        self.wonGame = False

    def revealCell(self, row, col):
        """ Reveal Cell
            Preconditions: generateGrid() must have been called prior to calling this method.
            Parameter row is the row of the cell to be revealed.
            Parameter col is column of the cell to be revealed.
            Bounds-checking issues are handled within this method,
            so this method is safe to call with bad input.
            Postconditions: Reveals the seleted cell and
            recursively reaveals nearby cells if no mines are nearby the selected cell.
            If a mine is revealed, this method calls gameOverLoss(), ending the game.
        """
        if (not self.gameOver):
            if(row >= 0 and row < self.rows and col >= 0 and col < self.columns):
                if(not self.grid[row][col].revealed):
                    self.grid[row][col].revealed = True

                    if (self.grid[row][col].flagged):
                        self.grid[row][col].flagged = False
                        self.flagsPlaced -= 1

                    if(self.grid[row][col].mine):
                        #end game here
                        self.gameOverLoss()
                    elif(self.countNearbyMines(row, col) > 0):
                        #Cell is already revealed, recursion terminates here
                        pass
                    elif(self.countNearbyMines(row, col) == 0):
                        for x in range(-1, 2):
                            for y in range(-1, 2):
                                    self.revealCell(row + x, col + y)

    def countNearbyMines(self, row, col):
        """ Count Nearby Mines
            Preconditions: generateGrid() must have been called prior to calling this method.
            Parameter row is the row of the cell to count its adjacent mines.
            Parameter col is the column of the cell to count its adjacent mines.
            Counts how many mines are adjacent to the specified cell.
            Bounds-checking issues are handles within this method,
            so this method is safe to call with bad input.
            Postconditions: Returns the number of mines adjacent to the specified cell counting all 8 directions.
        """
        nearbyMines = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (row + x >= 0 and row + x < self.rows and col + y >= 0 and col + y < self.columns):
                    if (self.grid[row + x][col + y].mine):
                        nearbyMines += 1
        return nearbyMines

    def flagCell(self, row, col):
        """ Flag Cell
            Preconditions: generateGrid() must have been called prior to calling this method.
            Parameter row is the row of the cell to flag.
            Parameter col is the column of the cell to flag.
            Bounds-checking issues are handles within this method,
            so this method is safe to call with bad input.
            Postconditions: Flags the selected Cell as a potential mine.
            Checks if all mines have been flagged, and if so calls gameOverWin(), ending the game.
        """
        if (not self.gameOver):
            if(row >= 0 and row < self.rows and col >= 0 and col < self.columns):
                if(not self.grid[row][col].revealed):
                    if (self.grid[row][col].flagged):
                        self.grid[row][col].flagged = False
                        self.flagsPlaced -= 1
                    elif (not self.grid[row][col].flagged and self.flagsPlaced < self.mines):
                        self.grid[row][col].flagged = True
                        self.flagsPlaced += 1
                        #check if the player has won the game
                        if (self.flagsPlaced == self.mines):
                            #this is a local variable, not the member variable of the same name
                            wonGame = True
                            for row in range(self.rows):
                                for col in range(self.columns):
                                    if(self.grid[row][col].flagged != self.grid[row][col].mine):
                                        wonGame = False
                            if (wonGame):
                                self.gameOverWin()


    def gameOverLoss(self):
        """ Game Over Loss
            Preconditions: revealCell() has to be called on a mine for this method to be called.
            Postconditions: Reveals all spaces and mines, and then sets gameOver to true.
            This then causes a game over message to be displayed by the GUI class.
        """
        self.gameOver = True
        for row in range(self.rows):
            for col in range(self.columns):
                self.grid[row][col].revealed = True
                self.grid[row][col].flagged = False
                self.flagsPlaced = 0

    def gameOverWin(self):
        """ Game Over Win
            Preconditions: flagCell() has to be called on all mines for this method to be called.
            Postconditions: Reveals all nonmine cells and sets both gameOver and wonGame to true.
            This then causes a win message to be displayed by the GUI class.
        """
        self.gameOver = True
        self.wonGame = True
        for row in range(self.rows):
            for col in range(self.columns):
                if (not self.grid[row][col].flagged):
                    self.grid[row][col].revealed = True
