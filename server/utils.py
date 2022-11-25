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


class Tile(object):
    def __init__(self, bottomObject=None, topObject=None):
        super(Tile, self).__init__()
        self.t = topObject
        self.b = bottomObject

    def __repr__(self):
        tmp = "bottom entity: "
        if self.b is not None:
            tmp += type(bottom)
        else:
            tmp += "None"
        tmp += " top entity: "
        if self.t is not None:
            tmp += type(top)
        else:
            tmp += "None"
        return tmp


def save_gamestate_to_file(filepath, gamestate):
    pass
