# [EECS 448] Minesweeper Project 1: PySweeper

## Instructor: Paul Kline

## Team members:

1. Jeff Kissick
2. Thomas Smithey
3. Benjamin Wyss
4. Jon Volden

### Requirements:

1. OS: Windows 10, OSX, Linux  
2. [Python 3.7.2](https://www.python.org/downloads/) or greater.

### Installation:

1. Git clone or download zip from [PySweeper](https://github.com/pysweeper/PySweeper.git).
2. Extract and/or cd into the pysweeper folder.
2. From the pysweeper folder run:  
    `$ pip install -r requirements.txt`
3. To run the game:  
    `$ python pysweeper.py`

### Resources/Citations:

1. Input box code based on [this SO article](https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame/46390412)  
2. General game logic influenced by [Daniel Shiffman](https://www.youtube.com/watch?v=LFU5ZlrR21E&vl=en)

### TODO:

- [x] Create group repo and add members.
- [x] Create and commit skeleton project.
- [X] Update README.md
- [X] Assign jobs for team members.
- [x] Start documentation.
- [x] Need to add minimum bounds checking to rows and columns input
- [x] If the user flags all mines, they can still unflag a mine and click it to get a game over. We need to disable flagging and revealing once all mines are flagged.
- [x] If the user sets the mines to a really high number, i.e. 99 on the 10x10 board, and then changes the board to a smaller board, i.e. 5x5, all spaces will be mines because the code is trying to place 99 mines on a 5x5 board. Need to make the number of max mines checked if the user edits the board size.
- [X] If the user inputs a non integer value into the text box field, then a valueerror: invalid literal is thrown. This needs fixed before the deadline.
- [X] Finish the GAME OVER screen with win or loss screen and an option to play again (In progress, Thomas)
- [ ] Add comments to code (In progress, Jeff but anyone can add on/edit)
- [X] Pydoc
- [X] Retrospective write up (In progess, Jeff)
- [ ] Deployment instructions
- [ ] Merge the sound branch or add that into the write up in things that didn't make the final product


Ignore but document
- [ ] Flags disappear when revealing spaces if the flag is not a mine, need to make the flags static             regardless of position on the board when revealing spaces 
- [ ] Make revealing all squares not mines a win, don't have to flag them

To Add as expansion
- [ ] Generate mines after first click
- [ ] middle click to show which are being clicked
- [ ] middle click to reveal if we say its not a mine for sure
- [ ] prevent user from clicking a flagged cell
- [ ] center toolbar or other gui objects using the colliderect() function