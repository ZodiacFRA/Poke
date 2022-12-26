class Vector2(object):
    def __init__(self, x=0, y=0):
        super(Vector2, self).__init__()
        self.x = x
        self.y = y
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError(
                f"Vector2: Could not create with non integers args: x={type(x)}, y={type(y)}"
            )

    def __floordiv__(self, other):
        return Vector2(y=self.y // other, x=self.x // other)

    def __mod__(self, other):
        return Vector2(y=self.y % other, x=self.x % other)

    def __mul__(self, other):
        return Vector2(y=self.y * other, x=self.x * other)

    def __add__(self, other):
        return Vector2(y=self.y + other.y, x=self.x + other.x)

    def __sub__(self, other):
        return Vector2(y=self.y - other.y, x=self.x - other.x)

    def __eq__(self, other):
        if self.y == other.y and self.x == other.x:
            return True
        else:
            return False

    def __le__(self, other):  # <=
        if self.y <= other.y and self.x <= other.x:
            return True
        else:
            return False

    def __ge__(self, other):  # >=
        if self.y >= other.y and self.x >= other.x:
            return True
        else:
            return False

    def __lt__(self, other):  # <
        if self.y < other.y and self.x < other.x:
            return True
        else:
            return False

    def __gt__(self, other):  # >
        if self.y > other.y and self.x > other.x:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"x:{self.x}/y:{self.y}"

    def get(self):
        return self.x, self.y
