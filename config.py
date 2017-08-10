import simulation
import geo

def create_simulator():
    sim = simulation.Simulator()

    sim.add_circle(simulation.Circle(geo.Point(-10, -0.5), 1, 1, geo.Vector(20, 0)))
    sim.add_circle(simulation.Circle(geo.Point(10,0), 2, 1, geo.Vector(-20, 0)))
    sim.add_circle(simulation.Circle(geo.Point(0,5), 3, 1, geo.Vector(5, 8)))
    sim.add_circle(simulation.Circle(geo.Point(0,-5), 2, 1, geo.Vector(5, -6)))
    sim.add_circle(simulation.Circle(geo.Point(15,8), 1, 1, geo.Vector(3, 7)))

    sim.add_polygon(simulation.Polygon(geo.Point(3, 3), 45 * 3.14 / 180, [geo.Point(0.5, 0.5), geo.Point(-0.5, 0.5), geo.Point(-0.5, -0.5), geo.Point(0.5, -0.5)], geo.Vector(0, 0), 3.14))

    return sim
