import NodeLookup
from ..MaxObjects import MaxObjectCustAttribute
import BeamIterable

from Py3dsMax import mxs

class Hydro(NodeLookup.NodeLookup,
              MaxObjectCustAttribute.MaxObjectCustAttribute,
              BeamIterable.BeamIterable):
    def __init__(self, max_object, nodes):
        NodeLookup.NodeLookup.__init__(self)
        MaxObjectCustAttribute.MaxObjectCustAttribute.__init__(self)
        BeamIterable.BeamIterable.__init__(self)
        
        self.max_object = max_object
        self.nodes = nodes
        
    def render(self):
        if not self.has_custattribute("hydrostype:hydrostype"):
            mxs.custattributes.add(self.max_object, mxs.rorhydro)
        
        ret = ""
        for node1, node2 in self.all_beams():
            ret += str(self.nodes.index(self.nearest_node(node1))) + ", "
            ret += str(self.nodes.index(self.nearest_node(node2))) + ", "
            ret += str(self.max_object.ratio) + ", "
            ret += str(self.max_object.opts) + ", "
            ret += str(self.max_object.start_delay) + ", "
            ret += str(self.max_object.stop_delay) + ", "
            ret += str(self.max_object.start_function) + ", "
            ret += str(self.max_object.stop_function)
            ret += "\n"
        return ret 
    
def generate_hydros(hydros, nodes):
    if not hydros:
        return ""
    ret = "hydros\n"
    for hydro in hydros:
        ret += Hydro(hydro, nodes).render()
    return ret + "\n"