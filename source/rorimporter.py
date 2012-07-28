import re

from Py3dsMax import mxs

from RoRImporter import *

def point3(lst):
    mxs.Point3(lst[0], lst[1], lst[2])

class Importer:
    def __init__(self):
        self.reader =  TruckFileReader.TruckFileReader()
        self.reader.load_truck(mxs.getopenfilename())
        self.draw_nodes()

    def draw_nodes(self):
        nodes = self.reader.nodes
        for node in nodes:
            pos = [node['x'], node['y'], node['z']]
            s = mxs.Sphere(radius = 0.1)
            s.pos = mxs.Point3(node['x'], node['y'], node['z'])
    
Importer()