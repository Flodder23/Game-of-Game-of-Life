# Installation
## Python
 Python can be installed [here](https://www.python.org/downloads/).
 The game was built and tested in Python 3.6.0.
## PyGame
 PyGame's official installation guide is [here](https://www.pygame.org/wiki/GettingStarted).
 The game was built and tested in PyGame 1.9.3.

# About the Game of Life

The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, alive or dead, or "populated" or "unpopulated".

Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent.

At each step in time, the following transitions occur:
- Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overpopulation.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed - births and deaths occur simultaneously, and the discrete moment at which this happens is sometimes called a tick (in other words, each generation is a pure function of the preceding one). The rules continue to be applied repeatedly to create further generations.

(Thanks, Wikipedia)


# General Help:
To change how the game looks, go into config.py and change the values there.
Each part looks like this:
```
<Name> = <Value>  # <Original value>
# <description of what changing the value will do
```
If the game is behaving oddly please check these values - ones which vary too far from the original may break the game

## General Controls:
 - LEFT CLICK to make a cell "alive".
 - RIGHT CLICK to kill a cell.
 - Press ESC to exit to the main menu

## Simulator Controls:
 - Press SPACE to pause/unpause the game.
 - Press RIGHT arrow to move forward a single turn when paused.
 - Press ENTER to clear the board.
 - Presets (Press the corresponding number to place one):
   - 1 - Glider
   - 2 - Small Exploder
   - 3 - Exploder
   - 4 - Light Weight Space Ship
   - 5 - Tumbler
   - 6 - Gosper Glider Gun
   - 7 - Pentadecathlon
   - 8 - r-Pentomino

<img src="./demo_sim.gif"/>

# 2-Player Game
This is a 2-player game based on the mechanics of the simulator. Players take it in turns to either place one of their own cells or kill any living cell. To win, both players are trying to get as many of their own colour on the board as possible. The winner is the one who either gets the most after a pre-determined amount of turns or who gets a certain amount first. The board has rotational symmetry, with colours on one half the opposite to the cell it corresponds to on the other half, to make it fair.

<img src="https://raw.githubusercontent.com/JosephLGibson/Game-of-Game-of-Life/81fc19b2116d652469b6a3a51778d6f172b8f3b5/demo_game.gif"/>

There are also options to add to the original mechanics, such as cells becoming immune after being alive for a certain amount of turns.
You can also skip turns, saving that turn for the future (eg. if you skip a turn, the next turn you can replace one of you opponent's cells with your own, as that takes 2 turns - one to kill the opponent's cell, the other to place your's.)
## Game Controls:
- Press ESC to deselect a cell when taking a turn.
- Press F to show/hide what the board will look like next turn (the smaller squares)
