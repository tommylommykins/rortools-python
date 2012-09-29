from Py3dsMax import mxs

import Box

class Camera(object):
    def __init__(self, counter, center_node, back_node, left_node):
        node_list = [("1", center_node, "camera_center_"),
                     ("2", back_node, "camera_back_"),
                     ("3", left_node, "camera_left_")]
        for box_number, current_node, box_name in node_list:
            box = Box.Box(current_node,
                          name=box_name + str(counter),
                          wirecolor=mxs.brown)
            setattr(self, "camera_" + box_number, box.max_object)