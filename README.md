# Py-Life

This is a quick implementation of Conway's Game of Life.

## Program structure

There are two classes:

- Grid (grid.py) implements a classic GOL grid with modifiable rules
- Gui (gui.py) implements a graphical user interface for the Grid class

## Requirements

The user interface uses the library [Pygame](https://www.pygame.org/news)

You can install it by running `pip install pygame` in the terminal

Or `apt install python3-pygame` if using Linux

## Running the program

Text-based user interface:

In the termianl, run `python3 grid.py`

Graphical user interface:

In the terminal, run `python3 gui.py [rule]`

With [rule] being an optional rule name that is defined in the dictionary in the Grid class

### Commands

Commands for the GUI:

Keyboard:
- Escape    close the program
- Space     toggle the simulation on / off
- n         perform 1 step in the simulation while paused
- r         randomly fill the entire grid
- t         randomly fill some cells in the middle of the grid
- p         change the rule randomly
- c         change colors randomly
- 0         clear the grid
- g         toggle the grid overlay

Mouse:
- Left      make cell alive
- Right     make cell dead

Commands for the TUI:

- q     End simulation and print the rule

