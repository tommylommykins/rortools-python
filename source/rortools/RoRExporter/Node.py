from Py3dsMax import mxs

import Position

class Node(object):
    def __init__(self, position_string):
        self.position = self._generate_position(position_string)
    
    def _generate_position(self, knot):
        return Position.Position(str(knot))
    
    def __cmp__(self, other):
        if self.position.x > other.position.x:
            return 1
        if self.position.x < other.position.x:
            return -1
        
        if self.position.y > other.position.y:
            return 1
        if self.position.y < other.position.y:
            return -1
        
        if self.position.z > other.position.z:
            return 1
        if self.position.z < other.position.z:
            return -1
        return 0
            
class FilteredNodeSet(object):
    def __init__(self, max_distance):
        self.max_distance = max_distance
        self.nodes = []
        
    def add_node(self, candidate_node):
        distances = map(lambda other_node: candidate_node.position.distance_to(other_node.position), self.nodes)
        nodes_too_close = filter(lambda distance: self.max_distance >= distance, distances)
        if len(nodes_too_close) == 0: self.nodes.append(candidate_node)

def generate_nodes(beam_objs):
    print "nodes\n"
    unfiltered_nodes = _read_nodes(beam_objs)
    node_set = FilteredNodeSet(0.1)
    for node in unfiltered_nodes:
        node_set.add_node(node)
    return node_set.nodes
            
def render_nodes(nodes):
    ret = ""
    for i, node in enumerate(nodes):
        ret += str(i) + ", " + str(node.position.x) + ", " + str(node.position.y) + ", " + str(node.position.z) + "\n"
    return ret

def _read_nodes(beam_objs):
    knots = []
    for beam_obj in beam_objs:
        #print mxs.pyhelper.namify(beam_obj.name)
        for spline_no in range(mxs.numsplines(beam_obj)):
            spline_no += 1
            for knot_no in range(mxs.numknots(beam_obj, spline_no)):
                knot_no += 1
                knots.append(mxs.getKnotPoint(beam_obj, spline_no, knot_no))
    return sorted(map(Node, knots))