import geo

import itertools
import math

class Circle(object):
    def __init__(self, position, radius, mass, velocity):
        self.position = position
        self.radius = radius
        self.mass = mass
        self.velocity = velocity

class Plane(object):
    def __init__(self, normal, displacement):
        self.normal = normal
        self.displacement = displacement

class Simulator(object):
    def __init__(self):
        self.circles = []
        self.planes = []

    def add_circle(self, circle):
        self.circles.append(circle)

    def set_bounds(self, min_x, min_y, max_x, max_y):
        self.planes.append(Plane(geo.Vector(1.0, 0), min_x))
        self.planes.append(Plane(geo.Vector(-1.0, 0), -max_x))
        self.planes.append(Plane(geo.Vector(0, 1.0), min_y))
        self.planes.append(Plane(geo.Vector(0, -1.0), -max_y))

    def stabilize_circle(self, circle, normal, distance):
        circle.position -= normal * distance

    def calculate_transferred_momentum(self, velocity1, velocity2, inverse_mass1, inverse_mass2, normal):
        return normal * (velocity1 - velocity2) * 2 / (inverse_mass1 + inverse_mass2)

    def handle_circle_circle_collision(self, circle1, circle2):
        distance = circle1.position - circle2.position
        if (circle1.position - circle2.position).magnitude2() <= (circle1.radius + circle2.radius) ** 2: 
            normal = (circle2.position - circle1.position).normalize()
            distance = circle1.radius + circle2.radius - (circle2.position - circle1.position).magnitude()
            self.stabilize_circle(circle1, normal, distance / 2)
            self.stabilize_circle(circle2, -normal, distance / 2)

            p = self.calculate_transferred_momentum(circle1.velocity, circle2.velocity, 1.0 / circle1.mass, 1.0 / circle2.mass, normal)

            circle1.velocity -= normal * p / circle1.mass
            circle2.velocity += normal * p / circle2.mass

    def handle_circle_plane_collision(self, circle, plane):
        position_vector = geo.Vector(circle.position.x, circle.position.y)
        circle_displacement = position_vector * plane.normal - circle.radius
        if circle_displacement <= plane.displacement and circle.velocity * plane.normal < 0:
            self.stabilize_circle(circle, -plane.normal, plane.displacement - circle_displacement)
            p = self.calculate_transferred_momentum(circle.velocity, geo.Vector(0, 0), 1.0 / circle.mass, 0, -plane.normal)
            circle.velocity += plane.normal * p / circle.mass

    def advance(self, time):
        for circle in self.circles:
            circle.position += circle.velocity * time   

        for (circle1, circle2) in itertools.combinations(self.circles, 2):
            self.handle_circle_circle_collision(circle1, circle2)

        for (circle, plane) in itertools.product(self.circles, self.planes):
            self.handle_circle_plane_collision(circle, plane)

