import os
from time import sleep
import random

def clamp(a, b, c):
    return min(max(a, b), c)

class Grid:
    rules = {
        # rules taken from https://en.wikipedia.org/wiki/Life-like_cellular_automaton#A_selection_of_Life-like_rules
        "replicator": "B1357/S1357",
        "seeds": "B2/S",
        "no death": "B3/S0123456789",
        "life": "B3/S23",
        "34 life": "B34/S34",
        "diamoeba": "B35678/S5678",
        "2x2": "B36/S125",
        "highlife": "B36/S23",
        "day night": "B3678/S34678",
        "morley": "B368/S245",
        "anneal": "B4678/S35678",

        # rules i found
        "soup": "B059/S4568",
        "bugs": "B1456/S",
        "degrade": "B347/S3679", # cool for a world generation
        "map": "B68/S13456789", # also cool for map gen
        "static": "B3457/S",
        "hungry": "B368/S01359",
        "tunnel": "B1479/S34567", # try with 1
        "squares": "B123456789/S012345679",
        "towers": "B3/S2456789",
        "negative": "B23478/S012346789", # life but 1 and 0 are sawpped
        "chaotic": "B3569/S23",
        "cheese": "B23679/S01245679",
        "ripples": "B3457/S8",
        "painting": "B2/S01245679",
        "painting 2": "B28/S124679",
    }

    def get_random_rule_name():
        return random.choice(list(Grid.rules.keys()))

    def __init__(self, w, h):
        # Width and height of the grid
        self.w = w
        self.h = h

        # The grid
        self.g = [[0 for i in range(w)] for j in range(h)]

        # The rule
        self.birth = ""
        self.survival = ""
        self.rule_name = ""

        # Used for displaying to the temrinal
        self.char = [" ", "\u2588"]

    # Get a string representation of the grid
    def __str__(self):
        return "\n".join("".join(self.char[1] if i == 1 else self.char[0] for i in row) for row in self.g)

    def __repr__(self):
        return str(self)

    # Set all the cells to dead
    def clear(self):
        self.g = [ [0 for i in range(self.w)] for j in range(self.h) ]

    # Return the value of the cell at (x, y)
    def get_cell(self, x, y):
        return self.g[y][x]

    # Set the value of the cell at (x, y)
    def set_cell(self, x, y, val = True):
        self.g[y][x] = val

    # Toggle the value of the cell at (x, y)
    def toggle_cell(self, x, y):
        self.g[y][x] = not self.g[y][x]

    # Return the rule of the grid in the form B/S
    def get_rule(self):
        return f"B{self.birth}/S{self.survival}"

    # Set the rule of the grid in the form B/S
    def set_rule(self, rule):
        rules = rule.split("/")
        self.birth = rules[0][1:]
        self.survival = rules[1][1:]

    # Set a random rule
    # If from_dict is true, then choose from the Grid.rules
    # Else choose a new random rule
    def set_random_rule(self, from_dict):
        if from_dict:
            self.rule_name = Grid.get_random_rule_name()
            self.set_rule(Grid.rules[self.rule_name])
        else:
            b = list("23456789")
            s = list("123456789")
            self.birth = ''.join(sorted(random.sample(b, random.randint(0, 8))))
            self.survival = ''.join(sorted(random.sample(s, random.randint(0, 9))))
            self.rule_name = "random"

    # Fill the grid randomly from (x, y) to (x + dx, y + dy)
    def fill_random(self, x, y, dx, dy):
        x = clamp(0, x, self.w)
        y = clamp(0, y, self.h)
        dx = clamp(0, dx, self.w - x)
        dy = clamp(0, dy, self.h - y)

        for i in range(y, y + dy):
            for j in range(x, x + dx):
                self.g[i][j] = random.randint(0, 1)

    # Fill all the grid randomly
    def fill_random_all(self):
        self.fill_random(0, 0, self.w, self.h)

    # Add one row below and one column to the right
    def increase_size(self, n = 1):
        for i in range(n):
            # add row below
            self.g.append([0 for i in range(self.w)])
            self.h += 1

            # add column to the right
            for i in range(self.h):
                self.g[i].append(0)
            self.w += 1

    # Remove one row below and one column to the right
    def decrease_size(self, n = 1):
        for i in range(n):
            if self.w < 10 or self.h < 10:
                return

            # remove row below
            self.g.pop()
            self.h -= 1

            # remove column to the right
            for i in range(self.h):
                self.g[i].pop()
            self.w -= 1

    # Count the number of cells alive in all of the grid
    def count_alive(self):
        return sum(sum(row) for row in self.g)

    check = ((-1, -1), (0, -1), (1, -1),
             (-1, 0),           (1, 0),
             (-1, 1),  (0, 1),  (1, 1)
    )

    def evolve(self):
        # Create a new empty grid
        new_g = [ [0 for i in range(self.w)] for j in range(self.h) ]

        # Loop over all cells
        for i in range(self.h):
            for j in range(self.w):
                neighbours = 0
                new_c = 0  # the new cell is 0 by default

                for dj, di in self.check:
                    # The grid has closed edges
                    #if i + di >= 0 and i + di < self.h \
                    #and j + dj >= 0 and j + dj < self.w:
                    #    neighbours += self.g[ii][jj]

                    # The grid edges loop and simulate a torus
                    ii = (i + di) % self.h
                    jj = (j + dj) % self.w

                    neighbours += self.g[ii][jj]

                if self.g[i][j] == 1:
                    if str(neighbours) in self.survival:
                        new_c = 1
                if self.g[i][j] == 0:
                    if str(neighbours) in self.birth:
                        new_c = 1

                new_g[i][j] = new_c

        self.g = new_g

if __name__ == "__main__":
    grid = Grid(60, 20)

    grid.set_rule(Grid.rules["life"])
    grid.fill_random(10, 10, 60, 5)

    while True:
        os.system("clear")
        print(grid)
        grid.evolve()

        stop = input()
        if stop == "q":
            print(grid.get_rule())
            break
    
