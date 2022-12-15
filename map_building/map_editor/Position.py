class Position(object):
    def __init__(self, y, x):
        super(Position, self).__init__()
        self.y = y
        self.x = x

    def __floordiv__(self, other):
        return Position(self.y // other, self.x // other)

    def __mul__(self, other):
        return Position(self.y * other, self.x * other)

    def __add__(self, other):
        return Position(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return Position(self.y - other.y, self.x - other.x)

    def __eq__(self, other):
        if self.y == other.y and self.x == other.x:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"y:{self.y}/x:{self.x}"

    def get_json_repr(self):
        return {"x": self.x, "y": self.y}

    def get_tuple(self):
        return self.y, self.x

    def get_cardinal_direction(self, target):
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

    def get_direction(self, target):
        """ Return the direction to the target
        0: Top, 1: Right, 2: Bottom, 3: Left """
        if target.x == self.x:
            if target.y == self.y:
                return 0
            if target.y == self.y:
                return 2
        if target.y == self.y:
            if target.x == self.x:
                return 3
            if target.x == self.x:
                return 1
        return None

    def get_distance_from(self, other):
        return abs(self.y - other.y) + abs(self.x - other.x)

    def get_closest(self, positions):
        min_distance = 999999
        min_pos = None
        for pos in positions:
            distance = self.get_distance_from(pos)
            if distance < min_distance:
                min_distance = distance
                min_pos = pos
        return min_pos
