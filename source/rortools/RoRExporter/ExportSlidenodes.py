import NodeLookup
from ..MaxObjects import MaxObjectCustAttribute

from Py3dsMax import mxs

import re

class Slidenode(NodeLookup.NodeLookup,
              MaxObjectCustAttribute.MaxObjectCustAttribute):
    def __init__(self, slider, rails, nodes):
        NodeLookup.NodeLookup.__init__(self)
        MaxObjectCustAttribute.MaxObjectCustAttribute.__init__(self) #watch out -- might assume has max_object
        self.slider = slider; self.max_object = slider
        self.rails = rails
        self.nodes = nodes
        
    def render(self):
        if not self.has_custattribute("slidenodestype:slidenodestype"):
            mxs.custattributes.add(self.max_object, mxs.rorslidenode)
        
        ret = ""
        ret += str(self.nodes.index(self.nearest_node(self.slider.pos)))
        for node in self.rails:
            ret += ", " + str(self.nodes.index(self.nearest_node(node.pos)))
        ret += ", s" + str(self.slider.spring)
        if not self.slider.break_amount < 0:
            ret += ", b" + str(self.slider.break_amount)
        ret += ", t" + str(self.slider.tolerence)
        ret += "\n"
        return ret 
    
def generate_slidenodes(slidenodes, nodes):
    if not slidenodes:
        return ""
    ret = "slidenodes\n"
    slidenodes = _partition_slidenodes_by_name(slidenodes)
    slidenodes = map(_partition_individual_slidenode_by_name, slidenodes)
    for slidenode in slidenodes:
        ret += Slidenode(slidenode['slider'], slidenode['rails'], nodes).render()
    return ret + "\n"

def _partition_slidenodes_by_name(slidenodes):
    """Exporter passes in an unsorted set of slidenode boxes.
    This function groups slidenodes according to the text in between the underscores in their name.
    """
    groups = {}
    for slidenode in slidenodes:
        name = re.findall(r'(?<=_).*?(?=_)', slidenode.name)[0]
        if name not in groups:
            groups[name] = []
        groups[name].append(slidenode)
    return groups.values()
    
def _partition_individual_slidenode_by_name(slidenode):
    """slidenodes are categorized into a slider node and a group of rail nodes
    """
    ret = {}
    ret['rails'] = []
    for box in slidenode:
        if box.name.lower().endswith("slider"):
            ret['slider'] = box
        else:
            ret['rails'].append(box)
    return ret





