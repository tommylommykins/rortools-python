import re

from Py3dsMax import mxs

from .._global import Position; reload(Position)
import Node; reload(Node)
import NodeLookup; reload(NodeLookup)

from .._global import Camera as ImporterCamera

class Camera(NodeLookup.NodeLookup):
    def __init__(self, center, back, left, nodes):
        self.center = center
        self.back = back
        self.left = left
        self.nodes = nodes
    
    def render(self):
        center_node = self.nearest_node(self.center.pos)
        center_index = str(self.nodes.index(center_node))
        back_node = self.nearest_node(self.back.pos)
        back_index = str(self.nodes.index(back_node))
        left_node = self.nearest_node(self.left.pos)
        left_index = str(self.nodes.index(left_node))
        return center_index + ", " + back_index + ", " + left_index
    
def generate_cameras(cameras, nodes):
    ret = "cameras\n"
    for camera_no in range(max_camera(cameras) + 1):
        selected_cameras = select_cameras(camera_no, cameras)
        if not cameras:
            continue
        c = selected_cameras
        ret += Camera(c[0], c[1], c[2], nodes).render() + "\n"
    if len(ret.split("\n")) < 3:
        return generate_default_cameras(cameras, nodes)
    return ret + "\n"

def generate_default_cameras(cameras, nodes):
    map(lambda camera: mxs.delete(camera), cameras)
    positions = []
    for node_no in range(3):
        node_pos = nodes[node_no].position
        positions.append(mxs.Point3(node_pos.x, node_pos.y, node_pos.z))
    ImporterCamera.Camera(0, positions[0], positions[1], positions[2])
    return "cameras\n0,1,2"
    
def max_camera(cameras):
    camera_numbers = map(lambda camera: re.findall(r'\d$', camera.name), cameras)
    camera_numbers = filter(None, camera_numbers)
    camera_numbers = map(lambda number: int(number[0]), camera_numbers)
    if not camera_numbers: return 0
    return max(camera_numbers)

def select_cameras(camera_no, cameras):
    candidate_set = [camera for camera in cameras if re.search(str(camera_no), camera.name)]
    if len(candidate_set) != 3:
        print "failed to find 3 different camera objects for camera set " + str(camera_no)
        print "got" + str([camera.name for camera in candidate_set])
        return False
    
    center_camera = None
    back_camera = None
    left_camera = None
    for camera in candidate_set:
        if camera.name.startswith("camera_center"): center_camera = camera
        if camera.name.startswith("camera_back"): back_camera = camera
        if camera.name.startswith("camera_left"): left_camera = camera
        
    ret = [center_camera, back_camera, left_camera]
    if len(filter(None, ret)) != 3:
        if center_camera is None: print "failed to find center camera for camera set" + str(camera_no)
        if back_camera is None: print "failed to find back camera for camera set" + str(camera_no)
        if left_camera is None: print "failed to find left camera for camera set" + str(camera_no)
    return ret