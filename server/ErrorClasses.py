class MapError(Exception):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return f"{self.pos}"

class CollisionError(MapError):
    pass

class EmptyEntityError(MapError):
    pass
