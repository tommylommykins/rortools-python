import math

class FilteredNodeSet(object):
    def __init__(self, max_distance):
        self.max_distance = max_distance
        self.nodes = []
        
    def add_node(self, candidate_node):
        distances = map(lambda node: self._distance(candidate_node, node), self.nodes)
        nodes_too_close = filter(lambda distance: self.max_distance >= distance, distances)
        if len(nodes_too_close) == 0: self.nodes.append(candidate_node)
        

    def _distance(self, node1, node2):
        return math.sqrt(((node1.x - node2.x) ** 2) +
                           ((node1.y - node2.y) ** 2) +
                           ((node1.z - node2.z) ** 2))
    