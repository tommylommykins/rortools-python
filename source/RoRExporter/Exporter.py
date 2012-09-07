from Py3dsMax import mxs
from blur3d.api import Scene

import Node
import FilteredNodeSet

class Exporter(object):
    def __init__(self):
        self.export_beams()
        
    def export_beams(self):
        objects = Scene.instance().objects()
        objects = filter(lambda obj: obj.name().lower().startswith("beam"), objects)
        objects = map (lambda obj: obj._nativePointer, objects)
        self._generate_nodes(objects)
                
    def _generate_nodes(self, beam_objs):
        unfiltered_nodes = self._read_nodes(beam_objs)
        node_set = FilteredNodeSet.FilteredNodeSet(0.1)
        for node in unfiltered_nodes:
            node_set.add_node(node)
            
        for node in node_set.nodes:
            print node.x, node.y, node.z
        
    def _read_nodes(self, beam_objs):
        knots = []
        for beam_obj in beam_objs:
            #print mxs.pyhelper.namify(beam_obj.name)
            for spline_no in range(mxs.numsplines(beam_obj)):
                spline_no += 1
                for knot_no in range(mxs.numknots(beam_obj, spline_no)):
                    knot_no += 1
                    knots.append(mxs.getKnotPoint(beam_obj, spline_no, knot_no))
        return sorted(map(Node.Node, knots))
    