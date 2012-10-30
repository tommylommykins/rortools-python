#TODO: Remove comments from list of beams. Should instead be done by inspection of comment line numbers.
#TODO: set_beam_defaults

from Py3dsMax import mxs

import TruckParser
import ImportNodes
import ImportGlobalData
import ImportBeams
import ImportCameras
import ImportCinecams
import ImportWheels
import ImportShocks
import ImportCommands
import ImportHydros
import ImportSlidenodes
import ImportSubmeshes
import ImportContacters

from .._global import MaxObjHolder

class Importer:
    def __init__(self, truck_file=None):
        #Load global RoR data definitions
        mxs.fileIn("rortools/_global/definitions.ms")
        parser = TruckParser.TruckParser()
        if truck_file is None:
            truck_file = mxs.getopenfilename()
        parser.load_truck(truck_file)
        
        object_holder = MaxObjHolder.MaxObjHolder()
        
        node_positions = ImportNodes.load_node_positions(parser.nodes, object_holder)
        
        ImportGlobalData.import_global_data(parser.truck_name, parser.global_data, object_holder)
        ImportBeams.import_beams(node_positions, parser.beams, parser.comments, parser.beam_defaults, object_holder)
        ImportCameras.import_cameras(node_positions, parser.cameras, object_holder)
        ImportCinecams.import_cinecams(node_positions, parser.cinecams, object_holder)
        ImportWheels.import_wheels(node_positions, parser.wheels, object_holder)
        ImportShocks.import_shocks(node_positions, parser.shocks, object_holder)
        ImportCommands.import_commands(node_positions, parser.commands, object_holder)
        ImportHydros.import_hydros(node_positions, parser.hydros, object_holder)
        ImportSlidenodes.import_slidenodes(node_positions, parser.slidenodes, object_holder)
        ImportSubmeshes.import_submeshes(node_positions, parser.submeshes, parser.cabs, parser.texcoords, parser.backmeshes, object_holder)
        ImportContacters.import_contacters(node_positions, parser.contacters, object_holder)
        object_holder.rotate_from_ror_to_max()
     
class RoRParseError(Exception):
    def __init__(self, value):
        self.msg = value 
