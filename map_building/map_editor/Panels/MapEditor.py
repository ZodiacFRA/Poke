import pygame

import display_utils
from .Panel import Panel
from Vector2 import Vector2


class MapEditor(Panel):
    """_p_ is a position in panel space. (0, 0) is the anchor
    _m_ is a position in map space. (0, 0) is the top left tile on the map"""

    def __init__(self, display, px_tile_size, sprites, context, map_data, backdrop):
        super().__init__(display, px_tile_size, sprites, context)
        ### Map data
        self.map, self.t_map_size = map_data
        self.t_m_limits = self.t_map_size - self.t_panel_size
        ### Positions
        # TODO: propagate (flood search) from top left
        # t_m_first_non_empty_tile = self.get_first_non_empty_tile()
        # self.t_m_anchor = (
        #     t_m_first_non_empty_tile if t_m_first_non_empty_tile else Vector2(0, 0)
        # )
        ### Positioning
        self.t_m_anchor = Vector2(0, 0)
        self.px_p_delta = Vector2(0, 0)
        self.px_mouse_moving_zone = self.px_panel_size // 6
        self.px_p_cursor = None
        ### Zoom
        self.scale_ratio = 1
        self.px_scaled_tile_size = self.px_tile_size
        ### Backdrop
        self.backdrop = backdrop
        self.scaled_backdrop = backdrop
        self.scaled_backdrop.set_alpha(150)
        self.display_backdrop_flag = 0

    ### Drawing functions

    def draw(self):
        if self.display_backdrop_flag == 1:
            self.display_backdrop()
        self.draw_map()
        if self.display_backdrop_flag == 2:
            self.display_backdrop()
        self.draw_grid()
        self.draw_highlighted_tile()

    def display_backdrop(self):
        px_anchor = (Vector2(0, 0) - self.t_m_anchor) * self.px_scaled_tile_size
        self.display.blit(self.scaled_backdrop, (px_anchor - self.px_p_delta).get())

    def draw_map(self):
        for y in range(-1, self.t_panel_size.y + 1):
            for x in range(-1, self.t_panel_size.x + 1):
                t_p_tile_pos = Vector2(x, y)
                t_m_tile_pos = t_p_tile_pos + self.t_m_anchor
                px_p_tile_pos = (
                    t_p_tile_pos * self.px_scaled_tile_size - self.px_p_delta
                )
                if not self.is_valid_pos_on_map(t_m_tile_pos):
                    continue
                top_entity_data = self.map["top"][t_m_tile_pos.y][t_m_tile_pos.x]
                bottom_entity_data = self.map["bottom"][t_m_tile_pos.y][t_m_tile_pos.x]
                if bottom_entity_data:
                    self.display.blit(
                        self.scaled_sprites[bottom_entity_data[1]],
                        px_p_tile_pos.get(),
                    )
                if top_entity_data:
                    self.display.blit(
                        self.scaled_sprites[top_entity_data[1]],
                        px_p_tile_pos.get(),
                    )

    def draw_highlighted_tile(self):
        if self.context["t_m_hovered_tile"] is None:
            return
        color = (255, 255, 255) if self.context["is_top_layer_selected"] else (0, 0, 0)
        pygame.draw.rect(
            self.display,
            color,
            pygame.Rect(
                *(
                    (self.context["t_m_hovered_tile"] * self.px_scaled_tile_size)
                    - self.px_p_delta
                ).get(),
                self.px_scaled_tile_size,
                self.px_scaled_tile_size,
            ),
            2,
        )

    def draw_grid(self):
        px_height = self.px_panel_size.y + self.px_scaled_tile_size
        px_width = self.px_panel_size.x + self.px_scaled_tile_size
        for y in range(0, px_height, self.px_scaled_tile_size):
            for x in range(
                0,
                px_width,
                self.px_scaled_tile_size,
            ):
                px_p_pos = Vector2(x, y) - self.px_p_delta
                rect = pygame.Rect(
                    *px_p_pos.get(), self.px_scaled_tile_size, self.px_scaled_tile_size
                )
                pygame.draw.rect(self.display, "#000000", rect, 1)

    ### Processing functions

    def process(self, inputs):
        # Mouse related
        px_p_cursor = inputs["cursor"] - self.px_anchor
        if self.is_cursor_hovering(px_p_cursor):
            self.context["t_m_hovered_tile"] = px_p_cursor // self.px_scaled_tile_size
            self.move_map_with_mouse(px_p_cursor)
        else:
            self.context["t_m_hovered_tile"] = None
        # Keyboard related
        self.process_key_inputs(inputs["keys"])

    def process_key_inputs(self, keys):
        # Zoom In / Out
        if keys[pygame.K_r] and self.scale_ratio < 2:
            self.zoom_in()
        if keys[pygame.K_t] and self.scale_ratio > 1 / 4:
            self.zoom_out()

    def zoom_in(self):
        """For both zoom_in and zoom_out, do not change the window size,
        only double or divide by 2 the sprite size and the nbr of visible tiles
        then rescale the backdrop and all the sprites
        """
        self.t_panel_size.x = int(self.t_panel_size.x // 2)
        self.t_panel_size.y = int(self.t_panel_size.y // 2)
        self.px_scaled_tile_size = int(self.px_scaled_tile_size * 2)
        self.t_m_limits = self.t_map_size - self.t_panel_size
        self.scale_ratio *= 2
        self.scaled_backdrop = display_utils.rescale_sprite(
            self.backdrop, self.scale_ratio
        )
        self.scaled_sprites = display_utils.rescale_sprites(
            self.sprites, self.scale_ratio
        )

    def zoom_out(self):
        self.t_panel_size.x = int(self.t_panel_size.x * 2)
        self.t_panel_size.y = int(self.t_panel_size.y * 2)
        self.px_scaled_tile_size = int(self.px_scaled_tile_size / 2)
        self.t_m_limits = self.t_map_size - self.t_panel_size
        self.scale_ratio /= 2
        self.scaled_backdrop = display_utils.rescale_sprite(
            self.backdrop, self.scale_ratio
        )
        self.scaled_sprites = display_utils.rescale_sprites(
            self.sprites, self.scale_ratio
        )

    def move_map_with_mouse(self, px_p_cursor):
        """t_tiles_delta represents how far the cursor is from the mouse_moving_zone
        the farther away, the faster we move"""
        # Vertical
        if px_p_cursor.y < self.px_mouse_moving_zone.y and self.t_m_anchor.y > 0:
            px_delta = self.px_mouse_moving_zone.y - px_p_cursor.y
            self.t_m_anchor.y -= px_delta // self.px_scaled_tile_size
            self.px_p_delta.y -= px_delta % self.px_scaled_tile_size
        elif px_p_cursor.y > self.px_panel_size.y - self.px_mouse_moving_zone.y:
            if self.t_m_anchor.y < self.t_m_limits.y:
                px_delta = self.px_mouse_moving_zone.y - (
                    self.px_panel_size.y - px_p_cursor.y
                )
                self.t_m_anchor.y += px_delta // self.px_scaled_tile_size
                self.px_p_delta.y += px_delta % self.px_scaled_tile_size
        # Horizontal
        if px_p_cursor.x < self.px_mouse_moving_zone.x and self.t_m_anchor.x > 0:
            px_delta = self.px_mouse_moving_zone.x - px_p_cursor.x
            self.t_m_anchor.x -= px_delta // self.px_scaled_tile_size
            self.px_p_delta.x -= px_delta % self.px_scaled_tile_size
        elif px_p_cursor.x > self.px_panel_size.x - self.px_mouse_moving_zone.x:
            if self.t_m_anchor.x < self.t_m_limits.x:
                px_delta = self.px_mouse_moving_zone.x - (
                    self.px_panel_size.x - px_p_cursor.x
                )
                self.t_m_anchor.x += px_delta // self.px_scaled_tile_size
                self.px_p_delta.x += px_delta % self.px_scaled_tile_size
        # Now transfer pixels delta to tiles delta if needed (when the delta is > px_scaled_tile_size)
        if self.px_p_delta // self.px_scaled_tile_size:
            self.t_m_anchor += self.px_p_delta // self.px_scaled_tile_size
            self.px_p_delta = self.px_p_delta % self.px_scaled_tile_size

    ### Utils functions

    def is_valid_pos_on_map(self, pos):
        if (
            pos.x < 0
            or pos.y < 0
            or pos.x >= self.t_map_size.x
            or pos.y >= self.t_map_size.y
        ):
            return False
        else:
            return True

    def is_cursor_hovering(self, px_p_pos):
        return px_p_pos < self.px_panel_size

    def get_first_non_empty_tile(self):
        for y in range(len(self.map["top"])):
            for x in range(len(self.map["top"][y])):
                if self.map["top"][y][x] or self.map["bottom"][y][x]:
                    return Vector2(x, y)
        return None
