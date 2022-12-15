import os
import json

import pygame

from Position import Position


def get_layers_from_json_file(map_filepath):
    print("[ ] - Map loader: Loading map from", map_filepath)
    with open(map_filepath, "r") as f:
        data = f.read()
    try:
        data = json.loads(data)
    except json.decoder.JSONDecodeError as e:
        print(f"""[-] - Map loading Json module: Could not decode "{data[:100]}" """)
        return
    top = []
    bottom = []
    raw_map = data["map"]
    y_size = len(raw_map["top"])
    x_size = max(len(x) for x in raw_map["top"])
    for y_idx in range(len(raw_map["top"])):
        top_line = []
        bottom_line = []
        for x_idx in range(len(raw_map["top"][y_idx])):
            top_entity_info = raw_map["top"][y_idx][x_idx]
            bottom_entity_info = raw_map["bottom"][y_idx][x_idx]
            if bottom_entity_info:
                bottom_line.append(str(bottom_entity_info[1]))
            else:
                bottom_line.append(None)
            if top_entity_info:
                top_line.append(str(top_entity_info[1]))
            else:
                top_line.append(None)
        top.append(top_line)
        bottom.append(bottom_line)
    return top, bottom, Position(y_size, x_size)

def load_sprites(sprites_dir):
    res = {}
    for file in os.listdir(sprites_dir):
        if file.endswith(".png"):
            sprite_path = os.path.join(sprites_dir, file)
            res[file[:file.find('.')]] = load_sprite(sprite_path)
    return res

def load_sprite(filepath, resize_factor=1):
    res = pygame.image.load(filepath).convert()
    if resize_factor == 1:
        return res
    else:
        size = res.get_size()
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
    layer = []
    for y in range(map_size.y):
        line = []
        for x in range(map_size.x):
            line.append(None)
        layer.append(line)
    return layer

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
