import math
from Py3dsMax import mxs

class Position(object):
    def __init__(self, coords):
        """Creates an object representing a set of coordinates in 3d space.
        position_string is the string returned by mxs.getknotpoint
        """
        self.x = float(coords[0])
        self.y = float(coords[1])
        self.z = float(coords[2])
            
    def distance_to(self, other_position):
        return math.sqrt(
            ((self.x - other_position.x) ** 2) +
            ((self.y - other_position.y) ** 2) +
            ((self.z - other_position.z) ** 2))
        
    def to_point3(self):
        return mxs.point3(self.x, self.y, self.z)