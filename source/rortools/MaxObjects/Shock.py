from Py3dsMax import mxs
import BeamThing
import MaxObjectCustAttribute

class Shock(BeamThing.BeamThing, MaxObjectCustAttribute.MaxObjectCustAttribute):
    def __init__(self, node_pairs, properties):
        BeamThing.BeamThing.__init__(self)
        MaxObjectCustAttribute.MaxObjectCustAttribute.__init__(self)
        self.apply_custattributes(properties)
        self.max_object.wirecolor = mxs.color(0, 0, 0)
        for node_pair in node_pairs:
            node1, node2 = node_pair
            self.draw_line(node1, node2)
            
    def apply_custattributes(self, properties):
        mxs.custattributes.add(self.max_object, mxs.rorshock)
        properties = properties.copy()
        del properties['node1']
        del properties['node2']
        self.set_custattribute_by_dict(properties)