import GroupBy; reload(GroupBy)

from .._global import Wheel

def import_wheels(node_positions, wheels, object_holder):
    print "importing wheels"
    group_helper = GroupBy.DictHelper()
    group_helper.dont_autocompare = ['node1', 'node2', 'rigidity_node', 'reference_node']
    grouped_wheels = GroupBy.group_by_comparison_function(group_helper.perform_camparison, wheels)
    for wheel_group in grouped_wheels:
        import_wheel(node_positions, wheel_group, object_holder)
        
def import_wheel(node_positions, wheel_group, object_holder):
    for i, wheel in enumerate(wheel_group):
        node1 = node_positions[wheel['node1']]
        node2 = node_positions[wheel['node1']]
        print "importing a wheel"
        #Wheel.Wheel(i, node1, node2, wheel)