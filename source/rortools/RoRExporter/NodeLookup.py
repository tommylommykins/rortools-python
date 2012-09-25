#from .._global import Position; reload(Position)

import sys

class NodeLookup(object):
    def nearest_node(self, pos):
        best_distance = sys.float_info.max
        best_node = self.nodes[0] 
        for node in self.nodes:
            distance = node.distance_to(pos)
            if distance == 0.0:
                return node
            if distance < best_distance:
                best_distance = distance
                best_node = node
        return best_node 