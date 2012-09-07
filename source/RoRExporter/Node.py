class Node(object):
    def __init__(self, position_string):
        self.position = self._knot_to_array(position_string)
    
    def _knot_to_array(self, knot):
        arr = map(lambda num: float(num), str(knot)[1:-1].split(","))
        self.x = arr[0]
        self.y = arr[1]
        self.z = arr[2]
    
    def __cmp__(self, other):
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
    
