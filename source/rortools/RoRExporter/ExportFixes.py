import NodeLookup

from Py3dsMax import mxs

class Fix(NodeLookup.NodeLookup):
    def __init__(self, fix, nodes):
        NodeLookup.NodeLookup.__init__(self)
        self.max_object = fix
        self.nodes = nodes
        
    def render(self):
        mxs.centerpivot(self.max_object)
        return str(self.nodes.index(self.nearest_node(self.max_object.pos))) + "\n"

def generate_fixes(fixes, nodes):
    if not fixes:
        return ""
    ret = "fixes\n"
    for fix in fixes:
        ret += Fix(fix, nodes).render()
    return ret + "\n"