import sys
from random import randint
import pygame as pg
import life

WIN_W = 800
WIN_H = 800

class Gridui:
    def __init__(self, grid):
        pg.init()
        self.clock = pg.time.Clock()
        pg.display.set_caption("Life")
        self.surface = pg.display.set_mode((WIN_W, WIN_H))
        self.loop = True
        self.game_loop = False

        self.grid = grid
        self.w = self.grid.w
        self.h = self.grid.h
        self.tile_w = float(WIN_W / self.w)
        self.tile_h = float(WIN_H / self.h)

    def draw(self):
        self.surface.fill((0, 0, 0))

        for row in range(self.grid.h):
            for col in range(self.grid.w):
                if self.grid.get_cell(row, col) == 1:
                    pg.draw.rect(
                        self.surface,
                        (255, 0, 0),
                        (row * self.tile_w, col * self.tile_h, self.tile_w, self.tile_h),
                    )
        pg.display.update()

    def main(self):
        while self.loop:
            self.draw()
            if self.game_loop: self.grid.evolve()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.loop = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.loop = False

                    elif event.key == pg.K_SPACE:
                        self.game_loop = not self.game_loop

                    elif event.key == pg.K_r:
                        self.grid.fill_random_all()

                    elif event.key == pg.K_t:
                        self.grid.clear()
                        self.grid.fill_random(80, 80, 40, 40)

                    elif event.key == pg.K_1:
                        self.grid.clear()
                        self.grid.set_cell(100, 100)

                    elif event.key == pg.K_2:
                        self.grid.clear()
                        self.grid.set_cell(100, 100)
                        self.grid.set_cell(100, 101)

                    elif event.key == pg.K_p:
                        grid.set_random_rule()

                    elif event.key == pg.K_n:
                        self.grid.evolve()

            self.clock.tick(60)

        pg.quit()


if __name__ == "__main__":
    grid = life.Grid(200, 200)
    grid.fill_random(0, 0, 200, 200)
    #grid.set_rule(life.Grid.rules[sys.argv[1]])
    #grid.set_random_rule(4)
    #grid.set_rule("B059/S6845")
    grid.set_rule("B84723/S892461370")
    gui = Gridui(grid)

    gui.main()
    print(grid.get_rule())

