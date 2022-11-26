class Entity(object):
    def __init__(self, pos):
        self.pos = pos
        self.collider = False
        self.sprite = None

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
    def __init__(self, pos, speed):
        super().__init__(pos)
        self.speed = speed
        self.turn_idx = 0

class Player(LivingEntity):
    def __init__(self, pos, name, id, sprite="player_0", speed=1):
        super().__init__(pos, speed)
        self.collider = True
        self.name = name
        self.id = id
        self.sprite = sprite
        self.inventory = {}

class Pet(LivingEntity):
    def __init__(self, pos, owner_id, sprite="player_0", speed=1):
        super().__init__(pos, speed)
        self.collider = True
        self.owner_id = owner_id
        self.sprite = sprite
        ### Pathfinding
        self.target_path = None
        self.last_pathfinding_turn_idx = -1
        self.pathfinding_turns_delta = 5

    def do_turn(self, map_wrapper, players, living_entities):
        if self.target_path is None or self.turn_idx - self.last_pathfinding_turn_idx > self.pathfinding_turns_delta:
            owner_pos = players[self.owner_id].pos
            target_pos = owner_pos  # TODO: Add variation
            self.target_path = map_wrapper.pathfinder.get_shortest_path(
                from_pos=self.pos, target_pos=target_pos
            )
            self.target_path.pop(-1)

            self.last_pathfinding_turn_idx = self.turn_idx

        if len(self.target_path) > 0:
            map_wrapper.move_entity(self.pos, self.target_path[0].pos)
            # print(f"moved pet from {self.pos} to {self.target_path[0].pos}")
            self.target_path.pop(0)
        self.turn_idx += 1
