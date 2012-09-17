#TODO: Remove comments from list of beams. Should instead be done by inspection of comment line numbers.
#TODO: set_beam_defaults

from Py3dsMax import mxs

import TruckParser; reload(TruckParser)
import Names
import ImportBeams; reload(ImportBeams)
from BeamObject import *
from BeamObjectSet import *
import GlobalDataBox; reload(GlobalDataBox)
import Camera; reload(Camera)

class Importer:
    def __init__(self, truck_file=None):
        #Load global RoR data definitions
        mxs.fileIn("rortools/global/definitions.ms")
        self.parser = TruckParser.TruckParser()
        if truck_file is None:
            truck_file = mxs.getopenfilename()
        self.parser.load_truck(truck_file)
        self._load_node_positions()
        self._import_global_data()
        builder = Beam.BeamObjectBuilder()
        builder.make_node_beam(self.node_positions, self.parser.beams, self.parser.comments, self.parser.beam_defaults)
        self.import_cameras()
        
    def _load_node_positions(self):
        self.node_positions = [mxs.Point3(n['x'], n['y'], n['z']) for n in self.parser.nodes]
        
    def import_cameras(self):
        for i, c in enumerate(self.parser.cameras):
            Camera.Camera(i,
                          self.node_positions[c['center']],
                          self.node_positions[c['back']],
                          self.node_positions[c['left']])

    def _import_global_data(self):
        """Takes truck data which isn't associated with a specific 3ds max object
        (weight, name, author, etc.) and assigns it to a box located at the origin.
        This allows it to be edited and exported later
        """
        #Make the box
        GlobalDataBox.GlobalDataBox(self.parser.truck_name, self.parser.global_data)
    
    def _spline_shape(self, name):
        """Generates an empty 3ds max splineshape"""
        return mxs.SplineShape(pos=mxs.Point3(0, 0, 0), name=name)

class RoRParseError(Exception):
    def __init__(self, value):
        self.msg = value 
