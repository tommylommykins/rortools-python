from Py3dsMax import mxs

class GlobalDataBox(object):
    def __init__(self, truck_name, global_data, object_holder):
        self.max_object = mxs.box(length=0.08, \
                                       width=0.08, \
                                       height=0.08, \
                                       pos=mxs.Point3(0, 0, 0), \
                                       wirecolor=mxs.red)
        self.max_object.name = "global_data_" + truck_name
        mxs.CustAttributes.add(self.max_object, mxs.RoRGlobals)
        self.max_object.global_data = global_data
        object_holder.add_object(self.max_object)
        