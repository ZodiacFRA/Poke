import time

import pygame
from pygame.locals import *

from Position import Position
from utils import *


class App(object):
    def __init__(self):
        ####
        self.visible_tiles = Position(21, 21)
        self.tile_size = 32
        self.window_size = Position(
            self.tile_size * self.visible_tiles.y,
            self.tile_size * self.visible_tiles.x
        )
        ####
        pygame.init()
        pygame.display.set_caption('Level editor')
        self.d = pygame.display.set_mode((self.window_size.x, self.window_size.y))
        ####
        self.sprites = load_sprites("../../client/sprites/")
        self.background_image = load_sprite(
            "../ressources/wholemap.png",
            resize_factor=2
        )
        reference_map_size = self.background_image.get_size()
        self.map_size = Position(reference_map_size[1], reference_map_size[0]) // self.tile_size
        self.top_layer = []
        self.bottom_layer = []
        for y in range(self.map_size.y):
            tmp_top_line = []
            tmp_bottom_line = []
            for x in range(self.map_size.x):
                tmp_top_line.append(None)
                tmp_bottom_line.append(None)
            self.top_layer.append(tmp_top_line)
            self.bottom_layer.append(tmp_bottom_line)
        ####
        self.moving_zone_pixels = self.window_size // 10
        self.top_left_tile = Position(0, 0)
        self.mouse_map_position = Position(-1, -1)
        ####
        self.delta_time = 1 / 15
        self.start_time = time.time()
        ####
        self.is_top_layer = True
        self.selected_sprite_idx = 0

    def launch(self):
        while self.handle_loop():
            self.display_background_image()
            self.drawGrid()
            self.handle_input()
            self.draw_map()

    def handle_loop(self):
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                print("[ ] - App: Exiting")
                pygame.quit()
                return 0
        # sleep handling
        to_sleep = self.delta_time - (time.time() - self.start_time)
        if to_sleep <= 0:
            print(f"[-] - App: Lagging behind: {to_sleep}")
        else:
            time.sleep(to_sleep)
        self.start_time = time.time()
        self.d.fill("#ff0000")
        return 1

    def drawGrid(self):
        for y in range(0, self.window_size.x, self.tile_size):
            for x in range(0, self.window_size.y, self.tile_size):
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                pygame.draw.rect(self.d, "#000000", rect, 1)

    def display_background_image(self):
        x_pos = 0 - (self.top_left_tile.x * self.tile_size)
        y_pos = 0 - (self.top_left_tile.y * self.tile_size)
        # INVERT COORDS FOR PYGAME
        self.d.blit(self.background_image, (x_pos, y_pos))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = Position(mouse_pos[1], mouse_pos[0])
        if pygame.mouse.get_focused():
            # Mouse is in the border of the screen, move the whole screen
            self.move_screen_with_mouse(mouse_pos)
            # Draw tile highlight on cursor pos
            self.draw_mouse_highlight(mouse_pos)
            # Refresh mouse_map_position
            self.mouse_map_position = (mouse_pos // self.tile_size) + self.top_left_tile
        # Zoom In / Out
        if keys[K_PLUS]:  # Zoom in
            self.visible_tiles.x = ((self.visible_tiles.x - 1) / 2) + 1
            self.visible_tiles.y = ((self.visible_tiles.y - 1) / 2) + 1
            self.tile_size = int(self.tile_size * 2)
        if keys[K_MINUS]:
            self.visible_tiles.x = ((self.visible_tiles.x - 1) * 2) + 1
            self.visible_tiles.y = ((self.visible_tiles.y - 1) * 2) + 1
            self.tile_size = int(self.tile_size / 2)
        if keys[K_RETURN]:
            pass
        if buttons[0]:
            if self.is_top_layer:
                print(f"top adding {self.selected_sprite_idx} at y {self.mouse_map_position.y}, x {self.mouse_map_position.x}")
                self.top_layer[self.mouse_map_position.y][self.mouse_map_position.x] = str(self.selected_sprite_idx)
            else:
                print(f"bottom adding {self.selected_sprite_idx} at y {self.mouse_map_position.y}, x {self.mouse_map_position.x}")
                self.bottom_layer[self.mouse_map_position.y][self.mouse_map_position.x] = str(self.selected_sprite_idx)


    def draw_map(self):
        for y in range(self.visible_tiles.y):
            for x in range(self.visible_tiles.x):
                pos = Position(y, x)
                self.display_entity(pos)

    def display_entity(self, tile_screen_pos):
        map_pos = tile_screen_pos + self.top_left_tile
        top_entity = self.top_layer[map_pos.y][map_pos.x]
        bottom_entity = self.bottom_layer[map_pos.y][map_pos.x]
        tile_pixel_pos = tile_screen_pos * self.tile_size
        if bottom_entity:
            self.d.blit(self.sprites[bottom_entity], (tile_pixel_pos.x, tile_pixel_pos.y))
        if top_entity:
            self.d.blit(self.sprites[top_entity], (tile_pixel_pos.x, tile_pixel_pos.y))

    def draw_mouse_highlight(self, mouse_pos):
        tile_on_screen = mouse_pos // self.tile_size
        pygame.draw.rect(self.d, (255,0,0), pygame.Rect(
            tile_on_screen.x * self.tile_size - 1,
            tile_on_screen.y * self.tile_size - 1,
            self.tile_size + 2,
            self.tile_size + 2
        ), 2)

    def move_screen_with_mouse(self, mouse_pos):
        if mouse_pos.y < self.moving_zone_pixels.y:
            self.top_left_tile.y -= 1
        if mouse_pos.x > self.window_size.x - self.moving_zone_pixels.x:
            self.top_left_tile.x += 1
        if mouse_pos.y > self.window_size.y - self.moving_zone_pixels.y:
            self.top_left_tile.y += 1
        if mouse_pos.x < self.moving_zone_pixels.x:
            self.top_left_tile.x -= 1

if __name__ == '__main__':
    app = App()
    app.launch()
