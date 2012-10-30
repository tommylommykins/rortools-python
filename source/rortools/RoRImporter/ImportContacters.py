from ..MaxObjects import Box

from Py3dsMax import mxs

def import_contacters(node_positions, contacters, object_holder):
    for contacter in contacters:
        box = Box.Box(node_positions[contacter],
                name="contacter",
                wirecolor=mxs.point3(62, 55, 83))
        object_holder.add_object(box.max_object)