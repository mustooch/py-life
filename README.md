# Py-Life

This is a quick implementation of Conway's Game of Life.

## Program structure

There are two classes:

- Life (life.py) implements a classic GOL with modifiable rules
- Gridui (gridui.py) implements a graphical user interface for the Life class

## Requirements

The user interface uses the library [Pygame](https://www.pygame.org/news)

You can install by running `pip install pygame` in the terminal

## Running the program

Text-based user interface:

In the termianl, run `python3 life.py`

Graphical user interface:

In the terminal, run `python3 gridui.py`

### Commands

Commands for the GUI:

- Escape    close the program
- Space     toggle the simulation on / off
- N         perform 1 step in the simulation while paused
- R         fill the grid randomly
- P         change the rule randomly

Commands for the TUI:

- q     End simulation and print the rule

