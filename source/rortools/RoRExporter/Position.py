import math

class Position(object):
    def __init__(self, position_string):
        """Creates an object representing a set of coordinates in 3d space.
        position_string is the string returned by mxs.getknotpoint
        """
        coords = map(lambda num: float(num), position_string[1:-1].split(","))
        self.x = float(coords[0])
        self.y = float(coords[1])
        self.z = float(coords[2])
        
    def distance_to(self, other_position):
        return math.sqrt(((self.x - other_position.x) ** 2) +
            ((self.y - other_position.y) ** 2) +
            ((self.z - other_position.z) ** 2))