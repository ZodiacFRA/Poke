import random

SPRITES = [
    "ground",
    "wall",
    "player_0"
]

class Entity(object):
    def __init__(self):
        super(Entity, self).__init__()
        self.collider = False
        self.sprite = None

class Ground(Entity):
    def __init__(self, sprite="ground"):
        super(Entity, self).__init__()
        self.sprite = sprite

class Wall(Entity):
    def __init__(self, sprite="wall"):
        super(Entity, self).__init__()
        self.collider = True
        self.sprite = sprite

class Player(Entity):
    def __init__(self, name, sprite="player_0"):
        super(Entity, self).__init__()
        self.sprite = sprite

class Tile(object):
    def __init__(self, bottomObject, topObject=None):
        super(Tile, self).__init__()
        self.t = topObject
        self.b = bottomObject

class Map(object):
    def __init__(self, y_size, x_size):
        super(Map, self).__init__()
        self.y_size = y_size
        self.x_size = x_size
        self.map = []
        for y_idx in range(self.y_size):
            line = []
            for x_idx in range(self.x_size):
                line.append(Tile(Ground()))
            self.map.append(line)

        ################ Random wall fill (TMP)
        for tmp in range(20):
            self.map[random.randint(0, self.y_size - 1)][random.randint(0, self.x_size - 1)].t = Wall()

        self.map[1][1].t = Player("jbbbb")

    def serialize(self):
        serialized = {"bottom": [], "top": []}
        for y_idx in range(self.y_size):
            top_line = []
            bottom_line = []
            for x_idx in range(self.x_size):
                top_entity = self.map[y_idx][x_idx].t
                bottom_entity = self.map[y_idx][x_idx].b
                top_line.append("" if top_entity is None else top_entity.sprite)
                bottom_line.append("" if bottom_entity is None else bottom_entity.sprite)
            serialized["top"].append(top_line)
            serialized["bottom"].append(bottom_line)
        return serialized
