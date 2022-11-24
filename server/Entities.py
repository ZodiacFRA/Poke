class Entity(object):
    def __init__(self):
        self.collider = False
        self.sprite = None

##############################################

class Ground(Entity):
    def __init__(self, sprite="ground"):
        self.sprite = sprite

class Wall(Entity):
    def __init__(self, sprite="wall"):
        self.collider = True
        self.sprite = sprite

##############################################

class LivingEntity(Entity):
    def __init__(self, pos, speed):
        self.pos = pos
        self.speed = speed

class Player(LivingEntity):
    def __init__(self, pos, name, id, sprite="player_0", speed=1):
        super().__init__(pos, speed)
        self.collider = True
        self.name = name
        self.id = id
        self.sprite = sprite
        self.inventory = {}
