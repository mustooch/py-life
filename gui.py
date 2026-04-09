import sys
import math
from random import randint
import pygame as pg
from grid import Grid

WIN_W = 800
WIN_H = 600

pg.init()
pg.font.init()

class Button:
    font = pg.font.SysFont("Monospace", 16)

    def __init__(self, rect, color, text, on_click):
        self.rect = rect
        self.color = color
        self.text = text
        self.text_surface = self.font.render(self.text, False, (0, 0, 0))
        self.on_click = on_click

    def check_clicked_fire(self, mx, my):
        if self.rect.collidepoint(mx, my):
            print("clicked")
            self.on_click()
    
    def draw(self, surface):
        pg.draw.rect(
            surface,
            self.color,
            self.rect
        )

        surface.blit(self.text_surface, (self.rect.x, self.rect.y))

class Gui:
    def __init__(self, grid):
        self.grid = grid
        self.update_size()

        pg.display.set_caption("Life")
        self.surface = pg.display.set_mode((WIN_W, WIN_H))
        self.clock = pg.time.Clock()
        self.loop = True
        self.game_loop = False
        self.fps = 30
        self.overlay = False

        self.set_random_colors()

        self.buttons = [
            Button(
                pg.Rect(640, 20, 100, 20),
                (200, 200, 200),
                "clear",
                self.grid.clear
            ),
            Button(
                pg.Rect(640, 60, 100, 20),
                (200, 200, 200),
                "random",
                self.grid.fill_random_all
            ),
            Button(
                pg.Rect(640, 100, 100, 20),
                (200, 200, 200),
                "play/pause",
                self.toggle_game_loop
            )
        ]
    
    def toggle_game_loop(self):
        self.game_loop = not self.game_loop

    def update_size(self):
        self.tile_w = float(WIN_W / self.grid.w)
        self.tile_h = float(WIN_H / self.grid.h)

        # take the smaller to make a square that fits the screen
        smaller = min(self.tile_w, self.tile_h)
        self.tile_w = smaller
        self.tile_h = smaller

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

    def draw_overlay(self):
        #line_color = (120, 120, 120)
        line_color = self.bg_col

        for x in range(0, self.grid.w):
            pg.draw.line(
                self.surface,
                line_color,
                (x * self.tile_w, 0), (x * self.tile_w, WIN_H),
            )

        for y in range(0, self.grid.h):
            pg.draw.line(
                self.surface,
                line_color,
                (0, y * self.tile_h), (WIN_W, y * self.tile_h),
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
        if self.overlay:
            self.draw_overlay()
        
        self.draw_buttons()

        pg.draw.line(
            self.surface,
            (150, 150, 150),
            (self.grid.w * self.tile_w, 0), (self.grid.w * self.tile_w, WIN_H),
            4
        )

        pg.display.update()

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.surface)

    def update_buttons(self, mx, my):
        for button in self.buttons:
            button.check_clicked_fire(mx, my)

    def handle_mouse_button_down(self, pos, button):
        mx, my = pos

        # on left click
        if button == 1:
            # check all buttons
            for button in self.buttons:
                button.check_clicked_fire(mx, my)


    def handle_key_down(self, key):
        if key == pg.K_ESCAPE:
            self.loop = False

        elif key == pg.K_SPACE:
            self.game_loop = not self.game_loop

        elif key == pg.K_r:
            self.grid.fill_random_all()

        elif key == pg.K_t:
            self.grid.clear()
            size_x = int(self.grid.w / 4)
            size_y = int(self.grid.h / 4)
            start_x = int(self.grid.w / 2 - size_x / 2)
            start_y = int(self.grid.h / 2 - size_y / 2)
            self.grid.fill_random(start_x, start_y, size_x, size_y)

        elif key == pg.K_p:
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                rule_name = self.grid.get_random_rule_name()
                self.grid.set_rule(grid.rules[rule_name])
                pg.display.set_caption(rule_name)
            else:
                self.grid.set_random_rule()
                pg.display.set_caption(self.grid.get_rule())

        elif key == pg.K_0:
            self.grid.clear()

        elif key == pg.K_n:
            self.grid.evolve()

        elif key == pg.K_c:
            self.set_random_colors()

        elif key == pg.K_g:
            self.overlay = not self.overlay

    def handle_mouse_pressed(self):
        mouse1, mouse2, mouse3 = pg.mouse.get_pressed()
        mx, my = pg.mouse.get_pos()
        gx = math.floor(mx / self.tile_w)
        gy = math.floor(my / self.tile_h)
        
        # left click
        if mouse1:

            # clicked inside grid
            if gx < self.grid.w: 
                self.grid.set_cell(gx, gy, True)

        # right click
        elif mouse3:

            # clicked inside grid
            if gx < self.grid.w: 
                self.grid.set_cell(gx, gy, False)

    def handle_mouse_wheel(self, y):
        if y < 0:
            self.grid.increase_size()
        elif y > 0:
            self.grid.decrease_size()

        self.update_size()

    def main(self):
        while self.loop:
            self.draw()
            if self.game_loop: self.grid.evolve()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.loop = False

                elif event.type == pg.KEYDOWN:
                    self.handle_key_down(event.key)

                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event.pos, event.button)

                elif event.type == pg.MOUSEWHEEL:
                    self.handle_mouse_wheel(event.y)

            self.handle_mouse_pressed()

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

