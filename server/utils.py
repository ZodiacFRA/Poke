class Position(object):
    def __init__(self, y, x):
        super(Position, self).__init__()
        self.y = y
        self.x = x

    def __add__(self, other):
        return Position(self.y + other.y, self.x + other.x)

    def __repr__(self):
        return f"y:{self.y}/x:{self.x}"
