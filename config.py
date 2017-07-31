import simulation
import geo

def createSimulator():
    sim = simulation.Simulator()

    sim.addCircle(simulation.Circle(geo.Point(0, 0), 1, geo.Vector(5, 0)))

    return sim
