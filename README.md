# Py-Life

This is a quick implementation of Conway's Game of Life.

## Program structure

There are three classes:

- Grid (grid.py) implements a classic GOL grid with modifiable rules.
- Gui (gui.py) implements a graphical user interface for the Grid class.
- Button (gui.py) implements a simple button that can trigger functions when clicked

## Requirements

The user interface uses the library [Pygame](https://www.pygame.org/news)

You can install it by running `pip install pygame` in the terminal.

Or `apt install python3-pygame` if using Linux.

## Running the program

### Text-based user interface:

In the termianl, run `python3 grid.py`.

#### Commands for the TUI:

- q : End simulation and print the rule

### Graphical user interface:

In the terminal, run `python3 gui.py [rule]`.

With [rule] being an optional rule name that is defined in the "rules" dictionary of the Grid class.

#### Commands for the GUI:

Keyboard:

| Key     | Description
| ------  | -----------
| Escape  | close the program
| Space   | toggle the simulation on / off
| n       | perform 1 step in the simulation while paused
| r       | randomly fill the entire grid
| t       | randomly fill some cells in the middle of the grid
| p       | change the rule randomly
| shift+P | pick a random rule from the dictionary
| c       | change colors randomly
| 0       | clear the grid

Mouse:

| Button | Action
| ------ | ------
| Left   | set cell alive
| Right  | set cell dead
| Wheel  | increase/decrease grid size

