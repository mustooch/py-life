import sys
import math
from random import randint
import pygame as pg
from grid import Grid

WIN_W = 800
WIN_H = 800

class Gui:
    def __init__(self, grid):
        self.grid = grid
        self.w = self.grid.w
        self.h = self.grid.h
        self.tile_w = float(WIN_W / self.w)
        self.tile_h = float(WIN_H / self.h)

        pg.init()
        self.clock = pg.time.Clock()
        pg.display.set_caption("Life")
        self.surface = pg.display.set_mode((WIN_W, WIN_H))
        self.loop = True
        self.game_loop = False
        self.fps = 60

        self.set_random_colors()

    def set_random_colors(self):
        self.bg_col = (
            randint(0, 50),
            randint(0, 50),
            randint(0, 50),
        )
        self.tile_col = (
            randint(150, 255),
            randint(150, 255),
            randint(150, 255),
        )

    def draw(self):
        self.surface.fill(self.bg_col)

        for row in range(self.grid.h):
            for col in range(self.grid.w):
                if self.grid.get_cell(row, col) == 1:
                    pg.draw.rect(
                        self.surface,
                        self.tile_col,
                        (row * self.tile_w, col * self.tile_h, self.tile_w, self.tile_h),
                    )
        pg.display.update()

    def handle_key_event(self, key):
        if key == pg.K_ESCAPE:
            self.loop = False

        elif key == pg.K_SPACE:
            self.game_loop = not self.game_loop

        elif key == pg.K_r:
            self.grid.fill_random_all()

        elif key == pg.K_t:
            self.grid.clear()
            self.grid.fill_random(80, 80, 40, 40)

        elif key == pg.K_p:
            self.grid.set_random_rule()
            pg.display.set_caption(self.grid.get_rule())

        elif key == pg.K_0:
            self.grid.clear()

        elif key == pg.K_n:
            self.grid.evolve()

        elif key == pg.K_c:
            self.set_random_colors()

    def handle_mouse(self):
        mouse1, mouse2, mouse3 = pg.mouse.get_pressed()
        mx, my = pg.mouse.get_pos()
        mx = math.floor(mx / self.tile_w)
        my = math.floor(my / self.tile_h)
        
        if mouse1:
            # left click
            self.grid.set_cell(mx, my, True)

        elif mouse3:
            # right click
            self.grid.set_cell(mx, my, False)

    def main(self):
        while self.loop:
            self.draw()
            if self.game_loop: self.grid.evolve()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.loop = False

                elif event.type == pg.KEYDOWN:
                    self.handle_key_event(event.key)

            self.handle_mouse()

            self.clock.tick(self.fps)

        pg.quit()

if __name__ == "__main__":
    # handle program arguments
    rule = "life"
    
    if len(sys.argv) > 1:
        rule = sys.argv[1]

    # setup the grid
    grid = Grid(100, 100)
    grid.set_rule(Grid.rules[rule])
    grid.fill_random_all()

    # setup the gui
    gui = Gui(grid)
    gui.main()

    # program end
    print(grid.get_rule())

