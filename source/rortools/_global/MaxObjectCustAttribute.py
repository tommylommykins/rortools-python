from Py3dsMax import mxs

class MaxObjectCustAttribute(object):
    """Helper methods for dealing with 3dsmax's custattributes
    """
    def has_custattribute(self, custattribute):
        custattribute_count = mxs.CustAttributes.count(self.max_object)
        if custattribute_count == 0:
            return False
        for i in range(1, custattribute_count + 1):
            if str(mxs.CustAttributes.get(self.max_object, i)) == custattribute:
                return True
        return False
    
    def set_custattribute_by_dict(self, dict):
        """sets the custattributes of self.max_object by assigning the
        values of the dict to the keys.
        If a custattribute which adds properties x and foo is applied to self.max_object
        then they can be set quickly be calling self.set_custattribute_by_dict({"x": 1, "foo": bar})
        """
        for key, value in dict.items():
            setattr(self.max_object, key, value)