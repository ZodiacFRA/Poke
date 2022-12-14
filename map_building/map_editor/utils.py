import os

import pygame


def load_sprites(sprites_dir):
    res = {}
    for file in os.listdir(sprites_dir):
        if file.endswith(".png"):
            sprite_path = os.path.join(sprites_dir, file)
            res[file[:file.find('.')]] = load_sprite(sprite_path)
    return res

def load_sprite(filepath, resize_factor=1):
    res = pygame.image.load(filepath).convert_alpha()
    if resize_factor == 1:
        return res
    else:
        size = res.get_size()
        # create a 2x bigger image than self.image
        return pygame.transform.scale(
            res,
            (int(size[0]*resize_factor), int(size[1]*resize_factor))
        )
