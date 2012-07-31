from RoRImporter import TruckFileReader

class RoRImporterScaffold(object):
    def __init__(self):
        self.importer = TruckFileReader.TruckFileReader()
        self.importer.load_truck("../test.truck")
        
RoRImporterScaffold()