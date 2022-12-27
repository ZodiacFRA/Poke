import time

import pygame

from Vector2 import Vector2


class EmptyPanel(object):
    """Made just for empty panels (borders)"""

    def __init__(self, display, px_tile_size):
        self.display = display
        self.px_anchor = Vector2(*self.display.get_abs_offset())
        self.px_tile_size = px_tile_size
        self.px_panel_size = Vector2(*self.display.get_size())
        self.t_panel_size = self.px_panel_size // px_tile_size
        self.delays = {}

    def draw(self):
        size = self.display.get_size()
        is_vertical = size[1] > size[0]
        half_tile = self.px_tile_size // 2
        """Draw a single white line in the middle"""
        if is_vertical:
            pygame.draw.line(
                self.display,
                "#ffffff",
                (half_tile, 0),
                (half_tile, size[1]),
                5,
            )
        else:
            pygame.draw.line(
                self.display,
                "#ffffff",
                (0, half_tile),
                (size[0], half_tile),
                5,
            )

    def process(self, inputs):
        return

    def is_cursor_hovering(self, px_p_pos):
        return px_p_pos >= Vector2(0, 0) and px_p_pos < self.px_panel_size

    def can_click(self, button_id):
        if button_id not in self.delays:
            return True
        now = time.time()
        if now - self.delays[button_id] > self.input_delta_time:
            self.delays[button_id] = now
            return True
        else:
            return False


class Panel(EmptyPanel):
    def __init__(self, display, px_tile_size, sprites, context):
        super().__init__(display, px_tile_size)
        self.sprites = sprites
        self.scaled_sprites = sprites
        self.context = context
        self.px_size = Vector2(*self.display.get_size())

    def draw(self):
        self.display.fill("#ff0000")
