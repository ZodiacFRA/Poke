import copy

import pygame

import display_utils
from .Panel import Panel
from Vector2 import Vector2


class TileVizualizer(Panel):
    def __init__(self, display, px_tile_size, sprites, context):
        super().__init__(display, px_tile_size, sprites, context)
        ### Positioning
        self.t_top_tile_pos = Vector2(2, 4)
        self.t_bottom_tile_pos = Vector2(2, 8)
        self.px_top_tile_pos = self.t_top_tile_pos * self.px_tile_size
        self.px_bottom_tile_pos = self.t_bottom_tile_pos * self.px_tile_size
        # Ressources
        self.transformed_sprites = display_utils.create_isometric_sprites(
            self.sprites, self.px_tile_size
        )
        ### Text
        self.large = pygame.font.SysFont(None, 44)
        self.medium = pygame.font.SysFont(None, 32)
        ### Drawing paths
        top_contour_path = [
            Vector2(0, 32),
            Vector2(64, 0),
            Vector2(128, 32),
        ]
        self.top_tile_top_contour = [
            (p + self.px_top_tile_pos).get() for p in top_contour_path
        ]
        self.bottom_tile_top_contour = [
            (p + self.px_bottom_tile_pos).get() for p in top_contour_path
        ]
        path = [
            (Vector2(0, 32), Vector2(64, 64), (255, 255, 255)),
            (Vector2(128, 32), Vector2(64, 64), (150, 150, 150)),
        ]
        self.top_tile_side_path = [
            (start + self.px_top_tile_pos, end + self.px_top_tile_pos, color)
            for start, end, color in path
        ]
        self.bottom_tile_side_path = [
            (start + self.px_bottom_tile_pos, end + self.px_bottom_tile_pos, color)
            for start, end, color in path
        ]

    def draw(self):
        self.display.fill((40, 40, 40))
        if self.context["t_m_hovered_tile"] is not None:
            self.draw_hovered_tile_contents()
        self.draw_tile_layers_contours()
        self.draw_text(
            self.large, "Map Editor", Vector2(self.t_panel_size.x // 2, 1), center=True
        )

    def draw_text(self, font, text, t_pos, center=False):
        img = font.render(text, True, (255, 255, 255))
        rect = img.get_rect()
        px_delta = 0
        if center:
            px_delta += img.get_size()[0] // 2
        # pygame.draw.rect(img, (255, 255, 255), rect, 1)
        self.display.blit(
            img, (t_pos * self.px_tile_size + Vector2(-px_delta, 0)).get()
        )

    def draw_hovered_tile_contents(self):
        bottom_entity_data = self.context["map"].get(
            "bottom", self.context["t_m_hovered_tile"]
        )
        if bottom_entity_data:
            self.display.blit(
                self.transformed_sprites[bottom_entity_data[1]],
                self.px_bottom_tile_pos.get(),
            )
            self.draw_text(
                self.medium,
                f"{bottom_entity_data[0].title()}",
                Vector2(self.t_panel_size.x // 2, self.t_bottom_tile_pos.y - 1),
                center=True,
            )
            self.draw_text(
                self.medium,
                f"{bottom_entity_data[1]}",
                Vector2(self.t_panel_size.x // 2 + 3, self.t_bottom_tile_pos.y + 1),
                center=True,
            )
        else:
            pygame.draw.lines(
                self.display, (255, 255, 255), False, self.bottom_tile_top_contour, 1
            )
        top_entity_data = self.context["map"].get(
            "top", self.context["t_m_hovered_tile"]
        )
        if top_entity_data:
            self.display.blit(
                self.transformed_sprites[top_entity_data[1]],
                self.px_top_tile_pos.get(),
            )
            self.draw_text(
                self.medium,
                f"{top_entity_data[0].title()}",
                Vector2(self.t_panel_size.x // 2, self.t_top_tile_pos.y - 1),
                center=True,
            )
            self.draw_text(
                self.medium,
                f"{top_entity_data[1]}",
                Vector2(self.t_panel_size.x // 2 + 3, self.t_top_tile_pos.y + 1),
                center=True,
            )
        else:
            pygame.draw.lines(
                self.display, (255, 255, 255), False, self.top_tile_top_contour, 1
            )

    def draw_tile_layers_contours(self):
        # Draw "sides" of the isometric tiles
        for y in range(15):
            for start, end, color in copy.deepcopy(self.top_tile_side_path):
                start.y += y
                end.y += y
                pygame.draw.line(self.display, color, start.get(), end.get(), 1)
            for start, end, color in copy.deepcopy(self.bottom_tile_side_path):
                start.y += y
                end.y += y
                pygame.draw.line(self.display, color, start.get(), end.get(), 1)
