class MapError(Exception):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return f"{self.pos}"

class CollisionError(MapError):
    pass

class ImpossibleMoveError(MapError):
    def __init__(self, from_pos, to_pos):
        self.from_pos = from_pos
        self.to_pos = to_pos

    def __str__(self):
        return f"{self.from_pos} to {self.to_pos}"
