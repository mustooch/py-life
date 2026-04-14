import sys
import math
from random import randint
import pygame as pg
from grid import Grid

WIN_W = 800
WIN_H = 600

pg.init()
pg.font.init()
font = pg.font.SysFont("Mono", 18)

# Button class
# Used to display buttons on the screen
# Buttons can trigger a function when clicked (the on_click attribute)
class Button:
    def __init__(self, center, color, text, on_click):
        self.color = color
        self.center = center

        # connect callback function
        self.on_click = on_click

        self.update_text(text)

    # Checks if the mouse coordinates lie inside the button's Rect
    # If it is, then the callback function is called
    def check_clicked_fire(self, mx, my):
        if self.rect.collidepoint(mx, my):
            #print("clicked")
            self.on_click()

    def update_text(self, text):
        # generate text surface
        self.text = text
        self.text_surface = font.render(self.text, False, (0, 0, 0))

        # generate button surface
        self.rect = self.text_surface.get_rect(center = self.center)
        self.rect.inflate_ip(10, 2)

        self.button_surface = pg.Surface((self.rect.w, self.rect.h), pg.SRCALPHA)
        self.button_surface.fill(self.color)
    
    # Draw the button and the text to the surface
    def draw(self, surface):
        surface.blit(self.button_surface, (self.rect.x, self.rect.y))
        surface.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 1))

class Gui:
    def __init__(self, grid):
        # Grid setup
        self.grid = grid
        self.update_size()

        # Pygame setup
        pg.display.set_caption("Life")
        self.surface = pg.display.set_mode((WIN_W, WIN_H))
        self.clock = pg.time.Clock()
        self.loop = True
        self.game_loop = False
        self.fps = 60
        self.overlay = False

        self.set_random_colors()

        # Buttons setup
        self.buttons = [
            # Button 0 = rule name
            Button( 
                (700, 420),
                (200, 200, 200, 220),
                f"Rule: {self.grid.rule_name}",
                lambda: True, # do nothing
            ),
            # Button 1 = births
            Button( 
                (700, 442),
                (200, 200, 200, 220),
                f"Birth: {self.grid.birth}",
                lambda: True,
            ),
            # Button 2 = survival
            Button( 
                (700, 464),
                (200, 200, 200, 220),
                f"Survival: {self.grid.survival}",
                lambda: True,
            ),
            # Button 3 = grid size
            Button( 
                (700, 507),
                (200, 200, 200, 220),
                f"Size: {self.grid.w}, {self.grid.h}",
                lambda: True,
            ),
            # Button 4 = FPS
            Button(
                (700, 342),
                (200, 200, 200, 220),
                f"FPS: {self.fps}",
                lambda: True,
            ),

            # The first 5 buttons are just used to display text

            Button(
                (700, 20),
                (200, 200, 200, 220),
                "Clear",
                self.grid.clear,
            ),
            Button(
                (700, 60),
                (200, 200, 200, 220),
                "Random",
                self.grid.fill_random_all,
            ),
            Button(
                (700, 100),
                (200, 200, 200, 220),
                "Play / Pause",
                self.toggle_game_loop,
            ),
            Button(
                (700, 140),
                (200, 200, 200, 220),
                "Next",
                self.grid.evolve,
            ),
            Button(
                (700, 180),
                (200, 200, 200, 220),
                "Rule from dict",
                lambda: self.set_random_rule(True),
            ),
            Button(
                (700, 220),
                (200, 200, 200, 220),
                "Random rule",
                lambda: self.set_random_rule(False),
            ),
            Button(
                (700, 300),
                (200, 200, 200, 220),
                "speed +",
                self.increase_fps,
            ),
            Button(
                (700, 321),
                (200, 200, 200, 220),
                "speed -",
                self.decrease_fps,
            ),
            Button(
                (700, 620),
                (200, 200, 200, 220),
                "Color",
                self.decrease_fps,
            ),
            Button(
                (700, 560),
                (200, 200, 200, 220),
                "Color",
                self.set_random_colors,
            ),
        ]

    def increase_fps(self, n = 5):
        self.fps += n
        self.buttons[4].update_text(f"FPS: {self.fps}")

    def decrease_fps(self, n = 5):
        self.fps = max(5, self.fps - n)
        self.buttons[4].update_text(f"FPS: {self.fps}")

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


    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.surface)

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

    # Randomly change the rule of the grid
    # from_dict defines wether to pick the rule from the Grid.rules dict
    # or to choose a new one
    def set_random_rule(self, from_dict):
        self.grid.set_random_rule(from_dict)
        self.buttons[0].update_text(f"Rule: {self.grid.rule_name}")
        self.buttons[1].update_text(f"B: {self.grid.birth}")
        self.buttons[2].update_text(f"S: {self.grid.survival}")
        pg.display.set_caption(f"{self.grid.rule_name} : {self.grid.get_rule()}")

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
                self.set_random_rule(True)
            else:
                self.set_random_rule(False)

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
            if pg.key.get_pressed()[pg.K_LSHIFT]:
                self.grid.increase_size(10)
            else:
                self.grid.increase_size()
        elif y > 0:
            if pg.key.get_pressed()[pg.K_LSHIFT]:
                self.grid.decrease_size(10)
            else:
                self.grid.decrease_size()

        self.update_size()
        self.buttons[3].update_text(f"Size: {self.grid.w}, {self.grid.h}")

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
    grid = Grid(200, 200)
    grid.set_rule(Grid.rules[rule])
    grid.rule_name = "Life"
    grid.fill_random_all()

    # setup the gui
    gui = Gui(grid)
    gui.main()

    # program end
    print(grid.get_rule())

