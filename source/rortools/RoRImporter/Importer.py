#TODO: Remove comments from list of beams. Should instead be done by inspection of comment line numbers.
#TODO: set_beam_defaults

from Py3dsMax import mxs

import TruckParser; reload(TruckParser)
import ImportBeams; reload(ImportBeams)
import Beam; reload(Beam)
import GlobalDataBox; reload(GlobalDataBox)
import Camera; reload(Camera)
from .._global import MaxObjHolder as MaxObjHolder

class Importer:
    def __init__(self, truck_file=None):
        #Load global RoR data definitions
        mxs.fileIn("rortools/_global/definitions.ms")
        self.parser = TruckParser.TruckParser()
        if truck_file is None:
            truck_file = mxs.getopenfilename()
        self.parser.load_truck(truck_file)
        
        object_holder = MaxObjHolder.MaxObjHolder()
        
        self._load_node_positions()
        self._import_global_data(object_holder)
        builder = ImportBeams.BeamObjectBuilder()
        builder.make_node_beam(self.node_positions, self.parser.beams, self.parser.comments, self.parser.beam_defaults, object_holder)
        self.import_cameras(object_holder)
        
        object_holder.rotate_from_ror_to_max()
        
    def _load_node_positions(self):
        self.node_positions = [mxs.Point3(n['x'], n['y'], n['z']) for n in self.parser.nodes]
        
    def import_cameras(self, object_holder):
        for i, c in enumerate(self.parser.cameras):
            Camera.Camera(i,
                          self.node_positions[c['center']],
                          self.node_positions[c['back']],
                          self.node_positions[c['left']],
                          object_holder)

    def _import_global_data(self, object_holder):
        """Takes truck data which isn't associated with a specific 3ds max object
        (weight, name, author, etc.) and assigns it to a box located at the origin.
        This allows it to be edited and exported later
        """
        #Make the box
        GlobalDataBox.GlobalDataBox(self.parser.truck_name, self.parser.global_data, object_holder)
    
    def _spline_shape(self, name):
        """Generates an empty 3ds max splineshape"""
        return mxs.SplineShape(pos=mxs.Point3(0, 0, 0), name=name)

class RoRParseError(Exception):
    def __init__(self, value):
        self.msg = value 
