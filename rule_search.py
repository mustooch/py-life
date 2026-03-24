import life

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

