import GroupBy

from ..MaxObjects import Hydro

def import_hydros(node_positions, hydros, object_holder):
    group_helper = GroupBy.DictHelper()
    group_helper.dont_autocompare = ['node1', 'node2']
    grouped_hydros = GroupBy.group_by_comparison_function(group_helper.perform_camparison, hydros)
    for i, hydro_group in enumerate(grouped_hydros):
        import_hydro(i, node_positions, hydro_group, object_holder)
        
def import_hydro(counter, node_positions, hydro_group, object_holder):
    node_pairs = []
    for hydro in hydro_group:
        temp = []
        node_pairs.append(temp)
        temp.append(node_positions[hydro['node1']])
        temp.append(node_positions[hydro['node2']])
    hydro = Hydro.Hydro(node_pairs, hydro_group[0])
    hydro.name = "hydro_" + str(counter)
    object_holder.add_object(hydro.max_object)