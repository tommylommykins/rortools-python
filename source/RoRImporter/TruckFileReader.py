import re
import copy

class FileInfo(object):
    def __init__(self, uid = None, cid = None, version = None):
        self.unique_id    = uid
        self.category_id  = cid
        self.file_version = version
        
class ExternalCamera(object):
    def __init__(self, camera_type = None, node = None):
        self.type = camera_type
        self.node = node
        
class SlopeBrake(object):
    def __init__(self, regulating_force = None, attack_angle = None, release_angle = None):
        self.regulating_force = regulating_force
        self.attack_angle = attack_angle
        self.release_angle = release_angle
        
class AntiLockBrakes(object):
    def __init__(self, regulating_force = None, wheel_slip = None, fade_speed = None, pulse_rate = None, mode = None):
        self.regulating_force = regulating_force
        self.wheel_slip = wheel_slip
        self.fade_speed = fade_speed
        self.pulse_rate = pulse_rate
        self.mode = mode
        
class TractionControl(object):
    def __init__(self, regulating_force = None, wheel_slip = None, fade_speed = None, pulse_rate = None, mode = None):
        self.regulating_force = regulating_force
        self.wheel_slip = wheel_slip
        self.fade_speed = fade_speed
        self.pulse_rate = pulse_rate
        self.mode = mode
        
class CruiseControl(object):
    def __init__(self, low_limit = None, autobrake = None):
        self.low_limit = low_limit
        self.autobrake = autobrake

class PropCameraMode(object):
    def __init__(self, line = None, value = None):
        self.line = line
        self.value = value
        
class FlexbodyCameraMode(object):
    def __init__(self, line = None, value = None):
        self.line = line
        self.value = value

class Author(object):
    def __init__(self, author_type = None, author_id = None, name = None, email = None):
        self.type = author_type
        self.id = author_id
        self.name = name
        self.email = email

class AddAnimation(object):
    def __init__(self, ratio = None, option_1 = None, option_2 = None, source = None, mode = None, event = None):
        self.ratio = ratio
        self.option_1 = option_1
        self.option_2 = option_2
        self.source = source
        self.mode = mode
        self.event = event

class SetBeamDefaultsScale(object):
    def __init__(self, line = None, spring = None, damp = None, deform = None, scale_break = None):
        self.line = line
        self.spring = spring
        self.damp = damp
        self.deform = deform
        self.scale_break = scale_break
        
class SetBeamDefaults(object):
    def __init__(self, line = None, spring = None, damp = None, deform = None, break_force = None, diameter = None, material = None,
                 deform_plastic = None):
        self.line = line
        self.spring = spring
        self.damp = damp
        self.deform = deform
        self.break_force = break_force
        self.diameter = diameter
        self.material = material
        self.deform_plastic = deform_plastic

class SetInertiaDefaults(object):
    def __init__(self, line = None, start_delay = None, stop_delay = None, start_function = None, stop_function = None,
                 default_value = None):
        self.line = line
        self.start_delay = start_delay
        self.stop_delay = stop_delay
        self.start_function = start_function
        self.stop_function = stop_function
        self.default_value = default_value

class SetNodeDefaults(object):
    def __init__(self, line = None, load_weight = None, friction = None, volume = None, surface = None, options = None):
        self.line = line
        self.load_weight = load_weight
        self.friction = friction
        self.volume = volume
        self.surface = surface
        self.options = options

class SetSkeletonSettings(object):
    def __init__(self, sight_range = None, beam_diameter = None):
        self.sight_range = sight_range
        self.beam_diameter = beam_diameter

class Node(object):
    def __init__(self, id_no = None, x = None, y = None, z = None, options = None, mass = None):
        self.id = id_no
        self.x = x
        self.y = y
        self.z = z
        self.options = options
        self.mass = mass

class Beam(object):
    def __init__(self, line = None, node1 = None, node2 = None, options = None, support_length = None):
        self.line = line
        self.node1 = node1
        self.node2 = node2
        self.options = options
        self.support_length = support_length
        
class TruckFileReader(object):
    def __init__(self):
        self.define_sections()

    def define_sections(self):
        self.sections = ["NONE", "nodes", "nodes2", "beams", "fixes", "shocks", "hydros", "wheels", "wheels2", "globals", "cameras",
        "engine", "texcoords", "cab", "commands", "commands2", "contacters", "ropes", "ropables", "ties", "help", "cinecam", 
        "flares", "props", "globeams", "wings", "turboprops", "turboprops2", "pistonprops", "fusedrag", "engoption", "brakes", 
        "rotators", "rotators2", "screwprops", "guisettings", "minimass", "exhausts", "particles", "turbojets", "rigidifiers", 
        "airbrakes", "meshwheels", "meshwheels2", "flexbodywheels", "flexbodies", "hookgroup", "materialflarebindings", 
        "soundsources", "soundsources2", "soundsources3", "envmap", "managedmaterials", "BTS_SECTIONCONFIG", "torquecurve", 
        "advdrag", "axles", "shocks2", "triggers", "railgroups", "slidenodes", "flares2", "animators", "nodecollision", 
        "description", "videocamera", "hooks", "lockgroups", "camerarail", "end"]

    #Loads a file. Iterates through it and creates data structures which can later be queried.
    def load_truck(self, truck_file):
        self.parse_truck(truck_file)

    def parse_truck(self, truck_file):
        """Reads a truck file. Incomplete. Sections that are written do not yet correctly
        handle expected data types of input values
        """
        truck_file_contents = open(truck_file).read()

        self.mode = "NONE"
        current_line = -1
        for l in truck_file_contents.splitlines():
            current_line += 1
            line = l.strip()

            #skip blank lines
            if not line:
                continue

            next_line = False
            for section in self.sections:
                if line == section:
                    print "MODE" + self.mode
                    self.mode = section
                    #Note: In the sourcecode, the mode queue is currently never actually used for anything, so
                    #it is not implemented here
                    next_line = True
            if next_line:
                continue

            try:
                self.real_truck_name
            except:
                self.real_truck_name = line
                continue

            if line == "end":
                return

            if line == "patchEngineTorque":
                self.patch_engine_torque = True
                continue

            if line == "end_description":
                self.mode = "NONE"
                continue

            if line == "end_comment":
                self.mode = "NONE"
                continue

            #TODO: Compatibility mode
            if line == "end_section":
                self.mode = "NONE"
                continue

            if self.mode == "description":
                try:
                    self.description
                except:
                    self.description = line
                else:
                    self.description = self.description + "\n" + line
                continue

            if self.mode == "comment":
                continue

            if self.mode == "section":
                continue

            #oneliners
            if line == "forwardcommands":
                self.forward_commands = True 
                continue

            if line == "importcommands":
                self.import_commands = True 
                continue

            if line == "rollon":
                self.wheel_contact_requested = True 
                continue

            if line == "rescuer":
                self.rescuer = True 
                continue

            if line == "disabledefaultsounds":
                self.disable_default_sounds  = True
                continue

            #ignoring sections
            if line.startswith("sectionconfig"):
                continue

            if line.startswith("section"):
                continue

            #ignoring detachers
            if line.startswith("detacher_group"):
                continue

            if line.startswith("fileinfo"):
                args = self._parse_args(line)
                args.pop(0)
                self.file_info = FileInfo()
                FileInfo.unique_id    = args.pop(0)
                FileInfo.category_id  = args.pop(0)
                FileInfo.file_version = args.pop(0)
                continue

            if line.startswith("extcamera"):
                args = self._parse_args(line)
                args.pop(0)
                self.external_camera = ExternalCamera()
                self.external_camera.type = args.pop(0)
                if self.external_camera.type == "node":
                    self.external_camera.node = args.pop(0)
                continue

            if line.startswith("submesh_groundmodel"):
                args = self._parse_args(line)
                args.pop(0)
                self.submesh_ground_model = args.pop(0)
                continue

            if line.startswith("SlopeBrake"):
                args = self._parse_args(line)
                args.pop(0)
                self.slope_brake = SlopeBrake()
                self.slope_brake.regulating_force = args.pop(0)
                self.slope_brake.attack_angle     = args.pop(0)
                self.slope_brake.release_angle    = args.pop(0)
                continue

            if line.startswith("AntiLockBrakes"):
                args = filter(len, re.split(r',',line))
                args.pop(0)
                self.anti_lock = AntiLockBrakes()
                self.anti_lock.regulating_force = args.pop(0)
                self.anti_lock.min_speed        = args.pop(0)
                self.anti_lock.pulse_rate       = args.pop(0)
                self.anti_lock.mode             = args.pop(0)
                continue

            if line.startswith("TractionControl"):
                args = filter(len, re.split(r',',line))
                args.pop(0)
                self.traction_control = TractionControl()
                self.traction_control.regulating_force = args.pop(0)
                self.traction_control.wheel_slip       = args.pop(0)
                self.traction_control.fade_speed       = args.pop(0)
                self.traction_control.pulse_rate       = args.pop(0)
                self.traction_control.mode             = args.pop(0)
                continue

            if line.startswith("cruisecontrol"):
                args = self._parse_args(line)
                args.pop(0)
                self.cruise_control = CruiseControl()
                self.cruise_control.low_limit = args.pop(0)
                self.cruise_control.autobrake = args.pop(0)
                continue

            if line.startswith("speedlimiter"):
                args = self._parse_args(line)
                args.pop(0)
                self.speed_limiter = args.pop(0)
                continue

            if line.startswith("fileformatversion"):
                args = self._parse_args(line)
                args.pop(0)
                self.file_format_version = args.pop(0)
                continue

            if line.startswith("author"):
                args = self._parse_args(line)
                args.pop(0)
                self.author = Author()
                self.author.type  = args.pop(0)
                self.author.id    = args.pop(0)
                self.author.name  = args.pop(0)
                self.author.email = args.pop(0)
                continue

            if line.startswith("slidenode_connect_instantly"):
                self.slidenode_connect_instantly = True
                continue

            if line.startswith("enable_advanced_deformation"):
                self.enable_advanced_deformation = True
                continue

            if line.startswith("lockgroup_default_nolock"):
                self.lockgroup_default_nolock = True
                continue

            if line.startswith("set_shadows"):
                self.shadow_mode = self._parse_args(line)[1]
                continue

            if line.startswith("prop_camera_mode"):
                if not hasattr(self, "prop_camera_modes"):
                    self.prop_camera_modes = []
                mode = PropCameraMode()
                self.prop_camera_modes.append(mode)

                mode.line  = current_line
                mode.value = self._parse_args(line)[1]
                continue

            if line.startswith("flexbody_camera_mode"):
                if not hasattr(self, "flexbody_camera_modes"):
                    self.flexbody_camera_modes = []
                mode = FlexbodyCameraMode()
                self.flexbody_camera_modes.append(mode)

                mode.line  = current_line
                mode.value = self._parse_args(line)[1]


            if line.startswith("add_animation"):
                if not hasattr(self, "animation"):
                    self.animation = []
                anim = AddAnimation()
                self.animation.append(anim)

                args = filter(len, re.split(r',',line))
                args.pop(0)
                anim.ratio    = args.pop(0)
                anim.option_1 = args.pop(0)
                anim.option_2 = args.pop(0)
                anim.source   = args.pop(0)
                anim.mode     = args.pop(0)
                if args:
                    anim.event = args.pop(0)
                continue

            if line.startswith("set_managedmaterials_options"):
                self.managed_materials_options = self._parse_args(line).pop(0)
                continue

            if line.startswith("set_beam_defaults_scale"):
                if not hasattr(self, "beam_defaults_scale"):
                    self.beam_defaults_scale = []
                scale = SetBeamDefaultsScale()
                self.beam_defaults_scale.append(scale)

                args = self._parse_args(line)
                args.pop(0)

                scale.line   = current_line
                scale.spring = args.pop(0)
                scale.damp   = args.pop(0)
                scale.deform = args.pop(0)
                scale.scale_break  = args.pop(0)
                continue

            if line.startswith("guid"):
                self.guid = self._parse_args(line)[1]
                continue

            if line.startswith("set_beam_defaults"):
                if not hasattr(self, "beam_defaults"):
                    self.beam_defaults = []
                defaults = SetBeamDefaults()
                self.beam_defaults.append(defaults)

                args = self._parse_args(line)
                args.pop(0)
                defaults.line   = current_line
                defaults.spring = args.pop(0)
                defaults.damp   = args.pop(0)
                defaults.deform = args.pop(0)
                defaults.break_force  = args.pop(0)
                if args: defaults.diameter = args.pop(0)
                if args: defaults.material = args.pop(0)
                if args: defaults.deform_plastic = args.pop(0)
                continue

            if line.startswith("set_inertia_defaults"):
                if not hasattr(self, 'inertia_defaults'):
                    self.inertia_defaults = []
                defaults = SetInertiaDefaults()
                self.inertia_defaults.append(defaults)

                args = self._parse_args(line)
                args.pop(0)

                defaults.line = current_line

                if len(args) == 1:
                    defaults.default_value = True
                    continue

                defaults.start_delay    = args.pop(0)
                defaults.stop_delay     = args.pop(0)
                defaults.start_function = args.pop(0)
                defaults.stop_function  = args.pop(0)
                continue

            if line.startswith("set_node_defaults"):
                if not hasattr(self, 'node_defaults'):
                    self.node_defaults = []
                defaults = SetNodeDefaults()
                self.node_defaults.append(defaults)

                args = self._parse_args(line)
                args.pop(0)
                defaults.line        = current_line
                defaults.load_weight = args.pop(0)
                defaults.friction    = args.pop(0)
                defaults.volume      = args.pop(0)
                defaults.surface     = args.pop(0)
                defaults.options     = args.pop(0)
                continue

            if line.startswith("set_skeleton_settings"):
                args = self._parse_args(line)
                args.pop(0)
                self.skeleton_settings = SetSkeletonSettings()
                self.skeleton_settings.sight_range = args.pop(0)
                self.skeleton_settings.beam_diameter = args.pop(0)
                continue

            if line.startswith("backmesh"):
                if not hasattr(self, 'backmeshes'):
                    self.backmeshes = []
                self.backmeshes.append(current_line)
                continue

            if line.startswith("submesh"):
                if hasattr(self, 'submeshes'):
                    self.submeshes = []
                self.submeshes.append(current_line)
                continue

            if line.startswith("set_collision_range"):
                self.collision_range = self._parse_args(line)[1]
                continue

            if self.mode == "nodes" or self.mode == "nodes2":
                if self._comment(line): continue #Comments are not used for parsing nodes yet.

                args = self._parse_args(line)
                node = Node()
                node.id = args.pop(0)
                node.x = float(args.pop(0))
                node.y = float(args.pop(0))
                node.z = float(args.pop(0))

                if args: node.options = args.pop(0)

                if args: node.mass = float(args.pop(0))

                self._add_node(node)
                continue

            if self.mode == "camerarail":
                continue

            if self.mode == "lockgroups":
                continue

            if self.mode == "hooks":
                continue

            if self.mode == "triggers":
                continue

            if self.mode == "beams":
                if not hasattr(self, "beams"): self.beams = []
                if self._comment(line): continue #Comments are not used for parsing beams yet

                args = self._parse_args(line)

                beam = Beam()
                self.beams.append(beam)

                beam.line  = current_line
                beam.node1 = self._resolve_node(args.pop(0))
                beam.node2 = self._resolve_node(args.pop(0))
                if args: beam.options = args.pop(0)
                if args: beam.support_length = args.pop(0)
                continue

            #print line

    def _add_node(self, node):
        """Adds a node to the node list.
        If the node is a named node, then adds an entry to the named node list too.
        """
        if not hasattr(self, "nodes"): self.nodes = []
        if not hasattr(self, "named_nodes"): self.named_nodes = {}
        if not hasattr(self, "free_node"): self.free_node = -1
        self.free_node += 1

        copy_node = copy.copy(node)

        try: 
            copy_node.id = int(node.id)
        except:
            node_name = node.id
            if node_name not in self.named_nodes: self.named_nodes[node_name] = self.free_node
            copy_node.id = self.named_nodes[node_name]

        self.nodes.append(copy_node)

    def _resolve_node(self, node_id):
        """Get the node ID for a node. Translates named nodes into node IDs.
        """
        try:
            return int(node_id)
        except:
            if node_id in self.named_nodes: 
                return self.named_nodes[node_id]
            print [node['id'] for node in self.nodes]
            raise Exception("Undeclared node found: " + node_id)

    def _parse_args(self, data):
        unfiltered_args = re.split(r":|\||,| |\t", data)
        return filter(len, unfiltered_args)

    def _comment(self, line):
        return line[0] == ";"
    