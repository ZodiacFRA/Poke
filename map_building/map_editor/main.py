import time

import pygame

import config
from Map import Map
import display_utils
from Vector2 import Vector2


class App(object):
    def __init__(
        self,
        sprites_dir_path,
        map_json_path=None,
        crop_map=True,
        backdrop_path=None,
        backdrop_resize_factor=1,
    ):
        ### FPS
        self.delta_time = 1 / 30
        self.frame_start_time = time.time()
        ### Pygame
        pygame.init()
        pygame.display.set_caption("Level editor")
        ### Display
        self.px_window_size = config.t_window_size * config.px_tile_size
        self.display = pygame.display.set_mode(self.px_window_size.get())
        # Load ressources
        self.sprites = display_utils.load_sprites(sprites_dir_path)
        self.backdrop = (
            display_utils.load_sprite(
                backdrop_path, resize_factor=backdrop_resize_factor
            )
            if backdrop_path
            else None
        )
        ### Context
        self.context = {
            "is_top_layer_selected": True,
            "selected_sprite_name": 1,
            "t_m_hovered_tile": Vector2(0, 0),
            "map": Map(map_json_path, self.backdrop, crop=crop_map),
        }
        # Create layout
        self.panels = display_utils.create_panels(
            self.display,
            self.sprites,
            self.context,
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
        sprites_dir_path="../../client/sprites/",
        map_json_path="../sprite_map_to_map/map_loadable.json",
        backdrop_path="../ressources/map_gen1_bw.png",
        backdrop_resize_factor=2,
    )
    app.launch()
