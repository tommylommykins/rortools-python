from Py3dsMax import mxs

class MaxObjHolder(object):
    def __init__(self, max_objects=None):
        self.mxs_objects = []
        if max_objects is not None:
            self.mxs_objects += max_objects
        
    def add_object(self, max_object):
        self.mxs_objects.append(max_object)
        
    def rotate_from_ror_to_max(self):
        angle1 = mxs.angleaxis(90, mxs.point3(1, 0, 0))
        angle2 = mxs.angleaxis(90, mxs.point3(0, 0, 1))
        for obj in self.mxs_objects:
            self._rotate(obj, angle1)
            self._rotate(obj, angle2)
            self._swap_pivot_x_and_y(obj)
                    
    def rotate_from_max_to_ror(self):
        angle1 = mxs.angleaxis(-90, mxs.point3(0, 1, 0))
        angle2 = mxs.angleaxis(-90, mxs.point3(0,0,1))
        for obj in self.mxs_objects:
            self._rotate(obj, angle1)
            self._rotate(obj, angle2)
            self._swap_pivot_x_and_y(obj)
            
    def _swap_pivot_x_and_y(self, object):
        try:
            original_x = object.pivot.x
            original_y = object.pivot.y
            original_z = object.pivot.z
            object.pivot = mxs.point3(original_y, original_x, original_z)
        except:
            print "failed to move pivot point for " + str(object)
    
    def _rotate(self, object, angle):
        try:
            original_pivot = object.pivot
            object.pivot = mxs.point3(0, 0, 0)
            mxs.rotate(object, angle)
            object.pivot = original_pivot
        except:
            print "failed to rotate " + str(object) 
            
            
    def delete_all(self):
        for obj in self.mxs_objects:
            try:
                mxs.delete(obj)
            except:
                print "failed to delete " + str(obj)