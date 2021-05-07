# Minesweeper

A minsweeper game made with tkinter.

### Utilisation
> python \PATH_TO_FILE\minesweeper.py

Click on the menu to change the size of the grid, view highscores or start a new game.

##### Board sizes:
* 8x8: 10 mines [default]
* 12x12: 25 mines
* 20x20: 60 mines

### Gameplay

[From wikipedia](https://en.wikipedia.org/wiki/Minesweeper_(video_game)#Gameplay):

> In Minesweeper, mines are scattered throughout a board, which is divided into cells. Cells have three states: uncovered, covered and flagged. 
> A covered cell is blank and clickable, while an uncovered cell is exposed. Flagged cells are those marked by the player to indicate a potential mine location.
>
> A player left-clicks a cell to uncover it. If a player uncovers a mined cell, the game ends, as there is only 1 life per game. Otherwise, the uncovered cells displays either 
> a number, indicating the quantity of mines adjacent to it, or a blank tile (or "0"), and all adjacent non-mined cells will automatically be uncovered. 
> Right-clicking on a cell will flag it, causing a flag to appear on it. Flagged cells are still considered covered, and a player can click on them to uncover them.
>
> To win the game, players must uncover all non-mine cells, at which point, the timer is stopped.

### Screenshot
12x12 grid:

![screenshot](https://user-images.githubusercontent.com/69766734/105035992-25a51900-5a5c-11eb-9d68-d5e92bafe170.png)
