from Py3dsMax import mxs

import BeamThing; reload(BeamThing)

class Cinecam(BeamThing.BeamThing):
    def __init__(self, counter, position_node, connection_nodes, spring=None, damping=None):
        BeamThing.BeamThing.__init__(self)
        self.make_max_object(position_node, connection_nodes, spring, damping)
        self.name = "cinecam_" + str(counter)
        
    def make_max_object(self, position_node, connection_nodes, spring, damping):
        self._spline_shape("aoue")
        for connection_node in connection_nodes:
            self.draw_line(position_node, connection_node)
        self.max_object.wirecolor = mxs.blue
        mxs.CustAttributes.add(self.max_object, mxs.RoRCinecam)
        if spring is not None: self.max_object.spring = spring
        if damping is not None: self.max_object.damping = damping
        
def generate_cinecams(cinecams, nodes):
    ret = "cinecam"
    return ret