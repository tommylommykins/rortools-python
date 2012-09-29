import sys

from Py3dsMax import mxs
from blur3d.api import Scene

import Node
import Beam
import GlobalData
import Camera
import Cinecam
import ExportWheels

from .._global import MaxObjHolder

class Exporter(object):
    def __init__(self):
        mxs.fileIn("rortools/_global/definitions.ms")
        self.rotate_all_to_ror()
        data = ""
        data += self.export_global_data()
        data += self.export_nodes() #This has the side effect of generating self.nodes and self.node_positions
        data += self.export_beams()
        data += self.export_cameras()
        data += self.export_cinecams()
        data += self.export_wheels()
        data += "\nend\n"
        self.rotate_all_to_max()
        print data
        
    def export_global_data(self):
        """Exports all data that is not associated with a specific max object.
        """
        global_data_boxes = self.get_objects_by_name("global_data")
        return GlobalData.generate_global_data(global_data_boxes)
            
    def export_nodes(self):
        beam_objects = self.get_objects_by_name("beam")
        beam_objects = sorted(beam_objects, None, lambda b: b.name)
        exporter = Node.NodeExporter(beam_objects)
        self.nodes = exporter.nodes
        self.node_positions = exporter.node_positions
        return exporter.render_nodes()
        
    def export_beams(self):
        beam_objects = self.get_objects_by_name("beam")
        return Beam.generate_beams(beam_objects, self.nodes)
    
    def export_cameras(self):
        cameras = self.get_objects_by_name("camera_center", "camera_left", "camera_back")
        return Camera.generate_cameras(cameras, self.nodes)
    
    def export_cinecams(self):
        cinecams = self.get_objects_by_name("cinecam")
        return Cinecam.generate_cinecams(cinecams, self.nodes)
    
    def export_wheels(self):
        wheels = self.get_objects_by_name("wheel")
        return ExportWheels.generate_wheels(wheels, self.nodes)
        
    def get_objects_by_name(self, *names):
        ret = []
        for name in names:
            objects = Scene.instance().objects()
            named_objects = filter(lambda obj: obj.name().lower().startswith(name), objects)
            native_named_objects = map(lambda obj: obj._nativePointer, named_objects)
            ret.extend(native_named_objects)
        return ret
    
    def rotate_all_to_ror(self):
        #get all objects
        objects = self.get_objects_by_name("")
        holder = MaxObjHolder.MaxObjHolder(objects)
        holder.rotate_from_max_to_ror()
    
    def rotate_all_to_max(self):
        objects = self.get_objects_by_name("")
        holder = MaxObjHolder.MaxObjHolder(objects)
        holder.rotate_from_ror_to_max()