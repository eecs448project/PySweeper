# [EECS 448] Minesweeper Project 1: PySweeper

## Instructor: Paul Kline

## Team members:

1. Jeff Kissick
2. Thomas Smithey
3. Benjamin Wyss
4. Jon Volden

### TODO:

- [x] Create group repo and add members.
- [x] Create and commit skeleton project.
- [X] Update README.md
- [ ] Assign jobs for team members.
- [x] Start documentation.
- [ ] Add more TODOs.

- [x] Need to add minimum bounds checking to rows and columns input
- [?] Flags disappear when revealing spaces if the flag is not a mine, need to make the flags static             regardless of position on the board when revealing spaces
- [x] If the user flags all mines, they can still unflag a mine and click it to get a game over. We need to disable flagging and revealing once all mines are flagged.
- [x] If the user sets the mines to a really high number, i.e. 99 on the 10x10 board, and then changes the board to a smaller board, i.e. 5x5, all spaces will be mines because the code is trying to place 99 mines on a 5x5 board. Need to make the number of max mines checked if the user edits the board size.
