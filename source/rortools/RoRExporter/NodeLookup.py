import Position; reload(Position)

import sys

class NodeLookup(object):
    def nearest_node(self, position_string):
        the_pos = Position.Position(position_string) 
        closest_distance = sys.float_info.max
        nearest_node = 0
        for node in self.nodes:
            distance = the_pos.distance_to(node.position) 
            if distance < closest_distance:
                nearest_node = self.nodes.index(node)
                closest_distance = distance
        return nearest_node