import geo

import itertools
import math

R = 0.75
GRAVITY = geo.Vector(0, 20)

class Circle(object):
    def __init__(self, position, radius, density, velocity):
        self.position = position
        self.radius = radius
        self.mass = density * math.pi * radius * radius
        self.velocity = velocity

class Plane(object):
    def __init__(self, normal, displacement):
        self.normal = normal
        self.displacement = displacement

class Polygon(object):
    def __init__(self, position, rotation, points, velocity, angular_velocity):
        self.position = position
        self.rotation = rotation
        self.points = points
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        self.collision = False

    def transformed_points(self):
        points = []
        for point in self.points:
            cos = math.cos(self.rotation)
            sin = math.sin(self.rotation)
            x = point.x * cos - point.y * sin + self.position.x
            y = point.x * sin + point.y * cos + self.position.y
            points.append(geo.Point(x, y))
        return points

class Simulator(object):
    def __init__(self):
        self.circles = []
        self.planes = []
        self.polygons = []

    def add_circle(self, circle):
        self.circles.append(circle)

    def add_polygon(self, polygon):
        self.polygons.append(polygon)

    def set_bounds(self, min_x, min_y, max_x, max_y):
        self.planes.append(Plane(geo.Vector(1.0, 0), min_x))
        self.planes.append(Plane(geo.Vector(-1.0, 0), -max_x))
        self.planes.append(Plane(geo.Vector(0, 1.0), min_y))
        self.planes.append(Plane(geo.Vector(0, -1.0), -max_y))

    def stabilize_circle(self, circle, normal, distance):
        circle.position -= normal * distance

    def calculate_transferred_momentum(self, velocity1, velocity2, inverse_mass1, inverse_mass2, normal):
        return normal * (velocity1 - velocity2) * (1 + R) / (inverse_mass1 + inverse_mass2)

    def handle_circle_circle_collision(self, circle1, circle2):
        distance = circle2.position - circle1.position
        if distance.magnitude2() <= (circle1.radius + circle2.radius) ** 2 and (circle2.velocity - circle1.velocity) * distance < 0:
            normal = distance.normalize()
            overlap = circle1.radius + circle2.radius - distance.magnitude()
            self.stabilize_circle(circle1, normal, overlap / 2)
            self.stabilize_circle(circle2, -normal, overlap / 2)

            p = self.calculate_transferred_momentum(circle1.velocity, circle2.velocity, 1.0 / circle1.mass, 1.0 / circle2.mass, normal)

            circle1.velocity -= normal * p / circle1.mass
            circle2.velocity += normal * p / circle2.mass

    def handle_circle_plane_collision(self, circle, plane):
        position_vector = geo.Vector(circle.position.x, circle.position.y)
        circle_displacement = position_vector * plane.normal - circle.radius
        if circle_displacement <= plane.displacement and circle.velocity * plane.normal < 0:
            overlap = plane.displacement - circle_displacement
            self.stabilize_circle(circle, -plane.normal, overlap)
            p = self.calculate_transferred_momentum(circle.velocity, geo.Vector(0, 0), 1.0 / circle.mass, 0, -plane.normal)
            circle.velocity += plane.normal * p / circle.mass

    def support(self, points, direction):
        max_point = None
        max_distance = 0
        for point in points:
            v = point - geo.Point(0, 0)
            distance = v * direction
            if max_point is None or distance > max_distance:
                max_point = point
                max_distance = distance
        return max_point

    def minkowski_difference(self, points1, points2, direction):
        point1 = self.support(points1, direction)
        point2 = self.support(points2, -direction)
        return geo.Point(point1.x - point2.x, point1.y - point2.y)

    def gjk_collision(self, points1, points2):
        direction = geo.Vector(1, 0)
        points = []
        points.append(self.minkowski_difference(points1, points2, direction))
        points.append(self.minkowski_difference(points1, points2, -direction))

        if points[0].x < 0 or points[1].x > 0:
            return False

        while True:
            AB = (points[1] - points[0]).normalize()
            AO = geo.Point(0, 0) - points[0]
            direction = AO - AB * (AO * AB)
            points.append(self.minkowski_difference(points1, points2, direction))

            AC = points[2] - points[0]
            if AC * direction < AO * direction:
                return False

            for i in range(0, 3):
                C = points[i]
                A = points[(i + 1) % 3]
                B = points[(i + 2) % 3]

                AB = (B - A).normalize()
                AC = C - A
                AO = geo.Point(0, 0) - A
                direction = AO - AB * (AO * AB)
                if AC * direction < 0:
                    del points[i]
                    break
            else:
                return True

    def handle_polygon_polygon_collision(self, polygon1, polygon2):
        points1 = polygon1.transformed_points()
        points2 = polygon2.transformed_points()

        if self.gjk_collision(points1, points2):
            polygon1.collision = True
            polygon2.collision = True

    def advance(self, time):
        for circle in self.circles:
            circle.velocity += GRAVITY * time
            circle.position += circle.velocity * time   

        for polygon in self.polygons:
            polygon.position += polygon.velocity * time
            polygon.rotation += polygon.angular_velocity * time
            polygon.collision = False

        for (circle1, circle2) in itertools.combinations(self.circles, 2):
            self.handle_circle_circle_collision(circle1, circle2)

        for (circle, plane) in itertools.product(self.circles, self.planes):
            self.handle_circle_plane_collision(circle, plane)

        for (polygon1, polygon2) in itertools.combinations(self.polygons, 2):
            self.handle_polygon_polygon_collision(polygon1, polygon2)

