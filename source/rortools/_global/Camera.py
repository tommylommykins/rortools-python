from Py3dsMax import mxs

class Camera(object):
    def __init__(self, counter, center_node, back_node, left_node):
        self.camera_1 = mxs.box(length=0.08, \
                           width=0.08, \
                           height=0.08, \
                           #pos=center_pos, \
                           pos=center_node.position.to_point3(), \
                           wirecolor=mxs.brown)
        self.camera_1.name = "camera_center_" + str(counter) 
        self.camera_2 = mxs.box(length=0.08, \
                           width=0.08, \
                           height=0.08, \
                           pos=back_node.position.to_point3(), \
                           wirecolor=mxs.brown)
        self.camera_2.name = "camera_back_" + str(counter)
        self.camera_3 = mxs.box(length=0.08, \
                           width=0.08, \
                           height=0.08, \
                           pos=left_node.position.to_point3(), \
                           wirecolor=mxs.brown)
        self.camera_3.name = "camera_left_" + str(counter)
