import sys

from Py3dsMax import mxs
from blur3d.api import Scene

import Node; reload(Node)
import Beam; reload(Beam)
import GlobalData; reload(GlobalData)
import Camera; reload(Camera)

class Exporter(object):
    def __init__(self):
        mxs.fileIn("rortools/global/definitions.ms")
        data = ""
        data += self.export_global_data()
        data += self.export_nodes()
        data += self.export_beams()
        data += self.export_cameras()
        print data
        
    def export_global_data(self):
        """Exports all data that is not associated with a specific max object.
        """
        global_data_boxes = self.get_objects_by_name("global_data")
        return GlobalData.generate_global_data(global_data_boxes)
        
    def export_nodes(self):
        beam_objects = self.get_objects_by_name("beam")
        beam_objects = sorted(beam_objects, None, lambda b: b.name)
        self.nodes = Node.generate_nodes(beam_objects)
        return Node.render_nodes(self.nodes)
        
    def export_beams(self):
        beam_objects = self.get_objects_by_name("beam")
        return Beam.generate_beams(beam_objects, self.nodes)
    
    def export_cameras(self):
        cameras = self.get_objects_by_name("camera_center", "camera_left", "camera_back")
        return Camera.generate_cameras(cameras, self.nodes)
        
    def get_objects_by_name(self, *names):
        ret = []
        for name in names:
            objects = Scene.instance().objects()
            named_objects = filter(lambda obj: obj.name().lower().startswith(name), objects)
            native_named_objects = map(lambda obj: obj._nativePointer, named_objects)
            ret.extend(native_named_objects)
        return ret