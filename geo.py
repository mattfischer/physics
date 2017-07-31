class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, vector):
        x = self.x + vector.x
        y = self.y + vector.y
        return Point(x, y)

class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, number):
        x = self.x * number
        y = self.y * number
        return Vector(x, y)

