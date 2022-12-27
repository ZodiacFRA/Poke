import pygame

import display_utils
from .Panel import Panel
from Vector2 import Vector2


class SpriteSelection(Panel):
    def __init__(self, display, px_tile_size, sprites, context):
        super().__init__(display, px_tile_size, sprites, context)
        self.grid_surface = display_utils.create_grid_surface(
            self.px_panel_size, self.px_tile_size
        )
        self.px_mouse_moving_zone = self.px_panel_size // 6
        self.t_sprite_row_idx = 0
        self.t_y_limit = len(self.sprites) // self.t_panel_size.x
        self.sprite_name_list = list(self.sprites.keys())
        self.t_p_selected_position = Vector2(0, 0)

    ### Drawing functions

    def draw(self):
        self.display.fill((40, 40, 40))
        self.draw_sprites()
        self.draw_grid()
        self.draw_highlighted_tile()

    def draw_sprites(self):
        sprite_name_list = self.sprite_name_list[
            self.t_sprite_row_idx * self.t_panel_size.x :
        ]
        for sprite_idx, sprite_name in enumerate(sprite_name_list):
            t_p_sprite_pos = Vector2(
                sprite_idx % self.t_panel_size.x, sprite_idx // self.t_panel_size.x
            )
            if t_p_sprite_pos.y > self.t_panel_size.y:
                break
            self.display.blit(
                self.sprites[sprite_name],
                (t_p_sprite_pos * self.px_tile_size).get(),
            )

    def draw_highlighted_tile(self):
        pygame.draw.rect(
            self.display,
            (255, 255, 255),
            pygame.Rect(
                *((self.t_p_selected_position * self.px_tile_size)).get(),
                self.px_tile_size,
                self.px_tile_size,
            ),
            2,
        )

    def draw_grid(self):
        self.display.blit(self.grid_surface, (0, 0))

    ### Processing functions

    def process(self, inputs):
        px_p_cursor = inputs["cursor"] - self.px_anchor
        if self.is_cursor_hovering(px_p_cursor):
            self.scroll_with_mouse(px_p_cursor)
            t_p_hovered_tile = (px_p_cursor) // self.px_tile_size
            self.process_mouse_buttons(inputs["buttons"], t_p_hovered_tile)

    def process_mouse_buttons(self, buttons, t_p_hovered_tile):
        if buttons[0] and self.can_click("l_mouse_button"):
            # Assign new selected position
            # this info can also be retrieved from self.context["selected_sprite_name"]
            # but would require many computations each time:
            # sprite_name -> sprite_idx -> sprite_pos -> p_sprite_pos
            self.t_p_selected_position = t_p_hovered_tile
            # Convert 2D pos to 1D pos (also add the scroll shift)
            hovered_tile_idx = (
                t_p_hovered_tile.y + self.t_sprite_row_idx
            ) * self.t_panel_size.x + t_p_hovered_tile.x
            # Get the sprite name from its index in the list
            self.context["selected_sprite_name"] = self.sprite_name_list[
                hovered_tile_idx
            ]

    def scroll_with_mouse(self, px_p_cursor):
        if px_p_cursor.y < self.px_mouse_moving_zone.y and self.t_sprite_row_idx > 0:
            self.t_sprite_row_idx -= 1
        elif px_p_cursor.y > self.px_panel_size.y - self.px_mouse_moving_zone.y:
            if self.t_sprite_row_idx < self.t_y_limit:
                self.t_sprite_row_idx += 1
