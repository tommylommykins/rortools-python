from ..MaxObjects import Cinecam
from .._global import Node 

def import_cinecams(node_positions, cinecams, object_holder):
    for i, cinecam in enumerate(cinecams):
        position_node = Node.Node([cinecam['x'], cinecam['y'], cinecam['z']])
        connection_nodes = []
        for connection_node in cinecam['nodes']:
            connection_nodes.append(node_positions[connection_node])
        cinecam = Cinecam.Cinecam(position_node, connection_nodes, cinecam)
        cinecam.max_object.name = "cinecam_" + str(i)
        object_holder.add_object(cinecam.max_object)