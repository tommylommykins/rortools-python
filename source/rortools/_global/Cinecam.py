from Py3dsMax import mxs

import BeamThing

class Cinecam(BeamThing.BeamThing):
    def __init__(self, position_node, connection_nodes, properties):
        BeamThing.BeamThing.__init__(self)
        self.make_max_object(position_node, connection_nodes, properties)
        
    def make_max_object(self, position_node, connection_nodes, properties):
        self._spline_shape("aoue")
        for connection_node in connection_nodes:
            self.draw_line(position_node, connection_node)
        self.max_object.wirecolor = mxs.blue
        mxs.CustAttributes.add(self.max_object, mxs.RoRCinecam)
        if 'spring' in properties: self.max_object.spring = properties['spring']
        if 'damp'in properties: self.max_object.damp = properties['damp']