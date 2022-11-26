import random

from Entities import *
from Dijkstra import Dijkstra
from utils import get_map_from_file
from HelperClasses import Position, Tile
from ErrorClasses import *


class MapWrapper(object):
    def __init__(self, map_filepath):
        super(MapWrapper, self).__init__()
        self.pathfinder = Dijkstra(self)
        self.sprites = [
            "ground",
            "wall",
            "player_0"
        ]
        self.map, self.y_size, self.x_size = get_map_from_file(map_filepath)
        self.map_events_deltas = []

    ########################################
    ### Map Modifiers
    # Those functions affect the entities positions
    # (both in the map and in the internal pos)
    #
    # Only top entities can be affected (added / moved / deleted)
    # as we consider bottom entities to be fixed by map creation (for now)
    #
    # Those functions also need to keep track of their effect in self.map_events_deltas,
    # in order to build the map_events_deltas to be sent to the clients
    #
    # To sum it up, each of those functions NEEDS to do 3 things:
    # - Action in the self.map object
    # - Update the entity's own position object
    # - Add the action to the self.delta list

    def add_entity(self, pos, entity):
        if entity is None:
            print(f"""[-] - Map system - Empty entity won't be added at {pos}""")
            return
        if self.is_colliding_pos(pos):
            print(f"""[-] - Map system - Could not add {entity} at {pos}, colliding""")
            raise CollisionError(pos)
        self.map[pos.y][pos.x].t = entity
        entity.pos = pos
        self.map_events_deltas.append({
            "type": "add_entity",
            "pos": str(pos),
            "entity": self.sprites.index(entity.sprite)
        })

    def delete_entity(self, pos, check_collision_before_delete=True):
        if check_collision_before_delete and not self.is_colliding_pos(pos):
            print(f"""[-] - Map system - No entity to remove at {pos}""")
            return
        entity = self.map[pos.y][pos.x].t
        self.map[pos.y][pos.x].t = None
        self.map_events_deltas.append({
            "type": "delete_entity",
            "pos": str(pos),
        })
        return entity

    def move_entity(self, from_pos, to_pos, debug=False):
        self.add_entity(to_pos, self.map[from_pos.y][from_pos.x].t)
        entity = self.delete_entity(from_pos)

    ########################################
    ### Do not affect the map

    def get(self, pos, top=True):
        if top:
            return self.map[pos.y][pos.x].t
        else:
            return self.map[pos.y][pos.x].b

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

    def get_available_position(self, retries=100):
        """ Random search """
        pos = Position(-1, -1)
        count = 0
        while count <= retries:
            pos = Position(
                random.randint(0, self.y_size),
                random.randint(0, self.x_size)
            )
            count += 1
            if not self.is_colliding_pos(pos):
                return pos
        return None

    def serialize(self):
        """ Network serialize the whole map"""
        serialized = {"size_y": self.y_size, "size_x": self.x_size, "bottom": [], "top": []}
        for y_idx in range(self.y_size):
            top_line = []
            bottom_line = []
            for x_idx in range(self.x_size):
                if self.map[y_idx][x_idx] is None:
                    print(f"[-] - Serializer error")
                top_entity = self.map[y_idx][x_idx].t
                bottom_entity = self.map[y_idx][x_idx].b
                top_line.append("" if top_entity is None else self.sprites.index(top_entity.sprite))
                bottom_line.append("" if bottom_entity is None else self.sprites.index(bottom_entity.sprite))
            serialized["top"].append(top_line)
            serialized["bottom"].append(bottom_line)
        return serialized
