import NodeLookup
from ..MaxObjects import MaxObjectCustAttribute
import BeamIterable

from Py3dsMax import mxs

class Command(NodeLookup.NodeLookup,
              MaxObjectCustAttribute.MaxObjectCustAttribute,
              BeamIterable.BeamIterable):
    def __init__(self, max_object, nodes):
        NodeLookup.NodeLookup.__init__(self)
        MaxObjectCustAttribute.MaxObjectCustAttribute.__init__(self)
        BeamIterable.BeamIterable.__init__(self)
        
        self.max_object = max_object
        self.nodes = nodes
        
    def render(self):
        if not self.has_custattribute("commandstype:commandstype"):
            mxs.custattributes.add(self.max_object, mxs.rorcommand)
        
        ret = ""
        for node1, node2 in self.all_beams():
            ret += str(self.nodes.index(self.nearest_node(node1))) + ", "
            ret += str(self.nodes.index(self.nearest_node(node2))) + ", "
            ret += str(self.max_object.short_rate) + ", "
            ret += str(self.max_object.long_rate) + ", "
            ret += str(self.max_object.amount_short) + ", "
            ret += str(self.max_object.amount_long) + ", "
            ret += str(self.max_object.short_key) + ", "
            ret += str(self.max_object.long_key) + ", "
            ret += str(self.max_object.options_var) + ", "
            ret += str(self.max_object.description) + ", "
            ret += str(self.max_object.start_delay) + ", "
            ret += str(self.max_object.stop_delay) + ", "
            ret += str(self.max_object.start_function) + ", "
            ret += str(self.max_object.stop_function) + ", "
            ret += str(self.max_object.affect_engine)[0]
            ret += "\n"
        return ret 
    
def generate_commands(commands, nodes):
    if not commands:
        return ""
    ret = "commands2\n"
    for command in commands:
        ret += Command(command, nodes).render()
    return ret + "\n"