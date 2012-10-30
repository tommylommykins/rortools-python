import sys

from Py3dsMax import mxs
from blur3d.api import Scene

import ExportNode
import ExportBeam
import ExportGlobalData
import ExportCamera
import ExportCinecam
import ExportWheels
import ExportShocks
import ExportCommands
import ExportHydros
import ExportSlidenodes
import ExportSubmeshes
import ExportContacters

from .._global import MaxObjHolder

import ColumnAligner

class Exporter(object):
    def __init__(self):
        mxs.fileIn("rortools/_global/definitions.ms")
        
        self.rotate_all_to_ror()
        
        data = ""
        data += self.export_global_data()
        data += self.export_nodes() #This has the side effect of generating self.nodes
    
        data += self.export_beams()
        data += self.export_cameras()
        data += self.export_cinecams()
        data += self.export_wheels()
        data += self.export_shocks()
        data += self.export_commands()
        data += self.export_hydros()
        data += self.export_slidenodes()
        data += self.export_submeshes()
        data += self.export_contacters()
        data += "\nend\n"
        
        self.rotate_all_to_max()
        
        data = ColumnAligner.RoRColumnAligner().ror_align_by_column(data)
        
        print data
        
    def export_global_data(self):
        """Exports all data that is not associated with a specific max object.
        """
        global_data_boxes = self.get_objects_by_name("global_data")
        return ExportGlobalData.generate_global_data(global_data_boxes)
            
    def export_nodes(self):
        beam_objects = self.get_objects_by_name("beam")
        beam_objects = sorted(beam_objects, None, lambda b: b.name)
        exporter = ExportNode.NodeExporter(beam_objects)
        self.nodes = exporter.nodes
        return exporter.render_nodes()
        
    def export_beams(self):
        beam_objects = self.get_objects_by_name("beam")
        return ExportBeam.generate_beams(beam_objects, self.nodes)
    
    def export_cameras(self):
        cameras = self.get_objects_by_name("camera_center", "camera_left", "camera_back")
        return ExportCamera.generate_cameras(cameras, self.nodes)
    
    def export_cinecams(self):
        cinecams = self.get_objects_by_name("cinecam")
        return ExportCinecam.generate_cinecams(cinecams, self.nodes)
    
    def export_wheels(self):
        wheels = self.get_objects_by_name("wheel")
        return ExportWheels.generate_wheels(wheels, self.nodes)
    
    def export_shocks(self):
        shocks = self.get_objects_by_name("shock")
        return ExportShocks.generate_shocks(shocks, self.nodes)
    
    def export_commands(self):
        commands = self.get_objects_by_name("command")
        return ExportCommands.generate_commands(commands, self.nodes)
    
    def export_hydros(self):
        hydros = self.get_objects_by_name("hydro")
        return ExportHydros.generate_hydros(hydros, self.nodes)
    
    def export_slidenodes(self):
        slidenodes = self.get_objects_by_name("slidenode")
        return ExportSlidenodes.generate_slidenodes(slidenodes, self.nodes)
    
    def export_submeshes(self):
        submeshes = self.get_objects_by_name("submesh")
        return ExportSubmeshes.generate_submeshes(submeshes, self.nodes)
    
    def export_contacters(self):
        contacters = self.get_objects_by_name("contacter")
        return ExportContacters.generate_contacters(contacters, self.nodes)
        
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