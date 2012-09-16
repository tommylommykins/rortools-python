from Py3dsMax import mxs

class MaxObjectCustAttribute(object):
    def has_custattribute(self, custattribute):
        try:
            return mxs.CustAttributes.get(self.max_object, custattribute) is not None
        except:
            return False