import random

from Entities import *
from utils import Position


class Tile(object):
    def __init__(self, bottomObject, topObject=None):
        super(Tile, self).__init__()
        self.t = topObject
        self.b = bottomObject

class Map(object):
    def __init__(self, y_size, x_size):
        super(Map, self).__init__()
        self.sprites = [
            "ground",
            "wall",
            "player_0"
        ]
        self.y_size = y_size
        self.x_size = x_size
        self.map = []
        for y_idx in range(self.y_size):
            line = []
            for x_idx in range(self.x_size):
                line.append(Tile(Ground()))
            self.map.append(line)
        self.generate_map()

    def add_player(self, player):
        tile_top = self.map[player.pos.y][player.pos.x].t
        if tile_top is not None:
            print(f"Player spawn collision with {type(tile_top)} at position {player.pos}")
        else:
            self.map[player.pos.y][player.pos.x].t = player
            print(f"Player spawned at position {player.pos}")

    def remove_entity(self, pos):
        tmp = self.map[pos.y][pos.x]
        self.map[pos.y][pos.x] = ""
        return tmp

    def generate_map(self):
        for tmp in range(20):
            self.map[random.randint(0, self.y_size - 1)][random.randint(0, self.x_size - 1)].t = Wall()

    def move(self, from_pos, to_pos, debug=False):
        if debug:
            self.print_map_pos("[ ] - before move - from", from_pos)
            self.print_map_pos("[ ] - before move - to", to_pos)
        self.map[to_pos.y][to_pos.x].t = self.map[from_pos.y][from_pos.x].t
        self.map[from_pos.y][from_pos.x].t = None
        if debug:
            self.print_map_pos("[ ] - after move - from", from_pos)
            self.print_map_pos("[ ] - after move - to", to_pos)

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

    def serialize(self):
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

    def print_map_pos(self, msg, pos):
        top = self.map[pos.y][pos.x].t
        bottom = self.map[pos.y][pos.x].b
        if top is not None:
            print(f"{msg} {pos}: bottom={type(bottom)} top={type(top)}")
        else:
            print(f"{msg} {pos}: bottom={type(bottom)} top=None")
