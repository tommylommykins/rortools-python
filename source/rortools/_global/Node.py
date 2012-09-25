import Position; reload(Position)

class Node(Position.Position):
    #Class used for storing positions 
    def __init__(self, position):
        Position.Position.__init__(self,  position)