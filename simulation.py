import geo

class Circle(object):
    def __init__(self, position, radius, velocity):
        self.position = position
        self.radius = radius
        self.velocity = velocity

class Simulator(object):
    def __init__(self):
        self.circles = []
        self.min_x = self.min_y = 0
        self.max_x = self.max_y = 0

    def addCircle(self, circle):
        self.circles.append(circle)

    def setBounds(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def advance(self, time):
        for circle in self.circles:
            circle.position += circle.velocity * time   

            self.handleBounds(circle)

    def handleBounds(self, circle):
        if circle.position.x - circle.radius <= self.min_x:
            circle.position.x = self.min_x + circle.radius
            circle.velocity = geo.Vector(-circle.velocity.x, circle.velocity.y)

        if circle.position.x + circle.radius >= self.max_x:
            circle.position.x = self.max_x - circle.radius
            circle.velocity = geo.Vector(-circle.velocity.x, circle.velocity.y)

        if circle.position.y - circle.radius <= self.min_y:
            circle.position.y = self.min_y + circle.radius
            circle.velocity = geo.Vector(circle.velocity.x, -circle.velocity.y)

        if circle.position.y + circle.radius >= self.max_y:
            circle.position.y = self.max_y - circle.radius
            circle.velocity = geo.Vector(circle.velocity.x, -circle.velocity.y)

