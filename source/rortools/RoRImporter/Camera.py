from Py3dsMax import mxs

class Camera(object):
    def __init__(self, counter, center_pos, back_pos, left_pos, obj_holder):
        camera_1 = mxs.box(length=0.08, \
                           width=0.08, \
                           height=0.08, \
                           #pos=center_pos, \
                           pos=center_pos, \
                           wirecolor=mxs.brown)
        camera_1.name = "camera_center_" + str(counter) 
        obj_holder.add_object(camera_1)
        camera_2 = mxs.box(length=0.08, \
                           width=0.08, \
                           height=0.08, \
                           pos=back_pos, \
                           wirecolor=mxs.brown)
        camera_2.name = "camera_back_" + str(counter)
        obj_holder.add_object(camera_2)
        camera_3 = mxs.box(length=0.08, \
                           width=0.08, \
                           height=0.08, \
                           pos=left_pos, \
                           wirecolor=mxs.brown)
        camera_3.name = "camera_left_" + str(counter)
        obj_holder.add_object(camera_3)
