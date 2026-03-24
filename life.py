import os
from time import sleep
from random import randint, sample

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
        "2x2": "B36/125",
        "highlife": "B36/S23",
        "day and night": "B3678/S34678",
        "morley": "B368/S245",
        "anneal": "B4678/S35678",

        # rules i found
        "primordial soup": "B059/S6845",
        "static bugs": "B5416/S",
        "degaradation": "B743/S7936", # cool for a world generation
        "static stoic": "B3457/S",
        "hungry": "B863/S30951",
        "tunnel": "B70941/S56734", # try with 1
        "squares": "B321675984/S316250974",
        "towers": "B3/S6479285",
        "negative life": "B84723/S892461370",
    }

    check = ((-1, -1), (0, -1), (1, -1),
             (-1, 0),           (1, 0),
             (-1, 1),  (0, 1),  (1, 1)
    )

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.g = [ [0 for i in range(w)] for j in range(h) ]
        self.char = [" ", "\u2588"]
        self.birth = ""
        self.survival = ""
        self.interactive = True

    def __str__(self):
        return "\n".join("".join(self.char[1] if i == 1 else self.char[0] for i in row) for row in self.g)

    def __repr__(self):
        return str(self)

    def clear(self):
        self.g = [ [0 for i in range(self.w)] for j in range(self.h) ]

    def set_cell(self, x, y, val = True):
        self.g[y][x] = val

    def get_cell(self, x, y):
        return self.g[y][x]

    def get_rule(self):
        return f"B{self.birth}/S{self.survival}"

    def set_rule(self, rule):
        rules = rule.split("/")
        self.birth = rules[0][1:]
        self.survival = rules[1][1:]

    def set_random_rule(self, n_max = 10):
        b = list("23456789")
        d = list("0123456789")
        self.birth = ''.join(sample(b, randint(0, min(8, n_max))))
        self.survival = ''.join(sample(d, randint(0, n_max)))

    def fill_random(self, x, y, dx, dy):
        x = clamp(0, x, self.w)
        y = clamp(0, y, self.h)
        dx = clamp(0, dx, self.w - x)
        dy = clamp(0, dy, self.h - y)

        for i in range(y, y + dy):
            for j in range(x, x + dx):
                self.g[i][j] = randint(0, 1)

    def fill_random_all(self):
        self.fill_random(0, 0, self.w, self.h)

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

    def count_alive(self):
        return sum(sum(row) for row in self.g)

    def run(self, timer = 0.15):
        while True:
            os.system("clear")
            print(self)
            self.evolve()

            if self.interactive:
                stop = input()
                if stop == "q":
                    print(f"B{self.birth}/S{self.survival}")
                    return
            else:
                sleep(timer)
    

if __name__ == "__main__":
    grid = Grid(80, 20)
    #grid.set_rule("B3/S23")
    heuristic = 150
    new_rules = []

    for iter_rule in range(100):
        grid.set_random_rule(4)
        grid.fill_random(0, 0, grid.w, grid.h)

        for i in range(100):
            grid.evolve()

        remaining = grid.count_alive()
        print(remaining)
        print(grid.get_rule())

        if remaining > heuristic - 20 and remaining < heuristic + 20:
            new_rules.append(grid.get_rule())

    print(new_rules)

