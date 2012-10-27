from Py3dsMax import mxs
import MaxObjectCustAttribute

import Box

class Slidenode(MaxObjectCustAttribute.MaxObjectCustAttribute):
    def __init__(self, slider, rails, custattribute_dict):
        MaxObjectCustAttribute.MaxObjectCustAttribute.__init__(self)
        self.id_box = Box.Box(slider, name="slidenode_slider")
        self.nodes = []
        
        for i, rail_node in enumerate(rails):
            node = Box.Box(rail_node, name="slidenode_rail" + str(i))
            self.nodes.append(node)
        mxs.custattributes.add(self.id_box.max_object, mxs.rorslidenode)
        self.set_custattribute_by_dict(custattribute_dict, self.id_box.max_object)
        
    def set_max_names(self, new_name):
        self.id_box.max_object.name = "slidenode_" + str(new_name) + "_slider"
        for j, box in enumerate(self.nodes):
            box.max_object.name = "slidenode_" + str(new_name) + "_rail_" + str(j)