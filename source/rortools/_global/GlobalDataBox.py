from Py3dsMax import mxs

import Box
import Node

class GlobalDataBox(Box.Box):
    def __init__(self, truck_name, global_data):
        Box.Box.__init__(self,
                         Node.Node([0, 0, 0]),
                         wirecolor=mxs.red,
                         name="global_data_" + truck_name)
        mxs.CustAttributes.add(self.max_object, mxs.RoRGlobals)
        self.max_object.global_data = global_data
        