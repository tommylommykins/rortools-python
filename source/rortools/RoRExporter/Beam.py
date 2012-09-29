from Py3dsMax import mxs

from .._global import Position
import MaxObjectCustAttribute
import NodeLookup

import re

class Beam(MaxObjectCustAttribute.MaxObjectCustAttribute, NodeLookup.NodeLookup):
    """A class for exporting the beams of a truck."""
    def __init__(self, max_object, nodes):
        self.nodes = nodes
        self.max_object = max_object
        self._split_lines()
        
    def render(self, preexisting_beams):
        """Generates the truck file representation of the 3ds max beam object. 
        """
        ret = ""
        ret += self._render_beam_header()
        unique_beams = self.unique_beams(preexisting_beams)
        for positions in unique_beams:
            ret += self._render_individual_beam(positions[0], positions[1])
        return ret
    
    def unique_beams(self, preexisting_beams):
        """gets the beams in this beam object which are not already in another beam object.
        Also appends those beams to a global list of all beams exported so far
        
        the global list written into the class variable update_preexisting_beams. 
        """
        unique_beams = []
        for node_pair in self.all_beams():
            #Ignore beams starting and ending at the same vertex.
            if len(set(node_pair)) == 1:
                continue
            
            node_pair = tuple(sorted(node_pair))
            if node_pair not in preexisting_beams:
                unique_beams.append(node_pair)
                preexisting_beams.add(node_pair)
        self.updated_preexisting_beams = preexisting_beams
        return unique_beams
    
    def all_beams(self):
        """for each beam in the object. returns the start and end nodes.
        """
        num_splines = mxs.numsplines(self.max_object)
        all_beams = []
        for spline_no in range(1, num_splines + 1):
            num_knots = mxs.numknots(self.max_object, spline_no)
            knot_pair = []
            for knot_no in range(1, num_knots + 1):
                pos_string = str(mxs.getKnotPoint(self.max_object, spline_no, knot_no))
                pos = Position.Position(pos_string[1:-1].split(","))
                knot_pair.append(pos)
            knot_pair = map( lambda knot_pos: self.nodes.index(self.nearest_node(knot_pos)), knot_pair)
            all_beams.append(sorted(knot_pair))
        return sorted(all_beams)
    
    def _render_beam_header(self):
        ret = "\n;" + self.max_object.name + "\n"
        ret += self._render_set_beam_defaults() + "\n"
        return ret
            
    def _render_set_beam_defaults(self):
        if not self.has_custattribute("BeamsType:BeamsType"):
            mxs.CustAttributes.add(self.max_object, mxs.RoRBeam)
        ret = "set_beam_defaults" 
        ret += " "  + str(self.max_object.spring)
        ret += ", " + str(self.max_object.damp)
        ret += ", " + str(self.max_object.deform)
        ret += ", " + str(self.max_object.break_force)
        ret += ", " + str(self.max_object.diameter)
        ret += ", " + str(self.max_object.ror_material)
        ret += ", " + str(self.max_object.deform_plastic)
        return ret
    
    def _render_individual_beam(self, pos1, pos2):        
        return str(pos1) + ", " + str(pos2) + self._render_beam_flags() + "\n"
    
    def _render_beam_flags(self):
        ret = ""
        if self.max_object.invisible: ret += "i"
        if self.max_object.rope: ret += "r"
        if self.max_object.support: ret += "s"
        #support length not yet supported? D:
        if not ret: return ""
        return ", " + ret
    
    def _split_lines(self):
        """forces all the splines of an editable spline object to be one segment long
        the method is defined in pure maxscript, so if it is not defined then it needs to be
        loaded.
        """
        if not mxs.SplitBeam.__class__.__name__ == "value_wrapper":
            mxs.fileIn("rortools/RoRExporter/splitbeam.ms")
        mxs.SplitBeam(self.max_object)

def generate_beams(beams, nodes):
    ret = "beams\n"
    beams = map(lambda beam: Beam(beam, nodes), beams)
    extant_beams = set()
    for beam in beams:
        ret += beam.render(extant_beams) + "\n"
        extant_beams = beam.updated_preexisting_beams
    return ret