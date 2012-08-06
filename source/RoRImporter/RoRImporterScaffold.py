from RoRImporter import TruckParser

import sys
import pprint

if len(sys.argv) != 2: raise Exception("Wrong number of arguments")


class RoRImporterScaffold(object):
    def __init__(self):
        self.parser = TruckParser.TruckParser()
        self.parser.load_truck(sys.argv[1])
        pprint.pprint(self.parser.meshwheels2)

        
RoRImporterScaffold()