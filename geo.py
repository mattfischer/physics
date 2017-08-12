import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'geo.Point(%s, %s)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, vector):
        return Point(self.x + vector.x, self.y + vector.y)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Vector(self.x - other.x, self.y - other.y)
        else:
            return Point(self.x - other.x, self.y - other.y)

class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'geo.Vector(%s, %s)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            return Vector(self.x * other, self.y * other)

    def __div__(self, other):
        return Vector(self.x / other, self.y / other)

    def __truediv__(self, other):
        return self.__div__(other)

    def __neg__(self):
        return self * -1

    def magnitude2(self):
        return self * self

    def magnitude(self):
        return math.sqrt(self.magnitude2())

    def normalize(self):
        return self / self.magnitude()
