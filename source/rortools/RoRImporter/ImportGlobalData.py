from ..MaxObjects import GlobalDataBox

def import_global_data(truck_name, global_data, object_holder):
    """Takes truck data which isn't associated with a specific 3ds max object
    (weight, name, author, etc.) and assigns it to a box located at the origin.
    This allows it to be edited and exported later
    """
    #Make the box
    box = GlobalDataBox.GlobalDataBox(truck_name, global_data)
    object_holder.add_object(box.max_object)