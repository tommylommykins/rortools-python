from ..MaxObjects import Camera

def import_cameras(node_positions, cameras, object_holder):
    for i, c in enumerate(cameras):
        camera = Camera.Camera(i,
                               node_positions[c['center']],
                               node_positions[c['back']],
                               node_positions[c['left']])
        object_holder.add_object(camera.camera_1)
        object_holder.add_object(camera.camera_2)
        object_holder.add_object(camera.camera_3)