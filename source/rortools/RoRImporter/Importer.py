#TODO: Remove comments from list of beams. Should instead be done by inspection of comment line numbers.
#TODO: set_beam_defaults

from Py3dsMax import mxs

import TruckParser; reload(TruckParser)
import ImportBeams; reload(ImportBeams)
import GlobalDataBox; reload(GlobalDataBox)

from .._global import MaxObjHolder as MaxObjHolder; reload(MaxObjHolder)
from .._global import Node as Node; reload(Node)
from .._global import Camera; reload(Camera)
from .._global import Cinecam as Cinecam; reload(Cinecam)

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
        self.import_cinecams(object_holder)
        
        object_holder.rotate_from_ror_to_max()
        
    def _load_node_positions(self):
        self.node_positions = []
        for n in self.parser.nodes:
            self.node_positions.append(Node.Node([n['x'], n['y'], n['z']])) 

    def import_cameras(self, object_holder):
        for i, c in enumerate(self.parser.cameras):
            camera = Camera.Camera(i,
                                   self.node_positions[c['center']],
                                   self.node_positions[c['back']],
                                   self.node_positions[c['left']])
            object_holder.add_object(camera.camera_1)
            object_holder.add_object(camera.camera_2)
            object_holder.add_object(camera.camera_3)

    def import_cinecams(self, object_holder):
        for i, cinecam in enumerate(self.parser.cinecams):
            position_node = Node.Node([cinecam['x'], cinecam['y'], cinecam['z']])
            connection_nodes = []
            for connection_node in cinecam['nodes']:
                connection_nodes.append(self.node_positions[connection_node])
            spring = None
            if "spring" in cinecam: spring = cinecam['spring']
            damp = None
            if "damp" in cinecam: damp = cinecam['damp']
            cinecam = Cinecam.Cinecam(i, position_node, connection_nodes, spring, damp)
            object_holder.add_object(cinecam.max_object)

    def _import_global_data(self, object_holder):
        """Takes truck data which isn't associated with a specific 3ds max object
        (weight, name, author, etc.) and assigns it to a box located at the origin.
        This allows it to be edited and exported later
        """
        #Make the box
        box = GlobalDataBox.GlobalDataBox(self.parser.truck_name, self.parser.global_data)
        object_holder.add_object(box.max_object)
    
    def _spline_shape(self, name):
        """Generates an empty 3ds max splineshape"""
        return mxs.SplineShape(pos=mxs.Point3(0, 0, 0), name=name)

class RoRParseError(Exception):
    def __init__(self, value):
        self.msg = value 
