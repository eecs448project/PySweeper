# Globals: Colors, starting window attributes
DEBUG = True

COLOR = dict(
    WHITE = (255, 255, 255),
    RED = (255, 0, 0),
    BLUE = (0, 0, 255),
    GREEN = (0, 255, 0),
    BLACK =  (0, 0, 0)
)

# Sane board size defaults
#@todo: Decide if these should be initialized in a Cell()
#+prior to generating GUI window. These are needed for GUI
#+constructor.
CELLWIDTH = 20
CELLHEIGHT = 20
MARGIN = 2
BORDER = 20
STARTINGMINES = 25
TOOLBARHEIGHT = 50