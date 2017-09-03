import simulation
import geo

def create_simulator():
    sim = simulation.Simulator()

    sim.add_polygon(
        simulation.Polygon(
            geo.Point(-3, 2),
            30 * 3.14 / 180,
            [geo.Point(1, 1), geo.Point(-1, 1), geo.Point(-1, -1), geo.Point(1, -1)],
            1,
            2.0 / 3.0,
            geo.Vector(4, 0),
            geo.Vector(0, 0, 2 * 3.14)
        )
    )

    sim.add_polygon(
        simulation.Polygon(
            geo.Point(5, 0),
            90 * 3.14 / 180,
            [geo.Point(3, 1), geo.Point(-3, 1), geo.Point(-3, -1), geo.Point(3, -1)],
            3,
            10,
            geo.Vector(0, 0),
            geo.Vector(0, 0, 3.14)
        )
    )

    return sim
