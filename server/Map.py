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

    def generate_map(self):
        for tmp in range(20):
            self.map[random.randint(0, self.y_size - 1)][random.randint(0, self.x_size - 1)].t = Wall()

    def move(self, from_pos, to_pos):
        self.print_map_pos(from_pos)
        self.print_map_pos(to_pos)
        self.map[to_pos.y][to_pos.x].t = self.map[from_pos.y][from_pos.x].t
        self.map[from_pos.y][from_pos.x].t = None
        # print("moved from ", from_pos, " to", to_pos)
        self.print_map_pos(from_pos)
        self.print_map_pos(to_pos)

    def is_colliding_pos(self, pos):
        if pos.x < 0 or pos.x >= self.x_size or pos.y < 0 or pos.y >= self.y_size:
            return True
        if self.map[pos.y][pos.x].t is None:
            return False
        if self.map[pos.y][pos.x].t is not None and not self.map[pos.y][pos.x].t.collider:
            return False
        return True

    def print_map_pos(self, pos):
        top = self.map[pos.y][pos.x].t
        bottom = self.map[pos.y][pos.x].b
        if top is not None:
            print(f"{pos}: bottom={type(bottom)} top={type(top)}")
        else:
            print(f"{pos}: bottom={type(bottom)} top=None")

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
