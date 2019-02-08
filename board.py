from cell import Cell
import random
class Board():
    def __init__(self, rows=10, columns=10, mines=25):
        """ Constructor for Board.
            What parameters do we want here?
        """
        self.rows = rows
        self.columns = columns
        self.mines = mines
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

    def draw(self):
        """ Draw the grid on the surface.
        """
        pass
