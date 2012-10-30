import NodeLookup

from Py3dsMax import mxs

class Contacter(NodeLookup.NodeLookup):
    def __init__(self, contacter, nodes):
        NodeLookup.NodeLookup.__init__(self)
        self.max_object = contacter
        self.nodes = nodes
        
    def render(self):
        mxs.centerpivot(self.max_object)
        return str(self.nodes.index(self.nearest_node(self.max_object.pos))) + "\n"

def generate_contacters(contacters, nodes):
    if not contacters:
        return ""
    ret = "contacters\n"
    for contacter in contacters:
        ret += Contacter(contacter, nodes).render()
    return ret + "\n"