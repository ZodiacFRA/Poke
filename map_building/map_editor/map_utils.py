import json
import copy
from pprint import pprint

from Vector2 import Vector2


def load_map_from_json(json_path, crop=False):
    print("[ ] - Map loader: Loading map from", json_path)
    with open(json_path, "r") as f:
        data = f.read()
    data = json.loads(data)["map"]
    map_size = Vector2(max(len(x) for x in data["top"]), len(data["top"]))
    if crop:
        print(f"[ ] - Map loader: Cropping from {map_size} to ", end="")
        data = crop_map(data, map_size)
        map_size = Vector2(max(len(x) for x in data["top"]), len(data["top"]))
        print(map_size)
    return data, map_size


def crop_map(data, map_size):
    # TODO: Debug
    """Remove all border empty rows and columns"""
    empty_row_idx_list = []
    # Detect new columns borders
    left_border = map_size.x
    right_border = 0
    for y in range(len(data["top"])):
        first_not_none_idx = get_first_non_none_idx(data["top"][y])
        last_not_none_idx = get_first_non_none_idx(data["top"][y], reversed=True)
        if first_not_none_idx is None and last_not_none_idx is None:  # Empty row
            empty_row_idx_list.append(y)
            continue
        if first_not_none_idx < left_border:
            left_border = first_not_none_idx
        if last_not_none_idx > right_border:
            right_border = last_not_none_idx
    # Detect new rows borders
    top_border = get_last_consecutive_idx(empty_row_idx_list) + 1
    bottom_border = get_last_consecutive_idx(empty_row_idx_list, reversed=True) - 1
    # Crop
    tmp = {"top": [], "bottom": []}
    for y in range(top_border, bottom_border + 1):
        top_line = []
        bottom_line = []
        for x in range(left_border, right_border + 1):
            top_line.append(data["top"][y][x])
            bottom_line.append(data["bottom"][y][x])
        tmp["top"].append(top_line)
        tmp["bottom"].append(bottom_line)
    return tmp


def get_last_consecutive_idx(empty_row_idx_list, reversed=False):
    empty_row_idx_list = copy.copy(empty_row_idx_list)
    if reversed:
        empty_row_idx_list.reverse()
        last_empty_idx = empty_row_idx_list[0] + 1
        for empty_row_idx in empty_row_idx_list:
            if last_empty_idx - 1 != empty_row_idx:
                return last_empty_idx
            last_empty_idx = empty_row_idx
    else:
        last_empty_idx = -1
        for empty_row_idx in empty_row_idx_list:
            if last_empty_idx + 1 != empty_row_idx:
                return last_empty_idx
            last_empty_idx = empty_row_idx


def get_first_non_none_idx(data, reversed=False):
    data = copy.copy(data)
    if reversed:
        data.reverse()
    for i, elem in enumerate(data):
        if elem:
            return i
    return None
