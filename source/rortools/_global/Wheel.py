from Py3dsMax import mxs
import BeamThing

class Wheel(BeamThing.BeamThing):
    def __init__(self, counter, node1, node2, properties):
        BeamThing.BeamThing.__init__(self)
        self.draw_line(node1, node2)
        self.name = "wheel_" + str(counter)