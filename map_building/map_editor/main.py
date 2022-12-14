import time

import pygame
from pygame.locals import *

from utils import *


class App(object):
    def __init__(self):
        self.visible_tiles_width = 21
        self.visible_tiles_height = 21
        self.tile_size = 32
        self.window_width = self.tile_size * self.visible_tiles_width
        self.window_height = self.tile_size * self.visible_tiles_height
        ####
        self.center_tile_pos = (
            0 + int(visible_tiles_height / 2),
            0 + int(visible_tiles_width / 2)
        )
        ####
        pygame.init()
        pygame.display.set_caption('Level editor')
        self.d = pygame.display.set_mode((self.window_width, self.window_height))
        ####
        self.sprites = load_sprites("../../client/sprites/")
        self.background_image = load_sprite(
            "../ressources/wholemap.png",
            resize_factor=2
        )
        ####
        self.delta_time = 1 / 30
        self.start_time = time.time()

    def launch(self):
        while self.handle_loop():
            self.display_background_image()
            self.drawGrid()

    def handle_loop(self):
        pygame.display.update()
        self.handle_input()
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
        return 1

    def draw_map(self, map, game_state):
        for y_idx in range(self.map_tiles_nbr.y):
            for x_idx in range(self.map_tiles_nbr.x):
                screen_pos = Position(y=y_idx, x=x_idx)
                map_pos = self.screen_pos_to_map_pos(screen_pos)
                line = map.get(map_pos.y, None)
                if not line: continue
                tile = line.get(map_pos.x, None)
                if not tile: continue
                self.display_entity(*tile, screen_pos)

    def drawGrid(self):
        for y in range(0, self.window_width, TILE_SIZE):
            for x in range(0, self.window_height, TILE_SIZE):
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.d, "#000000", rect, 1)

    def display_background_image(self):
        self.d.blit(
            self.background_image,
            (0, 0)
        )

    def handle_input(self):
        keys = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()
        if keys[K_PLUS]:  # Zoom in
            pass
        if keys[K_RETURN]:
            pass
        if keys[K_LEFT] and self.angle_speed >= 0:
            pass
        elif keys[K_RIGHT]:
            pass
        if buttons[0]:
            pass

if __name__ == '__main__':
    app = App()
    app.launch()
