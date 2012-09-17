from Py3dsMax import mxs

class MaxObjectCustAttribute(object):
    def has_custattribute(self, custattribute):
        custattribute_count = mxs.CustAttributes.count(self.max_object)
        if custattribute_count == 0:
            return False
        for i in range(1, custattribute_count + 1):
            if str(mxs.CustAttributes.get(self.max_object, i)) == custattribute:
                return True
        return False
    