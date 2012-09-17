from Py3dsMax import mxs

import Names

class BeamThing(object):
    def __init__(self):
        self.max_object = self._spline_shape("spline_shape")
    
    def _get_name(self):
        return self.max_object.name
    
    def _set_name(self, name):
        self.max_object.name = name
    
    name = property(_get_name, _set_name)
        
    def _spline_shape(self, name):
        """Generates an empty 3ds max splineshape"""
        return mxs.SplineShape(pos=mxs.Point3(0, 0, 0), name=name)
    
    def draw_line(self, pos1, pos2):
        """Draws a line between two points of a line object
        """
        beam_object = self.max_object
        spline = mxs.AddNewSpline(beam_object)
        mxs.AddKnot(beam_object, spline, Names.CORNER, Names.LINE, pos1)
        mxs.AddKnot(beam_object, spline, Names.CORNER, Names.LINE, pos2)
        mxs.UpdateShape(beam_object)