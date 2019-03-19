class Cell():
    """ The Cell class will be used to create the building blocks
        of the game board.
        It contains all information needed by a higher up board class
        in order to implement the minesweeper game
    """
    def __init__(self):
        """ Constructor for Cell class
            Takes no parameters
            sets each variable of the cell class to a default value.
            Cells are constructed as nonrevealed, nonflagged, nonmines.
        """
        self.mine = False
        self.revealed = False
        self.preRevealed = False
        self.flagged = False
        pass
