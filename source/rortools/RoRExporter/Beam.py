from Py3dsMax import mxs

import Position
import MaxObjectCustAttribute; reload(MaxObjectCustAttribute)

class Beam(MaxObjectCustAttribute.MaxObjectCustAttribute):
    """A class for exporting the beams of a truck."""
    def __init__(self, max_object, nodes):
        self.nodes = nodes
        self.max_object = max_object
        self._split_lines()
        
    def render(self):
        """Generates the truck file representation of the 3ds max beam object. 
        """
        ret = ""
        ret += self._render_beam_header()
        for positions in self.beam_positions():
            ret += self._render_individual_beam(positions[0], positions[1]) + "\n"
        return ret
    
    def beam_positions(self):
        num_splines = mxs.numsplines(self.max_object)
        for spline_no in range(1, num_splines + 1):
            num_knots = mxs.numknots(self.max_object, spline_no)
            knot_pair = []
            for knot_no in range(1, num_knots + 1):
                pass
                pos = (Position.Position(str(mxs.getKnotPoint(self.max_object, spline_no, knot_no))))
                knot_pair.append(pos)
            yield knot_pair
    
    def _render_beam_header(self):
        ret = "\n;" + self.max_object.name + "\n"
        ret += self._render_set_beam_defaults() + "\n"
        return ret
            
    def _render_set_beam_defaults(self):
        if not self.has_custattribute(mxs.RoRBeam):
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
        node1 = self._closest_node(pos1)
        index1 = self.nodes.index(node1)
        
        node2 = self._closest_node(pos2)
        index2 = self.nodes.index(node2)
        
        return str(index1) + ", " + str(index2) + self._render_beam_flags()
    
    def _render_beam_flags(self):
        ret = ""
        if self.max_object.invisible: ret += "i"
        if self.max_object.rope: ret += "r"
        if self.max_object.support: ret += "s"
        #support length not yet supported? D:
        if not ret: return ""
        return ", " + ret
        
    def _closest_node(self, pos):
        the_lambda = lambda acc, candidate: self._closer_node_to_pos(acc, candidate, pos)
        return reduce(the_lambda, self.nodes, self.nodes[0])
    
    def _closer_node_to_pos(self, node1, node2, pos):
        node1_distance = node1.position.distance_to(pos)
        node2_distance = node2.position.distance_to(pos)
        if node1_distance < node2_distance:
            return node1
        else:
            return node2
    
    def _split_lines(self):
        """forces all the splines of an editable spline object to be one segment long
        the method is defined in pure maxscript, so if it is not defined then it needs to be
        loaded.
        """
        if not mxs.SplitBeam.__class__.__name__ == "value_wrapper":
            mxs.fileIn("rortools/RoRExporter/splitbeam.ms")
        mxs.SplitBeam(self.max_object)

def generate_beams(beams, nodes):
    print "beams"
    beams = map(lambda beam: Beam(beam, nodes), beams)
    for beam in beams:
        print beam.render()
        