import Position; reload(Position)

class Node(object):
    #Class used for storing positions 
    def __init__(self, position_string=None, coord_list=None):
        if position_string is not None:
            coords = map(lambda num: float(num), position_string[1:-1].split(","))
            self.position = Position.Position(coords)
        else:
            self.position = Position.Position(coord_list)
    
    def __cmp__(self, other):
        #For pairwise ordering. Sort by X, then Y, then Z
        if self.position.x > other.position.x:
            return 1
        if self.position.x < other.position.x:
            return -1
        
        if self.position.y > other.position.y:
            return 1
        if self.position.y < other.position.y:
            return -1
        
        if self.position.z > other.position.z:
            return 1
        if self.position.z < other.position.z:
            return -1
        return 0