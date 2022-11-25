import random

from Entities import *
from utils import Position, Tile


class MapWrapper(object):
    def __init__(self, map_filepath):
        super(MapWrapper, self).__init__()
        self.sprites = [
            "ground",
            "wall",
            "player_0"
        ]
        self.map = []
        self.y_size = -1
        self.x_size = -1
        self.load_map(map_filepath)

    def add_player(self, player):
        self.map[player.pos.y][player.pos.x].t = player
        print(f"Player spawned at position {player.pos}")

    def remove_entity(self, pos):
        """ Only removes the top entity, as we don't want any holes in the ground
        Use the swap() method to change bottom entities """
        tmp = self.map[pos.y][pos.x]
        self.map[pos.y][pos.x] = ""
        return tmp

    def get(self, pos):
        return self.map[pos.y][pos.x]

    def move(self, from_pos, to_pos, debug=False):
        if debug:
            print(f"""[ ] - Before moving - from {from_pos} ({self.map_wrapper.get(from_pos)}) to {to_pos}  ({self.map_wrapper.get(to_pos)})""")
        self.map[to_pos.y][to_pos.x].t = self.map[from_pos.y][from_pos.x].t
        self.map[from_pos.y][from_pos.x].t = None
        if debug:
            print(f"""[ ] - After moving - from {from_pos} ({self.map_wrapper.get(from_pos)}) to {to_pos}  ({self.map_wrapper.get(to_pos)})""")

    def is_colliding_pos(self, pos):
        # OOB -> colliding
        if pos.x < 0 or pos.x >= self.x_size or pos.y < 0 or pos.y >= self.y_size:
            return True
        # No Floor -> colliding
        if self.map[pos.y][pos.x].b is None:
            return True
        # Floor only -> Not colliding
        if self.map[pos.y][pos.x].t is None:
            return False
        # Floor and Non-colliding entity -> Not colliding
        if not self.map[pos.y][pos.x].t.collider:
            return False
        # Floor and Colliding entity -> colliding
        return True

    def load_map(self, map_filepath):
        with open(map_filepath, "r") as f:
            data = f.read().split('\n')
            data = list(filter(None, data))

        self.y_size = len(data)
        self.x_size = max(len(x) for x in data)
        print(f"[ ] - Map loader: max height detected: {self.y_size}")
        print(f"[ ] - Map loader: max width detected: {self.x_size}")
        for y_idx, line in enumerate(data):
            map_line = []
            for x_idx, char in enumerate(line):
                if char == " ":
                    map_line.append(Tile())
                elif char == "0":
                    map_line.append(Tile(Ground()))
                elif char == "1":
                    map_line.append(Tile(Ground(), Wall()))
                elif char == "2":
                    map_line.append(Tile(Ground(), Player()))
            self.map.append(map_line)

    def serialize(self):
        """ Network serialize the whole map"""
        serialized = {"bottom": [], "top": []}
        for y_idx in range(self.y_size):
            top_line = []
            bottom_line = []
            for x_idx in range(self.x_size):
                top_entity = self.map[y_idx][x_idx].t
                bottom_entity = self.map[y_idx][x_idx].b
                top_line.append("" if top_entity is None else self.sprites.index(top_entity.sprite))
                bottom_line.append("" if bottom_entity is None else self.sprites.index(bottom_entity.sprite))
            serialized["top"].append(top_line)
            serialized["bottom"].append(bottom_line)
        return serialized
