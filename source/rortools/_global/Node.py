import math
from Py3dsMax import mxs

class Node(object):
    #Class used for storing positions 
    def __init__(self, coords):
        """Creates an object representing a set of coordinates in 3d space.
        """
        self.separation_category = None
        if coords.__class__.__name__ == "value_wrapper":
            coords = str(coords)
            coords = map(lambda num: float(num), coords[1:-1].split(","))
        elif coords.__class__ == str:
            coords = map(lambda num: float(num), coords[1:-1].split(","))
        
        self.x = float(coords[0])
        self.y = float(coords[1])
        self.z = float(coords[2])
        
    def __cmp__(self, other):
        #For pairwise ordering. Sort by X, then Y, then Z
        if self.x > other.x:
            return 1
        if self.x < other.x:
            return -1
        
        if self.y > other.y:
            return 1
        if self.y < other.y:
            return -1
        
        if self.z > other.z:
            return 1
        if self.z < other.z:
            return -1
        return 0
            
    def distance_to(self, other_position):
        return math.sqrt(
            ((self.x - other_position.x) ** 2) +
            ((self.y - other_position.y) ** 2) +
            ((self.z - other_position.z) ** 2))
        
    def __eq__(self, other):
        return self._key() == other._key()
    
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def to_point3(self):
        return mxs.point3(self.x, self.y, self.z)
    
    def _key(self):
        return (self.x, self.y, self.z)
    
    def __hash__(self):
        return self._key().__hash__()