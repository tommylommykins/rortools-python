from Py3dsMax import mxs

from .._global import Node

class BeamIterable(object):
    """Provides a method for iterating through all the beams of an object's max_object.
    The max_object must be a spline shape
    """
    def all_beams(self):
        """Gets a list of pairs of node objects, representing the positions of
        the nodes of each beam in the beam object
        """
        self._check_is_spline_shape()
        self._split_lines()
        num_splines = mxs.numsplines(self.max_object)
        all_beams = []
        for spline_no in range(1, num_splines + 1):
            num_knots = mxs.numknots(self.max_object, spline_no)
            knot_pair = []
            for knot_no in range(1, num_knots + 1):
                pos_string = str(mxs.getKnotPoint(self.max_object, spline_no, knot_no))
                pos = Node.Node(pos_string)
                knot_pair.append(pos)
            all_beams.append(sorted(knot_pair))
        return sorted(all_beams)
    
    def _split_lines(self):
        """forces all the splines of an editable spline object to be one segment long
        the method is defined in pure maxscript, so if it is not defined then it needs to be
        loaded.
        """
        if not mxs.SplitBeam.__class__.__name__ == "value_wrapper":
            mxs.fileIn("rortools/RoRExporter/splitbeam.ms")
        mxs.SplitBeam(self.max_object)
        
    def _check_is_spline_shape(self):
        """Raises an error if self.max_object is not a 3ds max spline shape
        """
        if not mxs.isshapeobject(self.max_object):
            raise Exception("max object is not a spline shape. Cannot perform spline operations on non-spline shapes")