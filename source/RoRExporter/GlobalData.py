import MaxObjectCustAttribute; reload(MaxObjectCustAttribute)

class GlobalData(MaxObjectCustAttribute.MaxObjectCustAttribute):
    def __init__(self, max_object):
        self.max_object = max_object
        
    def render(self):
        pass