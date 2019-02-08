from cell import Cell
import random
class Board():
    def __init__(self, rows=10, columns=10, mines=10):
        """ Constructor for Board.
            What parameters do we want here?
        """
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.flagsPlaced = 0
        self.generateGrid()
        pass

    def generateGrid(self):
        """ Generate grid
            Should we call this in __init__?
        """
        #Generate a grid of row x columns cells.
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
            print("Mine added: ", row, col)
        pass
    def revealCell(self, row, col):
        """Reveals the seleted cell and recursively reaveals nearby cells if no mines are nearby the selected cell
        """
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

        pass

    def countNearbyMines(self, row, col):
        """Counts how many mines are adjacent to the specified cell
        """
        nearbyMines = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (row + x >= 0 and row + x < self.rows and col + y >= 0 and col + y < self.columns):
                    if (self.grid[row + x][col + y].mine):
                        nearbyMines += 1
        return nearbyMines

    def flagCell(self, row, col):
        """Flags the selected Cell as a potential mines
        """
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
                        wonGame = True
                        for row in range(self.rows):
                            for col in range(self.columns):
                                if(self.grid[row][col].flagged != self.grid[row][col].mine):
                                    wonGame = False
                        if (wonGame):
                            self.gameOverWin()

        pass

    def gameOverLoss(self):
        """Reveals all mines and displays a game over message
        """
        for row in range(self.rows):
            for col in range(self.columns):
                self.grid[row][col].revealed = True
                self.grid[row][col].flagged = False
                self.flagsPlaced = 0
        pass

    def gameOverWin(self):
        """Reveals all nonmine cells and displays a win message
        """
        for row in range(self.rows):
            for col in range(self.columns):
                if (not self.grid[row][col].flagged):
                    self.grid[row][col].revealed = True
        pass
