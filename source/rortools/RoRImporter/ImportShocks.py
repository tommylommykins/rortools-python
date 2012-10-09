import GroupBy

from .._global import Shock

def import_shocks(node_positions, shocks, object_holder):
    group_helper = GroupBy.DictHelper()
    group_helper.dont_autocompare = ['node1', 'node2']
    grouped_shocks = GroupBy.group_by_comparison_function(group_helper.perform_camparison, shocks)
    for i, shock_group in enumerate(grouped_shocks):
        import_shock(i, node_positions, shock_group, object_holder)
        
def import_shock(counter, node_positions, shock_group, object_holder):
    node_pairs = []
    for shock in shock_group:
        temp = []
        node_pairs.append(temp)
        temp.append(node_positions[shock['node1']])
        temp.append(node_positions[shock['node2']])
    shock = Shock.Shock(node_pairs, shock_group[0])
    shock.name = "shock_" + str(counter)
    object_holder.add_object(shock.max_object)