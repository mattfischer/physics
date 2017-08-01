import simulation
import geo

def createSimulator():
    sim = simulation.Simulator()

    sim.addCircle(simulation.Circle(geo.Point(0, 0), 1, geo.Vector(10, 3)))

    return sim
