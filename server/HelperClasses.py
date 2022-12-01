class Position(object):
    def __init__(self, y, x):
        super(Position, self).__init__()
        self.y = y
        self.x = x

    def __add__(self, other):
        return Position(self.y + other.y, self.x + other.x)

    def __eq__(self, other):
        if self.y == other.y and self.x == other.x:
            return True
        return False

    def __ne__(self, other):
        if self.y == other.y and self.x == other.x:
            return False
        return True

    def __repr__(self):
        return f"y:{self.y}/x:{self.x}"

    def get_json_repr(self):
        return {"x": self.x, "y": self.y}

    def get_direction(self, target):
        """ Return the direction to the target
        returns None if target isn't in one of the 4 cardinal positions
        0: Top, 1: Right, 2: Bottom, 3: Left """
        if target.x == self.x:
            if target.y == self.y - 1:
                return 0
            if target.y == self.y + 1:
                return 2
        if target.y == self.y:
            if target.x == self.x - 1:
                return 3
            if target.x == self.x + 1:
                return 1
        return None


class Tile(object):
    def __init__(self, bottomObject=None, topObject=None):
        super(Tile, self).__init__()
        self.t = topObject
        self.b = bottomObject

    def __repr__(self):
        return f"Tile: [{self.t} / {self.b}]"
