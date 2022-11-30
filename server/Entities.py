import random
import collections
""" For now all Entities have a position, but only the living entities get an id
"""

class Entity(object):
    def __init__(self, pos):
        self.pos = pos
        self.collider = False
        self.sprite = None

    def __repr__(self):
        # Remove the <class Entities. and the >
        return f"{str(type(self))[17:-2]} - {self.pos}"

##############################################

class Ground(Entity):
    def __init__(self, pos, sprite="ground"):
        super().__init__(pos)
        self.sprite = sprite

class Wall(Entity):
    def __init__(self, pos, sprite="wall"):
        super().__init__(pos)
        self.collider = True
        self.sprite = sprite

##############################################

class LivingEntity(Entity):
    def __init__(self, id, pos, speed, sprite):
        super().__init__(pos)
        self.id = id
        self.speed = speed
        self.turn_idx = 0
        self.sprite = sprite
        self.direction = 0
        # 0: Top, 1: Right, 2: Bottom, 3: Left

    def do_turn(self, map_wrapper, living_entities):
        pass

class Player(LivingEntity):
    def __init__(self, id, pos, name, sprite="player", speed=1):
        super().__init__(id, pos, speed, sprite)
        self.collider = True
        self.name = name
        self.inventory = {}
        self.pets = []

class Pet(LivingEntity):
    def __init__(self, id, pos, owner, sprite="lava_0", speed=1):
        super().__init__(id, pos, speed, sprite)
        self.collider = True
        self.owner = owner
        self.owner_previous_positions = collections.deque(maxlen=4)
        self.distance_from_owner = 1
        self.distance_change_turns_duration = 10
        self.moves_nbr = 0

    def do_turn(self, map_wrapper, living_entities):
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
                    if self.moves_nbr > self.distance_change_turns_duration:
                        self.moves_nbr = 0
                        self.distance_change_turns_duration = random.randint(5, 20)
                        self.distance_from_owner = random.randint(1, len(self.owner_previous_positions))
                        # print(f"distance change to: {self.distance_from_owner}, will change in {self.distance_change_turns_duration}")  # DEBUG:
