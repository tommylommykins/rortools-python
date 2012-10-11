import GroupBy

from ..MaxObjects import Wheel
from ..MaxObjects import Box

from Py3dsMax import mxs

def import_wheels(node_positions, wheels, object_holder):
    fix_negative_rigidity_nodes(wheels)
    group_helper = GroupBy.DictHelper()
    group_helper.dont_autocompare = ['node1', 'node2']
    grouped_wheels = GroupBy.group_by_comparison_function(group_helper.perform_camparison, wheels)
    for i, wheel_group in enumerate(grouped_wheels):
        import_wheel(i, node_positions, wheel_group, object_holder)
        
def import_wheel(counter, node_positions, wheel_group, object_holder):
    node_pairs = []
    for wheel in wheel_group:
        temp = []
        node_pairs.append(temp)
        temp.append(node_positions[wheel['node1']])
        temp.append(node_positions[wheel['node2']])
    wheel = Wheel.Wheel(node_pairs, wheel_group[0])
    wheel.name = "wheel_" + str(counter)
    object_holder.add_object(wheel.max_object)
    
    first_wheel = wheel_group[0]
    if first_wheel['rigidity_node'] != 9999:
        rigidity_node = Box.Box(node_positions[first_wheel['rigidity_node']],
                                name="rigidity_node_" + wheel.name,
                                wirecolor=mxs.color(55, 76, 83))
        object_holder.add_object(rigidity_node.max_object)
        
def fix_negative_rigidity_nodes(wheels):
    for wheel in wheels:
        for key, value in wheel.items():
            if key is 'rigidity_node':
                if value < 0:
                    wheel['rigidity_node'] = -value