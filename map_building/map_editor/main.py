import time

import pygame
from pygame.locals import *

from Position import Position
from utils import *


class App(object):
    def __init__(self):
        ####
        self.visible_tiles = Position(21, 21)
        self.visible_tiles.x = 21
        self.visible_tiles.y = 21
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
        self.map = []  # TODO: INIT THE MAP
        # self.map_size = Position()
        ####
        self.moving_zone_pixels = self.window_size // 10
        self.top_left_tile = Position(0, 0)
        self.mouse_map_position = Position(-1, -1)
        ####
        self.delta_time = 1 / 15
        self.start_time = time.time()

    def launch(self):
        while self.handle_loop():
            self.display_background_image()
            self.drawGrid()
            self.handle_input()

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
        self.d.fill("#ffffff")
        return 1

    # def draw_map(self, map, game_state):
    #     for y_idx in range(self.map_tiles_nbr.y):
    #         for x_idx in range(self.map_tiles_nbr.x):
    #             screen_pos = Position(y=y_idx, x=x_idx)
    #             map_pos = self.screen_pos_to_map_pos(screen_pos)
    #             line = map.get(map_pos.y, None)
    #             if not line: continue
    #             tile = line.get(map_pos.x, None)
    #             if not tile: continue
    #             self.display_entity(*tile, screen_pos)

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
        # Zoom In / Out
        if keys[K_PLUS]:  # Zoom in
            self.visible_tiles.x = ((self.visible_tiles.x - 1) / 2) + 1
            self.visible_tiles.y = ((self.visible_tiles.y - 1) / 2) + 1
            self.tile_size = int(self.tile_size * 2)
        if keys[K_MINUS]:
            self.visible_tiles.x = ((self.visible_tiles.x - 1) * 2) + 1
            self.visible_tiles.y = ((self.visible_tiles.y - 1) * 2) + 1
            self.tile_size = int(self.tile_size / 2)
        # Movement on map
        # if keys[K_UP]:
        #     self.top_left_tile.y -= 1
        # elif keys[K_DOWN]:
        #     self.top_left_tile.y += 1
        # if keys[K_RIGHT]:
        #     self.top_left_tile.x += 1
        # elif keys[K_LEFT]:
        #     self.top_left_tile.x -= 1
        #
        if keys[K_RETURN]:
            pass
        if buttons[0]:
            pass

    def draw_mouse_highlight(self, mouse_pos):
        tile_on_screen = mouse_pos // self.tile_size
        pygame.draw.rect(self.d, (255,0,0), pygame.Rect(
            tile_on_screen.x * self.tile_size - 1,
            tile_on_screen.y * self.tile_size - 1,
            self.tile_size + 2,
            self.tile_size + 2
        ), 2)
        # print('drawn at ', )
        # tile_on_map =

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
