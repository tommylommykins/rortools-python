from Py3dsMax import mxs

from .._global import Node

class FilteredNodeSet(object):
    def __init__(self, max_distance):
        self.max_distance = max_distance
        self.nodes = []
        
    def add_node(self, candidate_node):
        distances = map(lambda other_node: candidate_node.distance_to(other_node), self.nodes)
        nodes_too_close = filter(lambda distance: self.max_distance >= distance, distances)
        if len(nodes_too_close) == 0: self.nodes.append(candidate_node)
        
class NodeExporter(object):
    def __init__(self, beam_objs):
        unfiltered_nodes = self._read_nodes(beam_objs)
        node_set = FilteredNodeSet(0.1)
        for node in unfiltered_nodes:
            node_set.add_node(node)
            
        self.nodes =  node_set.nodes
        self.node_positions = self._generate_node_positions()
        
    def _generate_node_positions(self):
        the_lambda = lambda node: lambda node: mxs.point3(node.x, node.y, node.z)
        return map(the_lambda, self.nodes)
            
    def render_nodes(self):
        ret = "nodes\n"
        for i, node in enumerate(self.nodes):
            ret += str(i) + ", " + str(node.x) + ", " + str(node.y) + ", " + str(node.z) + "\n"
        return ret

    def _read_nodes(self, beam_objs):
        knots = []
        for beam_obj in beam_objs:
            for spline_no in range(mxs.numsplines(beam_obj)):
                spline_no += 1
                for knot_no in range(mxs.numknots(beam_obj, spline_no)):
                    knot_no += 1
                    knots.append(str(mxs.getKnotPoint(beam_obj, spline_no, knot_no)))
        node_list = []
        for knot in knots:
            node_list.append(Node.Node(knot))
        return sorted(node_list)