import os
import json

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

def rescale_sprites(sprites, resize_factor):
    res = {}
    for sprite_idx, sprite in sprites.items():
        res[sprite_idx] = rescale_sprite(sprite, resize_factor)
    return res

def rescale_sprite(sprite, resize_factor):
        size = sprite.get_size()
        return pygame.transform.scale(
            sprite,
            (int(size[0]*resize_factor), int(size[1]*resize_factor))
        )

def init_map_layout(map_size):
    res = []
    for y in range(map_size.y):
        line = []
        for x in range(map_size.x):
            line.append(None)
        res.append(line)
    return res

def serialize(top_layer, bottom_layer, map_size):
    res = {"map": {"top": init_map_layout(map_size), "bottom": init_map_layout(map_size)}}
    for y_idx in range(map_size.y):
        for x_idx in range(map_size.x):
            top_entity = []
            top_sprite_idx = top_layer[y_idx][x_idx]
            if top_sprite_idx is not None:
                top_entity = ["ground", top_sprite_idx]
            res["map"]["top"][y_idx][x_idx] = top_entity

            bottom_entity = []
            bottom_sprite_idx = bottom_layer[y_idx][x_idx]
            if bottom_sprite_idx is not None:
                bottom_entity = ["ground", bottom_sprite_idx]
            res["map"]["bottom"][y_idx][x_idx] = bottom_entity

    with open("./map.json", 'w') as f:
        f.write(json.dumps(res))
    print("[+] - Serializing done, wrote to ./map.json")


def get_int_idx(elem):
    elem = int(elem)
    return elem
