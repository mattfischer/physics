import simulation
import geo

def create_simulator():
    sim = simulation.Simulator()

    sim.add_polygon(simulation.Polygon(geo.Point(-3, 3), 0, [geo.Point(1, 1), geo.Point(-1, 1), geo.Point(-1, -1), geo.Point(1, -1)], geo.Vector(0, 0), 3.14))
    sim.add_polygon(simulation.Polygon(geo.Point(5, 10), 45 * 3.14 / 180, [geo.Point(3, 1), geo.Point(-3, 1), geo.Point(-3, -1), geo.Point(3, -1)], geo.Vector(-1, -1), -3.14))

    return sim
