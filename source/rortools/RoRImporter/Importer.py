#TODO: Remove comments from list of beams. Should instead be done by inspection of comment line numbers.
#TODO: set_beam_defaults

from Py3dsMax import mxs

import TruckParser
import ImportBeams
import ImportWheels
import ImportShocks

from .._global import MaxObjHolder
from .._global import Node
from ..MaxObjects import GlobalDataBox
from ..MaxObjects import Camera
from ..MaxObjects import Cinecam

class Importer:
    def __init__(self, truck_file=None):
        #Load global RoR data definitions
        mxs.fileIn("rortools/_global/definitions.ms")
        parser = TruckParser.TruckParser()
        if truck_file is None:
            truck_file = mxs.getopenfilename()
        parser.load_truck(truck_file)
        
        object_holder = MaxObjHolder.MaxObjHolder()
        
        node_positions = self.load_node_positions(parser.nodes)
        self.import_global_data(parser.truck_name, parser.global_data, object_holder)
        self.import_beams(node_positions, parser.beams, parser.comments, parser.beam_defaults, object_holder)
        self.import_cameras(node_positions, parser.cameras, object_holder)
        self.import_cinecams(node_positions, parser.cinecams, object_holder)
        ImportWheels.import_wheels(node_positions, parser.wheels, object_holder)
        ImportShocks.import_shocks(node_positions, parser.shocks, object_holder)
        
        object_holder.rotate_from_ror_to_max()
        
    def load_node_positions(self, nodes):
        node_positions = []
        for n in nodes:
            node_positions.append(Node.Node([n['x'], n['y'], n['z']]))
        return node_positions
    
    def import_global_data(self, truck_name, global_data, object_holder):
        """Takes truck data which isn't associated with a specific 3ds max object
        (weight, name, author, etc.) and assigns it to a box located at the origin.
        This allows it to be edited and exported later
        """
        #Make the box
        box = GlobalDataBox.GlobalDataBox(truck_name, global_data)
        object_holder.add_object(box.max_object)
    
    def import_beams(self, node_positions, beams, comments, beam_defaults, object_holder):
        ImportBeams.import_beams(node_positions, beams, comments, beam_defaults, object_holder) 

    def import_cameras(self, node_positions, cameras, object_holder):
        for i, c in enumerate(cameras):
            camera = Camera.Camera(i,
                                   node_positions[c['center']],
                                   node_positions[c['back']],
                                   node_positions[c['left']])
            object_holder.add_object(camera.camera_1)
            object_holder.add_object(camera.camera_2)
            object_holder.add_object(camera.camera_3)

    def import_cinecams(self, node_positions, cinecams, object_holder):
        for i, cinecam in enumerate(cinecams):
            position_node = Node.Node([cinecam['x'], cinecam['y'], cinecam['z']])
            connection_nodes = []
            for connection_node in cinecam['nodes']:
                connection_nodes.append(node_positions[connection_node])
            cinecam = Cinecam.Cinecam(position_node, connection_nodes, cinecam)
            cinecam.max_object.name = "cinecam_" + str(i)
            object_holder.add_object(cinecam.max_object)
            
class RoRParseError(Exception):
    def __init__(self, value):
        self.msg = value 
