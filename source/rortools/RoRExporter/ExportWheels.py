import NodeLookup
from .._global import MaxObjectCustAttribute
import BeamIterable

from .._global import Node

from Py3dsMax import mxs

import blur3d.api

class Wheel(NodeLookup.NodeLookup,
            MaxObjectCustAttribute.MaxObjectCustAttribute,
            BeamIterable.BeamIterable):
    def __init__(self, max_object, nodes):
        NodeLookup.NodeLookup.__init__(self)
        MaxObjectCustAttribute.MaxObjectCustAttribute.__init__(self)
        BeamIterable.BeamIterable.__init__(self)
        self.max_object = max_object
        self.nodes = nodes
        
    def render(self):
        if not self.has_custattribute("WheelsType:WheelsType"):
            mxs.custattributes.add(self.max_object, mxs.rorwheel)
            
        ret = ""
        for node1, node2 in self.all_beams():
            ret += str(self.max_object.radius) + ", "
            ret += "0, "
            ret += str(self.max_object.rays) + ", "
            ret += str(self.nodes.index(self.nearest_node(node1))) + ", "
            ret += str(self.nodes.index(self.nearest_node(node2))) + ", "
            ret += self.rigidity_node_number() + ", "
            ret += str(self.max_object.braked) + ", "
            ret += str(self.max_object.driven) + ", "
            ret += "9999, "
            ret += str(self.max_object.mass) + ", "
            ret += str(self.max_object.spring) + ", "
            ret += str(self.max_object.damp) + ", "
            ret += str(self.max_object.face_material) + " "
            ret += str(self.max_object.tread_material) + "\n"
        return ret
            
    def rigidity_node_number(self):
        all_objects = blur3d.api.Scene().objects()
        required_name = "rigidity_node_" + self.max_object.name
        rigidity_nodes = filter(lambda obj: obj.name() == required_name,all_objects)
        if rigidity_nodes:
            chosen_node = rigidity_nodes[0].nativePointer()
            mxs.centerpivot(chosen_node)
            the_node = Node.Node(chosen_node.pos)
            return str(self.nodes.index(self.nearest_node(the_node)))
        return "9999"
    
def generate_wheels(wheels, nodes):
    ret = "wheels\n"
    for wheel in wheels:
        ret += Wheel(wheel, nodes).render()
    return ret + "\n"