import geo

import itertools
import math

class Circle(object):
    def __init__(self, position, radius, velocity):
        self.position = position
        self.radius = radius
        self.velocity = velocity

class Plane(object):
    def __init__(self, normal, displacement):
        self.normal = normal
        self.displacement = displacement

class Simulator(object):
    def __init__(self):
        self.circles = []
        self.planes = []

    def addCircle(self, circle):
        self.circles.append(circle)

    def setBounds(self, min_x, min_y, max_x, max_y):
        self.planes.append(Plane(geo.Vector(1.0, 0), min_x))
        self.planes.append(Plane(geo.Vector(-1.0, 0), -max_x))
        self.planes.append(Plane(geo.Vector(0, 1.0), min_y))
        self.planes.append(Plane(geo.Vector(0, -1.0), -max_y))

    def stabilizeCircle(self, circle, normal, distance):
        circle.position -= normal * distance

    def handleCircleCircleCollision(self, circle1, circle2):
        normal = (circle2.position - circle1.position).normalize()
        distance = circle1.radius + circle2.radius - (circle2.position - circle1.position).magnitude()
        self.stabilizeCircle(circle1, normal, distance / 2)
        self.stabilizeCircle(circle2, -normal, distance / 2)

        p = normal * (circle1.velocity - circle2.velocity)
        circle1.velocity -= normal * p
        circle2.velocity += normal * p

    def advance(self, time):
        for circle in self.circles:
            circle.position += circle.velocity * time   

        for (circle1, circle2) in itertools.combinations(self.circles, 2):
            distance = circle1.position - circle2.position
            if (circle1.position - circle2.position).magnitude2() <= (circle1.radius + circle2.radius) ** 2:
                self.handleCircleCircleCollision(circle1, circle2)

        for circle in self.circles:
            self.handleBounds(circle)

    def handleBounds(self, circle):
        for plane in self.planes:
            position_vector = geo.Vector(circle.position.x, circle.position.y)
            circle_displacement = position_vector * plane.normal - circle.radius
            if circle_displacement <= plane.displacement and circle.velocity * plane.normal < 0:
                self.stabilizeCircle(circle, -plane.normal, plane.displacement - circle_displacement)
                p = -plane.normal * circle.velocity * 2
                circle.velocity += plane.normal * p

