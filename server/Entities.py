import random
import collections

from ErrorClasses import ImpossibleMoveError
""" For now all Entities have a position, but only the living entities get an id
"""

class Entity(object):
    def __init__(self, pos):
        self.pos = pos
        self.collider = False
        self.sprite_idx = None

    def __repr__(self):
        # Remove the <class Entities. and the >
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
        self.collider = True
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
    def __init__(self, id, pos, name, sprite_idx=3, speed=1):
        super().__init__(id, pos, speed, sprite_idx)
        self.collider = True
        self.name = name
        self.inventory = {}
        self.pets = []

class Pet(LivingEntity):
    def __init__(self, id, pos, owner, sprite_idx=7, speed=1):
        super().__init__(id, pos, speed, sprite_idx)
        self.collider = True
        self.owner = owner
        self.requested_distance_from_owner = 3

    def do_turn(self, map_wrapper, living_entities):
        if self.pos.get_distance_from(self.owner.pos) == self.requested_distance_from_owner:
            return
        tiles = map_wrapper.pathfinder.get_tiles_at_distance_from(
            self.owner.pos, self.requested_distance_from_owner
        )
        target_pos = self.pos.get_closest(tiles)
        next_move = map_wrapper.pathfinder.get_next_move(self, target_pos)
        if next_move is not None:
            done_move = map_wrapper.move_entity(self.pos, next_move)
