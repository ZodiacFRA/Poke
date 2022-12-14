import sys
import time
import argparse

import pygame
from pygame.locals import *

from Position import Position
from utils import *


class App(object):
    """
    """
    def __init__(self, background_image_path, sprites_folder_path):
        self.visible_tiles = Position(21, 21)
        self.tile_size = 32
        self.window_size = Position(
            self.tile_size * self.visible_tiles.y,
            self.tile_size * self.visible_tiles.x
        )
        self.full_window_size = self.window_size + Position(0, 200)
        ####
        pygame.init()
        pygame.display.set_caption('Level editor')
        self.d = pygame.display.set_mode((self.full_window_size.x, self.full_window_size.y))
        ####
        self.scale_ratio = 1
        self.sprites = load_sprites(sprites_folder_path)
        self.background_image = load_sprite(
            background_image_path,
            resize_factor=2
        )
        # "in_use" members are needed as we want to rescale from the original sprites each time
        self.in_use_sprites = self.sprites
        self.in_use_background_image = self.background_image
        ####
        reference_map_size = self.background_image.get_size()
        self.map_size = Position(reference_map_size[1], reference_map_size[0]) // self.tile_size
        self.top_layer = init_map_layout(self.map_size)
        self.bottom_layer = init_map_layout(self.map_size)
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
            # Map related draws
            self.display_background_image()
            # self.drawGrid()
            self.draw_map()
            self.handle_input()
            # UI related draws
            self.draw_ui()

    def draw_ui(self):
        # Right UI
        pygame.draw.rect(
            self.d, (255, 255, 255),
            pygame.Rect(self.window_size.x, 0, self.full_window_size.x - self.window_size.x, self.window_size.y)
        )
        # Separation
        pygame.draw.rect(
            self.d, (0, 0, 0),
            pygame.Rect(self.window_size.x, 0, 4, self.window_size.y)
        )

    def handle_input(self):
        keys = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = Position(mouse_pos[1], mouse_pos[0])
        # Check if mouse is hovering on the map
        if self.is_mouse_focused_on_map(mouse_pos):
            self.mouse_map_position = (mouse_pos // self.tile_size) + self.top_left_tile
            # Mouse is in the border of the screen, move the whole screen
            self.move_screen_with_mouse(mouse_pos)
            # Draw tile highlight on cursor pos
            self.draw_mouse_highlight(mouse_pos)
            # Refresh mouse_map_position
        # Zoom In / Out
        if keys[K_r] and self.scale_ratio < 1:
            self.zoom_in()
        if keys[K_t] and self.scale_ratio > 1 / 8:
            self.zoom_out()
        # Serialize
        if keys[K_v]:
            serialize(self.top_layer, self.bottom_layer, self.map_size)
        # Layer selection
        if keys[K_a]:
            self.is_top_layer = not self.is_top_layer
        # Apply sprite
        if buttons[0]:
            if self.is_top_layer:
                self.top_layer[self.mouse_map_position.y][self.mouse_map_position.x] = str(self.selected_sprite_idx)
            else:
                self.bottom_layer[self.mouse_map_position.y][self.mouse_map_position.x] = str(self.selected_sprite_idx)
        # Delete sprite
        if buttons[2]:
            if self.is_top_layer:
                self.top_layer[self.mouse_map_position.y][self.mouse_map_position.x] = None
            else:
                self.bottom_layer[self.mouse_map_position.y][self.mouse_map_position.x] = None

    def zoom_in(self):
        self.visible_tiles.x = int(((self.visible_tiles.x - 1) / 2) + 1)
        self.visible_tiles.y = int(((self.visible_tiles.y - 1) / 2) + 1)
        self.tile_size = int(self.tile_size * 2)
        self.scale_ratio *= 2
        self.in_use_background_image = rescale_sprite(self.background_image, self.scale_ratio)
        self.in_use_sprites = rescale_sprites(self.sprites, self.scale_ratio)

    def zoom_out(self):
        self.visible_tiles.x = int(((self.visible_tiles.x - 1) * 2) + 1)
        self.visible_tiles.y = int(((self.visible_tiles.y - 1) * 2) + 1)
        self.tile_size = int(self.tile_size / 2)
        self.scale_ratio /= 2
        self.in_use_background_image = rescale_sprite(self.background_image, self.scale_ratio)
        self.in_use_sprites = rescale_sprites(self.sprites, self.scale_ratio)

    def draw_map(self):
        for y in range(self.visible_tiles.y):
            for x in range(self.visible_tiles.x):
                pos = Position(y, x)
                self.display_entity(pos)

    def display_entity(self, tile_screen_pos):
        map_pos = tile_screen_pos + self.top_left_tile
        if not self.is_valid_pos_on_map(map_pos):
            return
        top_entity = self.top_layer[map_pos.y][map_pos.x]
        bottom_entity = self.bottom_layer[map_pos.y][map_pos.x]
        tile_pixel_pos = tile_screen_pos * self.tile_size
        if bottom_entity:
            self.d.blit(self.in_use_sprites[bottom_entity], (tile_pixel_pos.x, tile_pixel_pos.y))
        if top_entity:
            self.d.blit(self.in_use_sprites[top_entity], (tile_pixel_pos.x, tile_pixel_pos.y))

    def draw_mouse_highlight(self, mouse_pos):
        tile_on_screen = mouse_pos // self.tile_size
        color = (255, 0, 0) if self.is_top_layer else (0, 255, 0)
        pygame.draw.rect(self.d, color, pygame.Rect(
            tile_on_screen.x * self.tile_size - 1,
            tile_on_screen.y * self.tile_size - 1,
            self.tile_size + 2,
            self.tile_size + 2
        ), 2)

    def move_screen_with_mouse(self, mouse_pos):
        if mouse_pos.y < self.moving_zone_pixels.y:
            self.top_left_tile.y -= int(1 / self.scale_ratio)
        if mouse_pos.x > self.window_size.x - self.moving_zone_pixels.x:
            self.top_left_tile.x += int(1 / self.scale_ratio)
        if mouse_pos.y > self.window_size.y - self.moving_zone_pixels.y:
            self.top_left_tile.y += int(1 / self.scale_ratio)
        if mouse_pos.x < self.moving_zone_pixels.x:
            self.top_left_tile.x -= int(1 / self.scale_ratio)

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
        self.d.fill("#000000")
        return 1

    def display_background_image(self):
        x_pos = 0 - (self.top_left_tile.x * self.tile_size)
        y_pos = 0 - (self.top_left_tile.y * self.tile_size)
        # INVERT COORDS FOR PYGAME
        self.d.blit(self.in_use_background_image, (x_pos, y_pos))

    def is_valid_pos_on_map(self, pos):
        if pos.x < 0 or pos.y < 0 or pos.x >= self.map_size.x or pos.y >= self.map_size.y:
            return False
        else:
            return True

    def drawGrid(self):
        for y in range(0, self.window_size.x, self.tile_size):
            for x in range(0, self.window_size.y, self.tile_size):
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                pygame.draw.rect(self.d, "#000000", rect, 1)

    def is_mouse_focused_on_map(self, mouse_pos):
        if not pygame.mouse.get_focused():
            return False
        if mouse_pos.x > self.window_size.x:
            return False
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog = 'Poke Map / Level editor',
                    description = 'Poke Map / Level editor',
                    epilog = "press:\n'R' to zoom\n'T' to dezoom\n'V' to serialize the result to a json loadable by the game\n'A' to change edited layer")
    parser.add_argument('-b', '--background_image', required=False, type=str, default="../ressources/wholemap.png")
    parser.add_argument('-s', '--sprites_folder_path', required=False, type=str, default="../../client/sprites/")
    args = parser.parse_args()
    app = App(args.background_image, args.sprites_folder_path)
    app.launch()
