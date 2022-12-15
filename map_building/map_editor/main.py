import sys
import time
import argparse
import random

import pygame
from pygame.locals import *

from Position import Position
from utils import *


class App(object):
    def __init__(self, backdrop_path, sprites_folder_path, json_map_path):
        # Members needed for sprite scaling
        self.visible_tiles = Position(21, 21)
        self.base_tile_size = 32
        self.tile_size = self.base_tile_size
        self.scale_ratio = 1
        self.window_size = Position(
            self.tile_size * self.visible_tiles.y,
            self.tile_size * self.visible_tiles.x
        )
        # Number of sprites in one row in the sprite selector panel
        self.ui_sprites_width_nbr = 8
        # Size of the window with the right panel
        self.full_window_size = self.window_size + Position(0, self.base_tile_size * (self.ui_sprites_width_nbr + 1))
        ####
        pygame.init()
        pygame.display.set_caption('Level editor')
        self.d = pygame.display.set_mode((self.full_window_size.x, self.full_window_size.y))
        ####
        self.sprites = load_sprites(sprites_folder_path)
        self.backdrop = load_sprite(
            backdrop_path,
            resize_factor=2
        )
        # "in_use" members are needed as we want to rescale
        # from the original sprites each time
        self.in_use_sprites = self.sprites
        self.in_use_backdrop = self.backdrop
        ####
        backdrop_map_size = self.backdrop.get_size()
        self.backdrop_map_size = Position(
            backdrop_map_size[1], backdrop_map_size[0]
        ) // self.tile_size
        if json_map_path:
            self.top_layer, self.bottom_layer, self.map_size = get_layers_from_json_file(
                json_map_path
            )
        else:
            self.top_layer, self.bottom_layer, self.map_size = init_map_layout(
                self.backdrop_map_size
            )
        ####
        print(self.map_size, Position(len(self.top_layer), len(self.top_layer[0])))
        self.moving_zone_pixels = self.window_size // 6
        # Position the map in the center
        # self.top_left_tile = self.map_size // 2 + self.visible_tiles // 2
        self.top_left_tile = Position(0, 0)
        self.mouse_map_position = Position(-1, -1)
        ####
        self.delta_time = 1 / 30
        self.start_time = time.time()
        ####
        self.toggle_delta_time = 0.1
        self.edit_top_layer = True
        self.edit_top_layer_time = time.time()
        self.display_backdrop_flag = True
        self.display_backdrop_flag_time = time.time()
        self.selected_sprite_idx = 0

    def launch(self):
        while self.handle_loop():
            if self.display_backdrop_flag:
                self.display_backdrop()
            self.draw_map_panel()
            self.draw_sprite_sheet_panel()
            self.handle_key_inputs()
            self.handle_mouse_buttons_inputs()
            self.handle_mouse_movements()

    def draw_sprite_sheet_panel(self):
        # Draw the white background
        self.draw_ui()
        # Now draw the available sprites
        ui_width_px = self.full_window_size.x - self.window_size.x - self.base_tile_size
        sprites_per_column = ui_width_px // self.base_tile_size
        sprite_indexes_list = list(self.sprites.keys())
        sprite_indexes_list.sort(key=get_int_idx)
        for base_sprite_idx, sprite_idx in enumerate(sprite_indexes_list):
            pos = Position(base_sprite_idx // sprites_per_column, base_sprite_idx % sprites_per_column)
            pos *= self.base_tile_size
            pos += Position(0, self.window_size.x + self.base_tile_size)
            self.d.blit(self.sprites[sprite_idx], (pos.x, pos.y))
        # Draw the highlight of the selected sprite
        highlight_pos = Position(self.selected_sprite_idx // sprites_per_column, self.selected_sprite_idx % sprites_per_column)
        highlight_pos *= self.base_tile_size
        highlight_pos.x += self.window_size.x + self.base_tile_size
        pygame.draw.rect(self.d, (0, 255, 0), pygame.Rect(
            highlight_pos.x,
            highlight_pos.y,
            self.base_tile_size,
            self.base_tile_size
        ), 2)

    def handle_key_inputs(self):
        keys = pygame.key.get_pressed()
        # Zoom In / Out
        if keys[K_r] and self.scale_ratio < 1:
            self.zoom_in()
        if keys[K_t] and self.scale_ratio > 1 / 8:
            self.zoom_out()
        if keys[K_v]:  # Serialize
            serialize(self.top_layer, self.bottom_layer, self.map_size)
        if keys[K_a]:  # Layer selection
            if time.time() - self.edit_top_layer_time > self.toggle_delta_time:
                self.edit_top_layer = not self.edit_top_layer
                self.edit_top_layer_time = time.time()
                print(f"[ ] - Editing top layer: {self.edit_top_layer}")
        if keys[K_c]:  # Toggle backdrop visibility
            if time.time() - self.display_backdrop_flag_time > self.toggle_delta_time:
                self.display_backdrop_flag = not self.display_backdrop_flag
                self.display_backdrop_flag_time = time.time()
                print(f"[ ] - Backdrop visible: {self.display_backdrop_flag}")

    def handle_mouse_buttons_inputs(self):
        buttons = pygame.mouse.get_pressed()
        if buttons[0]:  # Apply sprite
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = Position(mouse_pos[1], mouse_pos[0])
            mouse_focus = self.get_mouse_focus(mouse_pos)
            # Check if mouse is hovering on the map panel
            if mouse_focus == 1:
                if self.edit_top_layer:
                    self.top_layer[self.mouse_map_position.y][self.mouse_map_position.x] = str(self.selected_sprite_idx)
                else:
                    self.bottom_layer[self.mouse_map_position.y][self.mouse_map_position.x] = str(self.selected_sprite_idx)
            # elif mouse is hovering on top of the right panel,
            elif mouse_focus == 2:
                # Update the self.selected_sprite_idx based on the mouse position
                tile_on_screen = mouse_pos // self.tile_size - Position(0, self.visible_tiles.x + 1)
                self.selected_sprite_idx = tile_on_screen.x + self.ui_sprites_width_nbr * tile_on_screen.y;
        if buttons[2]:  # Delete sprite
            if self.edit_top_layer:
                self.top_layer[self.mouse_map_position.y][self.mouse_map_position.x] = None
            else:
                self.bottom_layer[self.mouse_map_position.y][self.mouse_map_position.x] = None

    def handle_mouse_movements(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = Position(mouse_pos[1], mouse_pos[0])
        # Check if mouse is hovering on the map
        mouse_focus = self.get_mouse_focus(mouse_pos)
        if mouse_focus == 0:
            self.mouse_map_position = None
        elif mouse_focus == 1:  # on Map
            # Refresh mouse_map_position
            self.mouse_map_position = (mouse_pos // self.tile_size) + self.top_left_tile
            # Mouse is in the border of the screen, move the whole screen
            self.move_screen_with_mouse(mouse_pos)
            # Draw tile highlight on cursor pos
            self.draw_map_mouse_highlight(mouse_pos)
        elif mouse_focus == 2:  # On UI
            # Refresh mouse_sprites_position
            self.mouse_map_position = None

    def zoom_in(self):
        """ For both zoom_in and zoom_out, do not change the window size,
        only double or divide by 2 the sprite size and the nbr of visible tiles
        then rescale the backdrop and all the sprites
        """
        self.visible_tiles.x = int(((self.visible_tiles.x - 1) / 2) + 2)
        self.visible_tiles.y = int(((self.visible_tiles.y - 1) / 2) + 2)
        self.tile_size = int(self.tile_size * 2)
        self.scale_ratio *= 2
        self.in_use_backdrop = rescale_sprite(self.backdrop, self.scale_ratio)
        self.in_use_sprites = rescale_sprites(self.sprites, self.scale_ratio)

    def zoom_out(self):
        self.visible_tiles.x = int(((self.visible_tiles.x - 1) * 2) + 2)
        self.visible_tiles.y = int(((self.visible_tiles.y - 1) * 2) + 2)
        self.tile_size = int(self.tile_size / 2)
        self.scale_ratio /= 2
        self.in_use_backdrop = rescale_sprite(self.backdrop, self.scale_ratio)
        self.in_use_sprites = rescale_sprites(self.sprites, self.scale_ratio)

    def draw_map_panel(self):
        for y in range(self.visible_tiles.y):
            for x in range(self.visible_tiles.x):
                tile_screen_pos = Position(y, x)
                # Display the entity
                map_pos = tile_screen_pos + self.top_left_tile
                if not self.is_valid_pos_on_map(map_pos):
                    continue
                top_entity = self.top_layer[map_pos.y][map_pos.x]
                bottom_entity = self.bottom_layer[map_pos.y][map_pos.x]
                tile_pixel_pos = tile_screen_pos * self.tile_size
                if bottom_entity is not None:
                    # try:
                    self.d.blit(self.in_use_sprites[bottom_entity], (tile_pixel_pos.x, tile_pixel_pos.y))
                    # except:
                        # print(bottom_entity)
                if top_entity is not None:
                    # try:
                    self.d.blit(self.in_use_sprites[top_entity], (tile_pixel_pos.x, tile_pixel_pos.y))
                    # except:
                        # print(top_entity)

    def draw_map_mouse_highlight(self, mouse_pos):
        """ Only called when the mouse is on the map panel, will draw square borders
        on the hovered tile, color is based on the active layer """
        tile_on_screen = mouse_pos // self.tile_size
        color = (255, 255, 255) if self.edit_top_layer else (0, 0, 0)
        pygame.draw.rect(self.d, color, pygame.Rect(
            tile_on_screen.x * self.tile_size - 1,
            tile_on_screen.y * self.tile_size - 1,
            self.tile_size + 2,
            self.tile_size + 2
        ), 2)

    def move_screen_with_mouse(self, mouse_pos):
        """ if mouse is in the "movement zone" (on the edge of the map panel)
        move the map, use the scale ratio to move quicker or slower based on
        the level of zoom """
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

    def display_backdrop(self):
        x_pos = 0 - (self.top_left_tile.x * self.tile_size)
        y_pos = 0 - (self.top_left_tile.y * self.tile_size)
        self.d.blit(self.in_use_backdrop, (x_pos, y_pos))

    def is_valid_pos_on_map(self, pos):
        if pos.x < 0 or pos.y < 0 or pos.x > self.map_size.x or pos.y > self.map_size.y:
            return False
        else:
            return True

    def draw_grid(self):
        for y in range(0, self.window_size.x, self.tile_size):
            for x in range(0, self.window_size.y, self.tile_size):
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                pygame.draw.rect(self.d, "#000000", rect, 1)

    def get_mouse_focus(self, mouse_pos):
        """ 0 = outside window, 1 = on map, 2 = on ui """
        if not pygame.mouse.get_focused():
            return 0
        if mouse_pos.x > self.window_size.x:
            return 2
        return 1

    def draw_ui(self):
        # Right UI background
        pygame.draw.rect(self.d, "#ffffff",
            pygame.Rect(
                self.window_size.x, 0,
                self.full_window_size.x - self.window_size.x, self.window_size.y
            )
        )
        # Map / UI Separation stripes
        pygame.draw.rect(self.d, "#ffffff",
            pygame.Rect(
                self.window_size.x, 0,
                self.base_tile_size, self.window_size.y
            )
        )
        pygame.draw.line(self.d, "#000000",
            (self.window_size.x + 1, 0),
            (self.window_size.x + 1, self.window_size.y), 3
        )
        pygame.draw.line(self.d, "#000000",
            (self.window_size.x + self.base_tile_size - 2, 0),
            (self.window_size.x + self.base_tile_size - 2, self.window_size.y), 3
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog = 'Poke Map / Level editor',
                    description = 'Poke Map / Level editor',
                    epilog = "press:\n'R' to zoom\n'T' to dezoom\n'V' to serialize the result to a json loadable by the game\n'A' to change edited layer")
    parser.add_argument('-b', '--backdrop', required=False, type=str, default="../ressources/wholemap.png")
    parser.add_argument('-m', '--json_map_path', required=False, type=str, default="")
    parser.add_argument('-s', '--sprites_folder_path', required=False, type=str, default="../../client/sprites/")
    args = parser.parse_args()
    app = App(args.backdrop, args.sprites_folder_path, args.json_map_path)
    app.launch()
