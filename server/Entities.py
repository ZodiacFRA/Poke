import random
import collections
from operator import attrgetter

from ErrorClasses import ImpossibleMoveError
""" For now all Entities have a position, but only the living entities get an id
"""

class Entity(object):
    def __init__(self, pos):
        self.pos = pos
        self.collider = 0
        self.sprite_idx = None
        self.direction = -1

    def __repr__(self):
        # Remove the "<class Entities." and the " >"
        return f"{str(type(self))[17:-2]} - {self.pos}"

    def get_sprite_idx(self):
        return self.sprite_idx

##############################################

class Ground(Entity):
    def __init__(self, pos, sprite_idx=0):
        super().__init__(pos)
        self.sprite_idx = sprite_idx

class Wall(Entity):
    def __init__(self, pos, sprite_idx=2):
        super().__init__(pos)
        self.collider = 1
        self.sprite_idx = sprite_idx

class Door(Entity):
    def __init__(self, pos, to_pos, sprite_idx=3):
        super().__init__(pos)
        self.to_pos = to_pos
        self.collider = 0
        self.sprite_idx = sprite_idx

##############################################

class LivingEntity(Entity):
    def __init__(self, id, pos, speed, sprite_idx):
        super().__init__(pos)
        self.id = id
        self.speed = speed
        self.turn_idx = 0
        self.sprite_idx = sprite_idx
        self.direction = 0
        # 0: Top, 1: Right, 2: Bottom, 3: Left

    def get_sprite_idx(self):
        return self.sprite_idx + self.direction

    def do_turn(self, map_wrapper, living_entities):
        pass

class Player(LivingEntity):
    def __init__(self, id, pos, name, sprite_idx=1000, speed=1):
        super().__init__(id, pos, speed, sprite_idx)
        self.collider = 2
        self.name = name
        self.inventory = {}
        self.pokedex = []

class Pet(LivingEntity):
    def __init__(self, id, pos, owner, sprite_idx=1004, speed=1):
        super().__init__(id, pos, speed, sprite_idx)
        self.collider = 2
        self.owner = owner
        self.requested_distance_from_owner = 3

    def do_turn(self, map_wrapper, living_entities):
        positions = map_wrapper.pathfinder.get_positions_at_distance_from_position(
            self.owner.pos, self.requested_distance_from_owner
        )
        target_pos = self.get_tile_behind(positions)
        # if target_pos == self.pos:
            # return
        if not target_pos:
            target_pos = self.pos.get_closest(positions)
        if target_pos:
            map_wrapper.go_towards_target_pos(self, target_pos)

    def get_tile_behind(self, positions):
        player_behind_direction = (self.owner.direction + 2) % 4
        if player_behind_direction == 0:
            res = min(positions, key=attrgetter('y'))
        elif player_behind_direction == 1:
            res = max(positions, key=attrgetter('x'))
        elif player_behind_direction == 2:
            res = max(positions, key=attrgetter('y'))
        elif player_behind_direction == 3:
            res = min(positions, key=attrgetter('x'))
        return res
