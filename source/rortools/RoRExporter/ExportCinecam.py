#from .._global import Cinecam; reload(Cinecam)

from Py3dsMax import mxs

import NodeLookup
from ..MaxObjects import MaxObjectCustAttribute
import BeamIterable
from .._global import Node
from ..MaxObjects import Cinecam

class Cinecam(NodeLookup.NodeLookup,
              MaxObjectCustAttribute.MaxObjectCustAttribute,
              BeamIterable.BeamIterable):
    def __init__(self, max_object, nodes):
        NodeLookup.NodeLookup.__init__(self)
        MaxObjectCustAttribute.MaxObjectCustAttribute.__init__(self)
        BeamIterable.BeamIterable.__init__(self)
        self.max_object = max_object
        self.nodes = nodes
        
    def render(self):
        if not self.has_custattribute("CinecamsType:CinecamsType"):
            mxs.CustAttributes.add(self.max_object, mxs.RoRCinecam)
        node_positions = self.all_beams()
        
        #the position-node is the one where many beams meet. So, be examining the first two
        #beams, there should be two nodes that are almost at the same spot. This is the
        #cinecam node
        position_node = self._calculate_position_node(node_positions[0], node_positions[1])
        
        ret = str(position_node.x) + ", " + \
              str(position_node.y) + ", " + \
              str(position_node.z) + ", "
              
        for beam_no in range(8):
            beam = node_positions[beam_no]
            far_node = self._select_non_position_node(position_node, beam)
            ret += str(self.nodes.index(self.nearest_node(far_node))) + ", "
        return ret + "\n"

    def _calculate_position_node(self, beam1_nodes, beam2_nodes):
        """Returns a node whose position is at the actual position of the viewpoint of the
        cinecam.
        
        Compares the points of two beams: One node from beam1 and one node from beam2
        must be at the same point. This is where the cinecam viewpoint is
        """
        maximum_distance = 0.1
        for beam1_node in beam1_nodes:
            for beam2_node in beam2_nodes:
                if beam1_node.distance_to(beam2_node) <= maximum_distance:
                    return beam1_node
        #nonsensical default value -- to be used when something went wrong.
        return beam1_nodes[0]
    
    def _select_non_position_node(self, position_node, other_beam_nodes):
        """Of the beam supplied, one of its nodes should be at the same place as the
        position node, and the other should not be near it.
        This returns the node that is not near it.
        """
        node1 = other_beam_nodes[0]
        node2 = other_beam_nodes[1]
        node1_distance = position_node.distance_to(node1)
        node2_distance = position_node.distance_to(node2)
        if node1_distance < node2_distance:
            return node2
        else:
            return node1
    
def generate_cinecams(cinecams, nodes):
    ret = "cinecam\n"
    if not cinecams:
        cinecam = generate_default_cinecam(nodes)
        cinecams = [cinecam]
    
    for cinecam in cinecams:
        cinecam = Cinecam(cinecam, nodes)
        ret += cinecam.render()
    return ret + "\n"
        
def generate_default_cinecam(nodes):
    position_node = Node.Node(coord_list=[0, 0, 0])
    connection_nodes = nodes[0:8]
    cinecam = Cinecam.Cinecam(0, position_node, connection_nodes)
    return cinecam.max_object