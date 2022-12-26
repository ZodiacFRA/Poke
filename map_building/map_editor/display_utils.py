import os
from collections import OrderedDict

import pygame
from tqdm import tqdm

import config
import Panels


def create_panels(display, sprites, context, backdrop):
    panels = [
        Panels.MapEditor(
            display.subsurface(
                pygame.Rect(
                    0, 0, *(config.t_map_editor_panel_size * config.px_tile_size).get()
                )
            ),
            config.px_tile_size,
            sprites,
            context,
            backdrop,
        ),
        Panels.TileVizualizer(
            display.subsurface(
                pygame.Rect(
                    (config.t_map_editor_panel_size.x + 1) * config.px_tile_size,
                    0,
                    *(config.t_tile_vizualizer_size * config.px_tile_size).get(),
                )
            ),
            config.px_tile_size,
            sprites,
            context,
        ),
        Panels.SpriteSelection(
            display.subsurface(
                pygame.Rect(
                    (config.t_map_editor_panel_size.x + 1) * config.px_tile_size,
                    (config.t_tile_vizualizer_size.y + 1) * config.px_tile_size,
                    *(config.t_sprite_selection_panel_size * config.px_tile_size).get(),
                )
            ),
            config.px_tile_size,
            sprites,
            context,
        ),
        # Vertical separation
        Panels.EmptyPanel(
            display.subsurface(
                pygame.Rect(
                    config.t_map_editor_panel_size.x * config.px_tile_size,
                    0,
                    config.px_tile_size,
                    config.t_map_editor_panel_size.y * config.px_tile_size,
                )
            ),
            config.px_tile_size,
        ),
        # Horizontal separation
        Panels.EmptyPanel(
            display.subsurface(
                pygame.Rect(
                    (config.t_map_editor_panel_size.x + 1) * config.px_tile_size,
                    config.t_tile_vizualizer_size.y * config.px_tile_size,
                    config.t_tile_vizualizer_size.x * config.px_tile_size,
                    config.px_tile_size,
                )
            ),
            config.px_tile_size,
        ),
    ]
    return panels


def load_sprites(dir_path):
    """Load all the PNGs in the dir_path folder
    Load into a dict (keys are ints, as all sprite names should be ints)
    Sort by numerical order"""
    filepath_list = []
    for filepath in os.listdir(dir_path):
        if filepath.endswith(".png"):
            try:
                file_name = int(filepath[: filepath.rfind(".")])
            except ValueError:
                print(
                    f"[-] Sprites loader: Ignoring sprite with non integer name: {filepath}"
                )
                continue
            filepath_list.append(file_name)
    filepath_list.sort()
    # Now load the sprites themselves
    res = OrderedDict()
    print("[ ] Sprites loader: Loading sprites")
    for file_name in tqdm(filepath_list):
        res[file_name] = load_sprite(os.path.join(dir_path, str(file_name) + ".png"))
    return res


def load_sprite(filepath, resize_factor=1):
    res = pygame.image.load(filepath).convert()
    if resize_factor == 1:
        return res
    else:
        size = res.get_size()
        return pygame.transform.scale(
            res, (int(size[0] * resize_factor), int(size[1] * resize_factor))
        )


def rescale_sprites(sprites, resize_factor):
    res = {}
    for sprite_idx, sprite in sprites.items():
        res[sprite_idx] = rescale_sprite(sprite, resize_factor)
    return res


def rescale_sprite(sprite, resize_factor):
    size = sprite.get_size()
    return pygame.transform.scale(
        sprite, (int(size[0] * resize_factor), int(size[1] * resize_factor))
    )
