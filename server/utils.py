import random
import json

from Entities import *
from HelperClasses import Tile, Position


def get_map_from_json_file(map_filepath):
    map = []
    with open(map_filepath, "r") as f:
        data = f.read()
    try:
        data = json.loads(data)
    except json.decoder.JSONDecodeError as e:
        print(f"""[-] - Map loading Json module: Could not decode "{data[:100]}" """)
        return
    raw_map = data["map"]
    y_size = len(raw_map["top"])
    x_size = max(len(x) for x in raw_map["top"])
    for y_idx in range(len(raw_map["top"])):
        map_line = []
        for x_idx in range(len(raw_map["top"][y_idx])):
            top_entity_info = raw_map["top"][y_idx][x_idx]
            bottom_entity_info = raw_map["bottom"][y_idx][x_idx]
            tmp_tile = Tile()
            if bottom_entity_info:
                if bottom_entity_info[0] == "ground":
                    tmp_tile.b = Ground(Position(y_idx, x_idx), bottom_entity_info[1])
            if top_entity_info:
                # TODO: Remove the ground assignment, the map json should
                # have a ground beneath walls on its own
                tmp_tile.b = Ground(Position(y_idx, x_idx), -1)
                if top_entity_info[0] == "wall":
                    tmp_tile.t = Wall(Position(y_idx, x_idx), top_entity_info[1])
                elif top_entity_info[0] == "door":
                    tmp_tile.t = Door(Position(y_idx, x_idx), top_entity_info[1], top_entity_info[2])
            map_line.append(tmp_tile)
        map.append(map_line)
    return map, y_size, x_size


def get_map_from_txt_file(map_filepath):
    map = []
    with open(map_filepath, "r") as f:
        data = f.read().split('\n')
        data = list(filter(None, data))

    y_size = len(data)
    x_size = max(len(x) for x in data)
    print(f"[ ] - Map loader: max height detected: {y_size}")
    print(f"[ ] - Map loader: max width detected: {x_size}")
    for y_idx, line in enumerate(data):
        map_line = []
        for x_idx, char in enumerate(line):
            if char == "":
                map_line.append(Tile())
            elif char == "0":
                sprite_idx = random.randint(0, 1)
                map_line.append(Tile(
                    Ground(Position(y_idx, x_idx), sprite_idx)
                ))
            elif char == "1":
                map_line.append(Tile(
                    Ground(Position(y_idx, x_idx)),
                    Wall(Position(y_idx, x_idx))
                ))
            elif char == "2":
                map_line.append(Tile(
                    Ground(Position(y_idx, x_idx)),
                    Player(Position(y_idx, x_idx))
                ))
        map.append(map_line)
    return map, y_size, x_size
