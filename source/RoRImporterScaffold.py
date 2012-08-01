from RoRImporter import TruckFileReader

import pprint

class RoRImporterScaffold(object):
    def __init__(self):
        self.importer = TruckFileReader.TruckFileReader()
        self.importer.load_truck("C:/Users/thomas.green/Desktop/Aptana/test1/test.truck")
        map(self.pprint_dict, self.importer.meshwheels2)
        
    def pprint_dict(self, obj):
        pprint.pprint(obj.__dict__)
    
        
RoRImporterScaffold()