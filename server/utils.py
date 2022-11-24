
class Position(object):
    def __init__(self, y, x):
        super(Position, self).__init__()
        self.y = y
        self.x = x

    def __repr__(self):
        return f"y:{self.y}/x:{self.x}"
