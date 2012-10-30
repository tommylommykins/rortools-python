from ..MaxObjects import Box

from Py3dsMax import mxs

def import_fixes(node_positions, fixes, object_holder):
    for fix in fixes:
        box = Box.Box(node_positions[fix],
                name="fix",
                wirecolor=mxs.point3(62, 55, 83))
        object_holder.add_object(box.max_object)