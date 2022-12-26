import pygame

from .Panel import Panel
from Vector2 import Vector2


class TileVizualizer(Panel):
    def __init__(self, display, px_tile_size, sprites, context):
        super().__init__(display, px_tile_size, sprites, context)
        self.px_top_tile_pos = Vector2(1, 2) * self.px_tile_size
        self.px_bottom_tile_pos = Vector2(1, 6) * self.px_tile_size

    def draw(self):
        self.display.fill((40, 40, 40))
        if self.context["t_m_hovered_tile"] is not None:
            self.draw_hovered_tile_contents()
        self.draw_tile_layers_contours()

    def draw_hovered_tile_contents(self):
        bottom_entity_data = self.context["map"].get(
            "bottom", self.context["t_m_hovered_tile"]
        )
        if bottom_entity_data:
            self.display.blit(
                self.sprites[bottom_entity_data[1]],
                self.px_bottom_tile_pos.get(),
            )
        top_entity_data = self.context["map"].get(
            "top", self.context["t_m_hovered_tile"]
        )
        if top_entity_data:
            self.display.blit(
                self.sprites[top_entity_data[1]],
                self.px_top_tile_pos.get(),
            )

    def draw_tile_layers_contours(self):
        pygame.draw.rect(
            self.display,
            (255, 255, 255),
            pygame.Rect(
                *(self.px_top_tile_pos - Vector2(1, 1)).get(),
                self.px_tile_size + 2,
                self.px_tile_size + 2,
            ),
            1,
        )
        pygame.draw.rect(
            self.display,
            (255, 255, 255),
            pygame.Rect(
                *(self.px_bottom_tile_pos - Vector2(1, 1)).get(),
                self.px_tile_size + 2,
                self.px_tile_size + 2,
            ),
            1,
        )
