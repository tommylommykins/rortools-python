import NodeLookup
from ..MaxObjects import MaxObjectCustAttribute
import BeamIterable

from Py3dsMax import mxs

class Shock(NodeLookup.NodeLookup,
            MaxObjectCustAttribute.MaxObjectCustAttribute,
            BeamIterable.BeamIterable):
    def __init__(self, max_object, nodes):
        NodeLookup.NodeLookup.__init__(self)
        MaxObjectCustAttribute.MaxObjectCustAttribute.__init__(self)
        BeamIterable.BeamIterable.__init__(self)
        self.max_object = max_object
        self.nodes = nodes
        
    def render(self):
        if not self.has_custattribute("shockstype:shockstype"):
            mxs.custattributes.add(self.max_object, mxs.rorshock)
            
        ret = ""
        for node1, node2 in self.all_beams():
            ret += str(self.nodes.index(self.nearest_node(node1))) + ", "
            ret += str(self.nodes.index(self.nearest_node(node2))) + ", "
            ret += str(self.max_object.spring_in) + ", "
            ret += str(self.max_object.damp_in) + ", "
            ret += str(self.max_object.progressive_spring_in) + ", "
            ret += str(self.max_object.progressive_damp_in) + ", "
            ret += str(self.max_object.spring_out) + ", "
            ret += str(self.max_object.damp_out) + ", "
            ret += str(self.max_object.progressive_spring_out) + ", "
            ret += str(self.max_object.progressive_damp_out) + ", "
            ret += str(self.max_object.shortest_length) + ", "
            ret += str(self.max_object.longest_length) + ", "
            ret += str(self.max_object.precompression)
            opts = self.max_object.opts.strip()
            if opts:
                ret += ", " +  opts
            ret += "\n"
        return ret
        
def generate_shocks(shocks, nodes):
    if not shocks:
        return ""
    ret = "shocks2\n"
    for shock in shocks:
        ret += Shock(shock, nodes).render()
    return ret + "\n"