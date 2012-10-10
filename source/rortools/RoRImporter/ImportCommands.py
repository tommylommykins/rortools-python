import GroupBy

from ..MaxObjects import Command

def import_commands(node_positions, commands, object_holder):
    group_helper = GroupBy.DictHelper()
    group_helper.dont_autocompare = ['node1', 'node2']
    grouped_commands = GroupBy.group_by_comparison_function(group_helper.perform_camparison, commands)
    for i, command_group in enumerate(grouped_commands):
        import_command(i, node_positions, command_group, object_holder)
        
def import_command(counter, node_positions, command_group, object_holder):
    node_pairs = []
    for command in command_group:
        temp = []
        node_pairs.append(temp)
        temp.append(node_positions[command['node1']])
        temp.append(node_positions[command['node2']])
    command = Command.Command(node_pairs, command_group[0])
    command.name = "command_" + str(counter)
    object_holder.add_object(command.max_object)