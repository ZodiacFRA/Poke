import time

import pygame

import map_utils
import config
import display_utils
from Vector2 import Vector2


class App(object):
    def __init__(self, sprites_folder_path, backdrop_path=None, map_json_path=None):
        ### FPS
        self.delta_time = 1 / 30
        self.frame_start_time = time.time()
        ### Context
        self.context = {
            "is_top_layer_selected": True,
            "selected_sprite_name": 0,
            "t_m_hovered_tile": Vector2(0, 0),
        }
        ### Pygame
        pygame.init()
        pygame.display.set_caption("Level editor")
        ### Window & Layout
        self.px_window_size = config.t_window_size * config.px_tile_size
        self.display = pygame.display.set_mode(self.px_window_size.get())
        self.sprites = display_utils.load_sprites(sprites_folder_path)
        self.backdrop = (
            display_utils.load_sprite(backdrop_path, resize_factor=2)
            if backdrop_path
            else None
        )
        self.panels = display_utils.create_panels(
            self.display,
            self.sprites,
            self.context,
            map_utils.load_map_from_json(map_json_path, crop=True),
            self.backdrop,
        )

    def launch(self):
        while self.handle_loop():
            inputs = {
                "cursor": Vector2(*pygame.mouse.get_pos()),
                "buttons": pygame.mouse.get_pressed(),
                "keys": pygame.key.get_pressed(),
            }
            # Serialization
            if inputs["keys"][pygame.K_v]:
                self.serialize()
            # Process panels
            for panel in self.panels:
                panel.process(inputs)
                panel.draw()
            pygame.display.update()

    def handle_loop(self, debug=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ ] - App: Stopping")
                pygame.quit()
                return 0
        to_sleep = self.delta_time - (time.time() - self.frame_start_time)
        if to_sleep > 0:
            time.sleep(to_sleep)
        elif debug:
            print(f"[-] - App: Lagging behind: {to_sleep}")
        self.frame_start_time = time.time()
        self.display.fill("#000000")
        return 1

    def serialize(self):
        print("SERIALIZATION NOT IMPLEMENTED")


if __name__ == "__main__":
    app = App(
        sprites_folder_path="../../client/sprites/",
        backdrop_path="../ressources/map_gen1_bw.png",
        map_json_path="../sprite_map_to_map/map_loadable.json",
    )
    app.launch()
