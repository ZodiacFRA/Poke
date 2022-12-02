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
    def __init__(self, pos, sprite_idx=1):
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

    def do_turn(self, map_wrapper, living_entities):
        pass

class Player(LivingEntity):
    def __init__(self, id, pos, name, sprite_idx=2, speed=1):
        super().__init__(id, pos, speed, sprite_idx)
        self.collider = True
        self.name = name
        self.inventory = {}
        self.pets = []

    def get_sprite_idx(self):
        print("player", self.sprite_idx + self.direction)
        return self.sprite_idx + self.direction

class Pet(LivingEntity):
    def __init__(self, id, pos, owner, sprite_idx=4, speed=1):
        super().__init__(id, pos, speed, sprite_idx)
        self.collider = True
        self.owner = owner
        self.owner_previous_positions = collections.deque(maxlen=4)
        self.distance_from_owner = 2
        self.moves_nbr = 0

    def do_turn(self, map_wrapper, living_entities):
        old_pos = self.pos
        if self.owner_previous_positions:
            idx = min(len(self.owner_previous_positions) - 1, len(self.owner_previous_positions) - self.distance_from_owner)
            target_pos = self.owner_previous_positions[idx]
        else:
            target_pos = self.owner.pos
            self.owner_previous_positions.append(self.owner.pos)
        if self.owner.pos != self.owner_previous_positions[-1]:
            self.owner_previous_positions.append(self.owner.pos)
        if self.pos != target_pos:
            next_move = map_wrapper.pathfinder.get_next_move(self, target_pos, 0)
            if next_move is not None:
                done_move = map_wrapper.move_entity(self.pos, next_move)
                if done_move:
                    self.moves_nbr += 1
                    direction = old_pos.get_direction(next_move)
                    if direction is None:
                        # raise ImpossibleMoveError(old_pos, next_move)
                        print("[-] - TODO: Fix Pet impossible move")
                    self.direction = direction
