import geo

class Circle(object):
    def __init__(self, position, radius, velocity):
        self.position = position
        self.radius = radius
        self.velocity = velocity

class Simulator(object):
    def __init__(self):
        self.circles = []

    def addCircle(self, circle):
        self.circles.append(circle)

    def advance(self, time):
        for circle in self.circles:
            circle.position += circle.velocity * time   
