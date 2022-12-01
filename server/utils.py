from Entities import *
from HelperClasses import Tile, Position


def get_map_from_file(map_filepath):
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
                map_line.append(Tile(
                    Ground(Position(y_idx, x_idx))
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
