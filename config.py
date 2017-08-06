import simulation
import geo

def createSimulator():
    sim = simulation.Simulator()

    sim.addCircle(simulation.Circle(geo.Point(-10, -0.5), 1, geo.Vector(20, 0)))
    sim.addCircle(simulation.Circle(geo.Point(10,0), 1, geo.Vector(-20, 0)))
    sim.addCircle(simulation.Circle(geo.Point(0,5), 1, geo.Vector(5, 8)))
    sim.addCircle(simulation.Circle(geo.Point(0,-5), 1, geo.Vector(5, -6)))
    sim.addCircle(simulation.Circle(geo.Point(15,8), 1, geo.Vector(3, 7)))


    return sim
