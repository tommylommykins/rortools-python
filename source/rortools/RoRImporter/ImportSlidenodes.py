import GroupBy

from ..MaxObjects import Slidenode

def import_slidenodes(node_positions, slidenodes, object_holder):
    for slidenode in slidenodes:
        attribute_dict = slidenode.copy()
        del attribute_dict['id']
        del attribute_dict['nodes']
        print slidenode
        nodes = map(lambda node: node_positions[node], slidenode['nodes'])
        max_slidenode = Slidenode.Slidenode(node_positions[slidenode['id']], nodes, attribute_dict)
        for max_object in max_slidenode.max_objects:
            object_holder.add_object(max_object)