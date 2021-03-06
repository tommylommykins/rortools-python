from Py3dsMax import mxs
import BeamThing
import MaxObjectCustAttribute

class Wheel(BeamThing.BeamThing, MaxObjectCustAttribute.MaxObjectCustAttribute):
    def __init__(self, node_pairs, properties):
        BeamThing.BeamThing.__init__(self)
        MaxObjectCustAttribute.MaxObjectCustAttribute.__init__(self)
        self.apply_custattributes(properties)
        self.max_object.wirecolor = mxs.color(55, 76, 83)
        self.max_object.render_displayRenderMesh = True
        self.max_object.render_viewport_rectangular = False
        self.max_object.render_thickness = (properties['radius'] * 2)
        self.max_object.render_sides = properties['rays']
        self.draw_lines_from_node_pairs(node_pairs)
            
    def apply_custattributes(self, properties):
        mxs.custattributes.add(self.max_object, mxs.RoRWheel)
        properties = properties.copy()
        del properties['node1']
        del properties['node2']
        del properties['rigidity_node']
        del properties['reference_node']
        self.set_custattribute_by_dict(properties)