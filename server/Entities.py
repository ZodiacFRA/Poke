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

    def do_turn(self, map_wrapper, living_entities):
        pass

class Player(LivingEntity):
    def __init__(self, id, pos, name, sprite="player", speed=1):
        super().__init__(id, pos, speed, sprite)
        self.collider = True
        self.name = name
        self.inventory = {}

class Pet(LivingEntity):
    def __init__(self, id, pos, owner_id, sprite="lava_0", speed=1):
        super().__init__(id, pos, speed, sprite)
        self.collider = True
        self.owner_id = owner_id

    def do_turn(self, map_wrapper, living_entities):
        owner_pos = living_entities[self.owner_id].pos
        target_pos = owner_pos  # TODO: Add variation
        next_move = map_wrapper.pathfinder.get_next_move(self, target_pos)
        # print("next move", next_move)
        if next_move is not None:
            map_wrapper.move_entity(self.pos, next_move)
