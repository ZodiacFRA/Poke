import random

import Globals
from Entities import *
from Pathfinder import Pathfinder
from utils import get_map_from_json_file
from HelperClasses import Position, Tile
from ErrorClasses import *


class MapWrapper(object):
    def __init__(self, map_filepath):
        super(MapWrapper, self).__init__()
        self.pathfinder = Pathfinder(self)
        self.map, self.y_size, self.x_size = get_map_from_json_file(map_filepath)
        self.map_events = []

    ########################################
    ### Map Modifiers
    # Those functions affect the entities positions
    # (both in the map and in the internal pos)
    #
    # Only top entities can be affected (added / moved / deleted)
    # as we consider bottom entities to be fixed by map creation (for now)
    #
    # Those functions also need to keep track of their effect in self.map_events,
    # in order to build the map_events to be sent to the clients
    #
    # To sum it up, each of those functions NEEDS to do 3 things:
    # - Action in the self.map object
    # - Update the entity's own position object OR its direction
    # - Add the action to the self.map_events list (will be sent through network)

    def add_entity(self, pos, entity, is_move=False):
        if entity is None:
            print(f"""[-] - Map system - Empty entity won't be added at {pos}""")
            return
        if self.is_colliding_pos(pos):
            raise CollisionError(pos)
        self.map[pos.y][pos.x].t = entity
        entity.pos = pos
        if not is_move:
            self.map_events.append({
                "type": "add_entity",
                "pos": pos.get_json_repr(),
                "entity": entity.get_sprite_idx()
            })

    def delete_entity(self, pos, is_move=False, check_collision_before_delete=True):
        if check_collision_before_delete and not self.is_colliding_pos(pos):
            print(f"""[-] - Map system - No entity to remove at {pos}""")
            return
        entity = self.map[pos.y][pos.x].t
        self.map[pos.y][pos.x].t = None
        if not is_move:
            self.map_events.append({
                "type": "delete_entity",
                "pos": pos.get_json_repr()
            })
        return entity

    def move_entity(self, from_pos, to_pos, teleported=False, debug=False):
        """
        If direction != -1: must check direction before moving, return flag
        will change based on [
            impossible move -> False,
            changed direction (no pos change) -> 1,
            moved -> 2
        ]
        No need to check for collisions before calling this method
        as it will be checked by add_entity()
        Returns True if move is successful
        """
        entity_from = self.map[from_pos.y][from_pos.x].t
        move_direction = from_pos.get_direction(to_pos)
        if move_direction is None:  # Invalid move (not cardinal)
            print(f"""[ ] - Map system - Invalid move {from_pos} to {to_pos}""")
            return False
        # Entity needs to change direction before moving, return 1
        if entity_from.direction != -1 and move_direction != entity_from.direction:
            entity_from.direction = move_direction
            self.map_events.append({
                "type": "update_entity",
                "pos": from_pos.get_json_repr(),
                "entity": entity_from.get_sprite_idx()
            })
            return 1
        else:
            try:
                self.add_entity(to_pos, self.map[from_pos.y][from_pos.x].t, True)
            except CollisionError:
                if debug:
                    print(f"""[ ] - Map system - Could not move {self.map[from_pos.y][from_pos.x].t} to {to_pos}, colliding""")
                return False
            entity = self.delete_entity(from_pos, True)
            self.map_events.append({
                "type": "move_entity",
                "from_pos": from_pos.get_json_repr(),
                "to_pos": to_pos.get_json_repr()
            })
            # Check if the tile we just moved on is a door, if so teleport if possible
            if not teleported and type(self.map[to_pos.y][to_pos.x].t) is Door:
                return self.move_entity(
                    to_pos,
                    self.map[to_pos.y][to_pos.x].t.to_pos,
                    teleported=True
                )
            return 2

    ########################################
    ### Do not affect the map

    def get(self, pos, top_entity_only=True):
        try:
            if top_entity_only:
                return self.map[pos.y][pos.x].t
            else:
                return self.map[pos.y][pos.x].b
        except IndexError:
            print(f"[-] - Map wrapper: Invalid position requested: {pos}")
            return None

    def get_tile_in_front(self, pos, direction, top_entity_only=True):
        return self.get(pos + Globals.deltas[direction], top_entity_only)

    def is_colliding_pos(self, pos, collide_treshold=99999):
        # OOB -> colliding
        if pos.x < 0 or pos.x >= self.x_size or pos.y < 0 or pos.y >= self.y_size:
            return True
        try:
            # No Floor -> colliding
            if self.map[pos.y][pos.x].b is None:
                return True
            # Floor only -> Not colliding
            if self.map[pos.y][pos.x].t is None:
                return False
            # Floor and Non-colliding entity -> Not colliding
            if self.map[pos.y][pos.x].t.collider > collide_treshold:
                return False
        except IndexError:  # For non square maps, index won't exist, return True
            return True
        # Floor and Colliding entity -> colliding
        return True

    def go_towards_target_pos(self, entity, target_pos):
        next_move = self.pathfinder.get_next_move(entity, target_pos)
        if next_move is not None:
            if self.move_entity(entity.pos, next_move) == 2:  # If move successful
                pass  # TODO: if the move has not been done prevent the pathdfinder
                # class from popping this move

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
            for x_idx in range(len(self.map[y_idx])):
                if self.map[y_idx][x_idx] is None:
                    print(f"[-] - Serializer error")
                top_entity = self.map[y_idx][x_idx].t
                bottom_entity = self.map[y_idx][x_idx].b
                top_line.append(-1 if top_entity is None else top_entity.get_sprite_idx())
                bottom_line.append(-1 if bottom_entity is None else bottom_entity.get_sprite_idx())
            serialized["top"].append(top_line)
            serialized["bottom"].append(bottom_line)
        return serialized

    def display_ascii(self):
        """ Only displaying the top entity """
        for y_idx in range(self.y_size):
            for x_idx in range(self.x_size):
                print(f"{str(self.get(Position(y_idx, x_idx)))}", end="")
            print()
