from Py3dsMax import mxs

from .._global import Node

from ..MaxObjects import Box

def load_node_positions(nodes, object_holder):
    node_positions = []
    for n in nodes:
        node_positions.append(Node.Node([n['x'], n['y'], n['z']]))
        
    #generate separation categories export will note fuse nodes if they are
    #separate at import 
    for i, node1 in enumerate(node_positions):
        for node2 in node_positions:
            if node2 is node1:
                continue
            if node1.distance_to(node2) < 0.02:
                _add_separation_node_box(node1, object_holder)
                node1.separation_category = str(i)
    
    return node_positions

def _add_separation_node_box(node, object_holder):
    box = Box.Box(node, name="separation_node", wirecolor=mxs.green)
    object_holder.add_object(box.max_object)