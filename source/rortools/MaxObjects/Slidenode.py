from Py3dsMax import mxs
import MaxObjectCustAttribute

import Box

class Slidenode(MaxObjectCustAttribute.MaxObjectCustAttribute):
    def __init__(self, slider, rails, custattribute_dict):
        MaxObjectCustAttribute.MaxObjectCustAttribute.__init__(self)
        self.max_objects = []
        id_box = Box.Box(slider, name="slidenode_1")
        self.max_objects.append(id_box.max_object)
        for i, rail_node in enumerate(rails):
            node = Box.Box(rail_node, name="slidenode_1_" + str(i))
            self.max_objects.append(node.max_object)
        mxs.custattributes.add(id_box.max_object, mxs.rorslidenode)
        self.set_custattribute_by_dict(custattribute_dict, id_box.max_object)