from Py3dsMax import mxs
from blur3d.api import Scene

import Node
import Beam


class Exporter(object):
    def __init__(self):
        self.export_nodes()
        self.export_beams()
        
    def export_nodes(self):
        beam_objects = self.get_objects_by_name("beam")
        beam_objects = sorted(beam_objects, None, lambda b: b.name)
        self.nodes = Node.generate_nodes(beam_objects)
        for i, node in enumerate(self.nodes):
            print str(i) + ", " + str(node.position.x) + ", " + str(node.position.y) + ", " + str(node.position.z)
        
    def export_beams(self):
        beam_objects = self.get_objects_by_name("beam")
        Beam.generate_beams(beam_objects, self.nodes)
        
    def get_objects_by_name(self, name):
        objects = Scene.instance().objects()
        named_objects = filter(lambda obj: obj.name().lower().startswith(name), objects)
        native_named_objects = map(lambda obj: obj._nativePointer, named_objects)
        return native_named_objects