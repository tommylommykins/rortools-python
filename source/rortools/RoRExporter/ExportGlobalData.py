from .._global import MaxObjectCustAttribute

from ..RoRImporter import GlobalDataBox

class GlobalData(MaxObjectCustAttribute.MaxObjectCustAttribute):
    def __init__(self, max_object):
        self.max_object = max_object
        
    def render(self):
        return self.max_object.global_data
        
def generate_global_data(global_boxes):
    if not global_boxes:
        #use default data if there is no box 
        default_data = open("rortools/_global/default_global_data.txt").read()
        box = GlobalDataBox.GlobalDataBox("MyTruck", default_data)
        return GlobalData(box.max_object).render()
    else:
        return GlobalData(global_boxes[0]).render()