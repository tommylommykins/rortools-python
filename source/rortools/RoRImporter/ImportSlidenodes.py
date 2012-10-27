import GroupBy

from ..MaxObjects import Slidenode

def import_slidenodes(node_positions, slidenodes, object_holder):
    for i, slidenode in enumerate(slidenodes):
        attribute_dict = slidenode.copy()
        del attribute_dict['id']
        del attribute_dict['nodes']
        nodes = map(lambda node: node_positions[node], slidenode['nodes'])
        max_slidenode = Slidenode.Slidenode(node_positions[slidenode['id']], nodes, attribute_dict)
        max_slidenode.set_max_names(i)
        
        object_holder.add_object(max_slidenode.id_box.max_object)
        for box in max_slidenode.nodes:
            object_holder.add_object(box.max_object)