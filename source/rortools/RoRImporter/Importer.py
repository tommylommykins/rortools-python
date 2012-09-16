#TODO: Remove comments from list of beams. Should instead be done by inspection of comment line numbers.
#TODO: set_beam_defaults

from Py3dsMax import mxs

from TruckParser import *
import Names
from BeamObject import *
from BeamObjectSet import *
import GlobalDataBox; reload(GlobalDataBox)

class Importer:
    def __init__(self):
        #Load global RoR data definitions
        mxs.fileIn("rortools/global/definitions.ms")
        self.parser = TruckParser()
        self.parser.load_truck(mxs.getopenfilename())
        self._load_node_positions()
        self._import_global_data()
        self.make_node_beam()
        
    def _load_node_positions(self):
        self.node_positions = [mxs.Point3(n['x'], n['y'], n['z']) for n in self.parser.nodes]

    def make_node_beam(self):
        """Generates the 3ds Max representation of the beams of a truck.
        """
        beam_set = BeamObjectSet("beam_1", {'line': 0, 'spring':-987,
                                            'damp':-1, 'deform':-1,
                                            'break_force': 0 })
        for i, beam in enumerate(self.parser.beams):
            #Create a new beam object if necessary
            if self._new_beam_section_required(beam):
                comment = self._applicable_comment(beam)
                defaults = self._applicable_beam_default(beam)
                beam_set.delete_unused_beam_objects()
                beam_set = BeamObjectSet(comment, defaults)
            
            #Add a beam
            beam_object = beam_set.select_beam_object(beam)
            start_point = self.node_positions[beam['node1']]
            end_point = self.node_positions[beam['node2']]
            beam_object.draw_line(start_point, end_point)
        beam_set.delete_unused_beam_objects() 
            
    def _new_beam_section_required(self, beam):
        if not (self._new_comment_in_beam_section(beam) or
                self._new_beam_default_in_beam_section(beam)):
            return False
        
        self.previous_comment = self._applicable_comment(beam)
        self.previous_beam_default = self._applicable_beam_default(beam)
        return True
        
    def _new_comment_in_beam_section(self, beam):
        """To provide differentiation between beams, whenever a comment is reached in the
        truck file, a new 3dsmax spline object is created. This method detects when a new
        comment has been found. 
        """
        current_comment = self._applicable_comment(beam)
        if not hasattr(self, "previous_comment"):
            self.previous_comment = current_comment
            return True
        
        if self.previous_comment == current_comment:
            return False
        
        self.previous_comment = current_comment
        return True
    
    def _applicable_comment(self, beam):
        """Gets previous comment relative to the line of the specified beam in the truck file.
        """
        if not hasattr(self.parser, "comments"): return None
        specified_line = beam['line']
        sorted_comments = sorted(self.parser.comments, key=lambda comment: comment['line_no'])
        for comment in reversed(sorted_comments):
            if comment['line_no'] < specified_line: return comment['text']
        return None
        
    def _new_beam_default_in_beam_section(self, beam):
        """To correctly implement set_beam_defaults, a new set of beam objects must be created
        whenever a new set_beam_defaults appears. This method detects when the new defaults has
        appeared."""
        current_default = self._applicable_beam_default(beam)
        if not hasattr(self, "previous_beam_default"):
            self.previous_beam_default = current_default
            return True
        
        if self.previous_beam_default == current_default:
            return False
        
        self.previous_beam_default = current_default
        return True 
    
    def _applicable_beam_default(self, beam):
        """Gets the set_beam_defaults entry which is is effect at the line specified
        Returns None if there is no set_beam_defaults at before the line."""
        if not hasattr(self.parser, "beam_defaults"): return None
        specified_line = beam['line']
        sorted_defaults = sorted(self.parser.beam_defaults, key=lambda default: default['line'])
        for default in reversed(sorted_defaults):
            if default['line'] < specified_line:
                return default
            
                 
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
