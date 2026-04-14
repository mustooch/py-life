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
        "life without death": "B3/S0123456789",
        "life": "B3/S23",
        "34 life": "B34/S34",
        "diamoeba": "B35678/S5678",
        "2x2": "B36/S125",
        "highlife": "B36/S23",
        "day and night": "B3678/S34678",
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
        "negative life": "B23478/S012346789", # life but 1 and 0 are sawpped
        "chaotic life": "B3569/S23",
        "cheese": "B23679/S01245679",
        "ripples": "B3457/S8",
        "stacks": "B2/S01245679",
    }

    def get_random_rule_name(self):
        return random.choice(list(self.rules.keys()))

    check = ((-1, -1), (0, -1), (1, -1),
             (-1, 0),           (1, 0),
             (-1, 1),  (0, 1),  (1, 1)
    )

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.g = [[0 for i in range(w)] for j in range(h)]
        self.char = [" ", "\u2588"]
        self.birth = ""
        self.survival = ""

    def __str__(self):
        return "\n".join("".join(self.char[1] if i == 1 else self.char[0] for i in row) for row in self.g)

    def __repr__(self):
        return str(self)

    def clear(self):
        self.g = [ [0 for i in range(self.w)] for j in range(self.h) ]

    def get_cell(self, x, y):
        return self.g[y][x]

    def set_cell(self, x, y, val = True):
        self.g[y][x] = val

    def toggle_cell(self, x, y):
        self.g[y][x] = not self.g[y][x]

    def get_rule(self):
        return f"B{self.birth}/S{self.survival}"

    def set_rule(self, rule):
        rules = rule.split("/")
        self.birth = rules[0][1:]
        self.survival = rules[1][1:]

    def set_random_rule(self, n_max = 10):
        b = list("23456789")
        d = list("0123456789")
        self.birth = ''.join(sorted(random.sample(b, random.randint(0, min(8, n_max)))))
        self.survival = ''.join(sorted(random.sample(d, random.randint(0, n_max))))

    def fill_random(self, x, y, dx, dy):
        x = clamp(0, x, self.w)
        y = clamp(0, y, self.h)
        dx = clamp(0, dx, self.w - x)
        dy = clamp(0, dy, self.h - y)

        for i in range(y, y + dy):
            for j in range(x, x + dx):
                self.g[i][j] = random.randint(0, 1)

    def fill_random_all(self):
        self.fill_random(0, 0, self.w, self.h)

    def increase_size(self, n = 1):
        for i in range(n):
            # add row below
            self.g.append([0 for i in range(self.w)])
            self.h += 1

            # add column to the right
            for i in range(self.h):
                self.g[i].append(0)
            self.w += 1

    def decrease_size(self, n = 1):
        if self.w < 10 or self.h < 10:
            return

        for i in range(n):
            # remove row below
            self.g.pop()
            self.h -= 1

            # remove column to the right
            for i in range(self.h):
                self.g[i].pop()
            self.w -= 1

    def count_alive(self):
        return sum(sum(row) for row in self.g)

    def evolve(self):
        new_g = [ [0 for i in range(self.w)] for j in range(self.h) ]

        for i in range(self.h):
            for j in range(self.w):
                neighbours = 0
                new_c = 0

                for dj, di in self.check:
                    #if i + di >= 0 and i + di < self.h \
                    #and j + dj >= 0 and j + dj < self.w:
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
    
