import NodeLookup
from ..MaxObjects import MaxObjectCustAttribute

from .._global import Node

from Py3dsMax import mxs

class Submesh(NodeLookup.NodeLookup,
            MaxObjectCustAttribute.MaxObjectCustAttribute):
    def __init__(self, max_object, nodes):
        NodeLookup.NodeLookup.__init__(self)
        MaxObjectCustAttribute.MaxObjectCustAttribute.__init__(self)
        
        self.max_object = max_object
        self.nodes = nodes
        
    def render(self):
        if not self.has_custattribute("submeshtype:submeshtype"):
            mxs.custattributes.add(self.max_object, mxs.rorsubesh)
        
        ret = "submesh\n"
        ret += "cab\n"
        all_nodes = set()
        for face_no in range(mxs.getnumfaces(self.max_object)):
            max_face_no = face_no + 1
            vertices = mxs.getface(self.max_object, max_face_no)
            vertices = map(int, filter(lambda thing: len(thing) != 0, str(vertices)[1:-1].split(",")))
            nearest_nodes = []
            for vertex in vertices:
                vertex_pos = Node.Node(mxs.meshop.getvert(self.max_object, vertex, node=self.max_object))
                nearest_node = self.nodes.index(self.nearest_node(vertex_pos))
                nearest_nodes.append(str(nearest_node))
                all_nodes.add(str(nearest_node))
            ret += nearest_nodes[0]
            ret += ", " + nearest_nodes[1]
            ret += ", " + nearest_nodes[2]
            if len(self.max_object.flag.strip()) != 0:
                ret += ", " + self.max_object.flag
            ret += "\n"
        ret += "texcoords\n"
        for node in sorted(list(all_nodes)):
            ret += node + ", 0, 0\n"
        if self.max_object.backmesh:
            ret += "backmesh\n"
        return ret + "\n"

def generate_submeshes(submeshes, nodes):
    if not submeshes:
        return
    ret = ""
    for submesh in submeshes:
        ret += Submesh(submesh, nodes).render()    return ret + "\n"