import json
import copy
from pprint import pprint

from Vector2 import Vector2


def load_map_from_json(json_path, crop=False):
    print("[ ] - Map loader: Loading map from", json_path)
    with open(json_path, "r") as f:
        data = f.read()
    map = json.loads(data)["map"]
    map_size = Vector2(max(len(x) for x in map["top"]), len(map["top"]))
    if crop:
        # print(f"[ ] - Map loader: Cropping from {map_size} to ", end="")
        map = crop_map(map, map_size)
        map_size = Vector2(max(len(x) for x in map["top"]), len(map["top"]))
        # print(map_size)
    return map, map_size


def crop_map(map, map_size):
    """Remove all border empty rows and columns"""
    top_left, bottom_right = detect_map_edges(map, map_size)
    # Now crop
    tmp = {"top": [], "bottom": []}
    for y in range(top_left.y, bottom_right.y + 1):
        top_line = []
        bottom_line = []
        for x in range(top_left.x, bottom_right.x + 1):
            top_line.append(map["top"][y][x])
            bottom_line.append(map["bottom"][y][x])
        tmp["top"].append(top_line)
        tmp["bottom"].append(bottom_line)
    return tmp


def detect_map_edges(map, map_size):
    """Borders are in the map! (if top border = 1, the row at idx 1 will contain tiles)"""
    # Detect top border first
    top_border = 0
    for y in range(map_size.y):
        if not is_empty_row(map, y):
            top_border = y
            break
    # Then the bottom border
    bottom_border = map_size.y - 1
    for y in range(bottom_border, -1, -1):
        if not is_empty_row(map, y):
            bottom_border = y
            break
    # Now detect the left border
    left_border = 0
    for x in range(map_size.x):
        if not is_empty_column(map, map_size, x):
            left_border = x
            break
    # Then the right border
    right_border = map_size.x - 1
    for x in range(right_border, -1, -1):
        if not is_empty_column(map, map_size, x):
            right_border = x
            break
    return Vector2(left_border, top_border), Vector2(right_border, bottom_border)


def is_empty_row(map, row_idx):
    return not any(map["top"][row_idx]) and not any(map["bottom"][row_idx])


def is_empty_column(map, map_size, col_idx):
    col_top = [map["top"][y][col_idx] for y in range(map_size.y)]
    col_bottom = [map["bottom"][y][col_idx] for y in range(map_size.y)]
    return not any(col_top) and not any(col_bottom)
