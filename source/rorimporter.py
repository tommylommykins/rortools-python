import re

from Py3dsMax import mxs

from RoRImporter import TruckFileReader
reload(TruckFileReader)

#def point3(lst):
#    mxs.Point3(lst[0], lst[1], lst[2])

class Importer:
    def __init__(self):
        self.reader =  TruckFileReader.TruckFileReader()
        self.reader.load_truck(mxs.getopenfilename())
        self.make_node_beam()

    def make_node_beam(self):
        nodes = self.reader.nodes
        positions = [mxs.Point3(n.x, n.y, n.z) for n in nodes]
        
        beams = self.reader.beams

        beam_object = mxs.SplineShape(pos=mxs.Point3(0,0,0), name="beam_1")
        for beam in beams:
            current_spline = mxs.AddNewSpline(beam_object)
            mxs.AddKnot(beam_object, current_spline, mxs.pyhelper.namify("corner"), mxs.pyhelper.namify("line"), positions[beam.node1])
            mxs.AddKnot(beam_object, current_spline, mxs.pyhelper.namify("corner"), mxs.pyhelper.namify("line"), positions[beam.node2])
            mxs.UpdateShape(beam_object)
        mxs.UpdateShape(beam_object)

class RoRParseError(Exception):
    def __init__(self, value):
        self.msg = value

Importer()