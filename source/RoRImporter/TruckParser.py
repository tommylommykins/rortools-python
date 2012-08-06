import re
import copy

#class FileInfo(object):
#    def __init__(self, uid = None, cid = None, version = None):
#        self.unique_id    = uid
#        self.category_id  = cid
#        self.file_version = version
#        
#class ExternalCamera(object):
#    def __init__(self, camera_type = None, node = None):
#        self.type = camera_type
#        self.node = node
#        
#class SlopeBrake(object):
#    def __init__(self, regulating_force = None, attack_angle = None, release_angle = None):
#        self.regulating_force = regulating_force
#        self.attack_angle = attack_angle
#        self.release_angle = release_angle
#        
#class AntiLockBrakes(object):
#    def __init__(self, regulating_force = None, wheel_slip = None, fade_speed = None, pulse_rate = None, mode = None):
#        self.regulating_force = regulating_force
#        self.wheel_slip = wheel_slip
#        self.fade_speed = fade_speed
#        self.pulse_rate = pulse_rate
#        self.mode = mode
#        
#class TractionControl(object):
#    def __init__(self, regulating_force = None, wheel_slip = None, fade_speed = None, pulse_rate = None, mode = None):
#        self.regulating_force = regulating_force
#        self.wheel_slip = wheel_slip
#        self.fade_speed = fade_speed
#        self.pulse_rate = pulse_rate
#        self.mode = mode
#        
#class CruiseControl(object):
#    def __init__(self, low_limit = None, autobrake = None):
#        self.low_limit = low_limit
#        self.autobrake = autobrake
#
#class PropCameraMode(object):
#    def __init__(self, line = None, value = None):
#        self.line = line
#        self.value = value
#        
#class FlexbodyCameraMode(object):
#    def __init__(self, line = None, value = None):
#        self.line = line
#        self.value = value
#
#class Author(object):
#    def __init__(self, author_type = None, author_id = None, name = None, email = None):
#        self.type = author_type
#        self.id = author_id
#        self.name = name
#        self.email = email
#
#class AddAnimation(object):
#    def __init__(self, ratio = None, option_1 = None, option_2 = None, source = None, mode = None, event = None):
#        self.ratio = ratio
#        self.option_1 = option_1
#        self.option_2 = option_2
#        self.source = source
#        self.mode = mode
#        self.event = event
#
#class SetBeamDefaultsScale(object):
#    def __init__(self, line = None, spring = None, damp = None, deform = None, scale_break = None):
#        self.line = line
#        self.spring = spring
#        self.damp = damp
#        self.deform = deform
#        self.scale_break = scale_break
#        
#class SetBeamDefaults(object):
#    def __init__(self, line = None, spring = None, damp = None, deform = None, break_force = None, diameter = None, material = None,
#                 deform_plastic = None):
#        self.line = line
#        self.spring = spring
#        self.damp = damp
#        self.deform = deform
#        self.break_force = break_force
#        self.diameter = diameter
#        self.material = material
#        self.deform_plastic = deform_plastic
#
#class SetInertiaDefaults(object):
#    def __init__(self, line = None, start_delay = None, stop_delay = None, start_function = None, stop_function = None,
#                 default_value = None):
#        self.line = line
#        self.start_delay = start_delay
#        self.stop_delay = stop_delay
#        self.start_function = start_function
#        self.stop_function = stop_function
#        self.default_value = default_value
#
#class SetNodeDefaults(object):
#    def __init__(self, line = None, load_weight = None, friction = None, volume = None, surface = None, options = None):
#        self.line = line
#        self.load_weight = load_weight
#        self.friction = friction
#        self.volume = volume
#        self.surface = surface
#        self.options = options
#
#class SetSkeletonSettings(object):
#    def __init__(self, sight_range = None, beam_diameter = None):
#        self.sight_range = sight_range
#        self.beam_diameter = beam_diameter
#
#class Node(object):
#    def __init__(self, id_no = None, x = None, y = None, z = None, options = None, mass = None):
#        self.id = id_no
#        self.x = x
#        self.y = y
#        self.z = z
#        self.options = options
#        self.mass = mass
#
#class Beam(object):
#    def __init__(self, line = None, node1 = None, node2 = None, options = None, support_length = None):
#        self.line = line
#        self.node1 = node1
#        self.node2 = node2
#        self.options = options
#        self.support_length = support_length
#        
#class Trigger(object):
#    def __init__(self, node1 = None, node2 = None, contraction_limit = None, extension_limit = None, shorten_key = None,
#                 lengthen_key = None, option = None, boundary_timer = None):
#        self.node1 = node1
#        self.node2 = node2
#        self.contraction_limit = contraction_limit
#        self.extension_limit = extension_limit
#        self.shorten_key = shorten_key
#        self.lengthen_key = lengthen_key
#        self.option = option
#        self.boundary_timer = boundary_timer
#        
#class Shock(object):
#    def __init__(self, 
#                 node1= None, 
#                 node2 = None, 
#                 spring_in = None, 
#                 damp_in = None,
#                 progressive_spring_in = None,
#                 progressive_damp_in = None,
#                 spring_out = None, 
#                 damp_out = None,
#                 progressive_spring_out = None,
#                 progressive_damp_out = None,                  
#                 shortest_length = None, 
#                 longest_length = None,
#                 precompression = None, 
#                 options = None):
#        self.node1 = node1
#        self.node2 = node2
#        self.spring_in = spring_in
#        self.damp_in = damp_in
#        self.progressive_spring_in = progressive_spring_in
#        self.progressive_damp_in = progressive_damp_in
#        self.spring_out = spring_out
#        self.damp_out = damp_out
#        self.progressive_spring_out = progressive_spring_out
#        self.progressive_damp_out = progressive_damp_out
#        self.shortest_length = shortest_length
#        self.longest_length = longest_length
#        self.precompression = precompression
#        self.options = options
#        
#class Hydro(object):
#    def __init__(self, node1 = None, node2 = None, ratio = None, options = None, start_delay = None, stop_delay = None,
#                 start_function = None, stop_function = None):
#        self.node1 = node1
#        self.node2 = node2
#        self.ratio = ratio
#        self.options = options
#        self.start_delay = start_delay
#        self.stop_delay = stop_delay
#        self.start_function = start_function
#        self.stop_function = stop_function
#        
#class Animator(object):
#    def __init__(self, node1 = None, node2 = None, factor = None, option = None):
#        self.node1 = node1
#        self.node2 = node2
#        self.factor = factor
#        self.option = option
#        
#class Wheel(object):
#    def __init__(self, radius = None, numrays = None, node1 = None, node2 = None, rigidity_node = None, braked = None,
#                 driven = None, reference_node = None, mass = None, spring = None, damp = None, face_material = None,
#                 tread_material = None):
#        self.radius = radius
#        self.numrays = numrays
#        self.node1 = node1
#        self.node2 = node2
#        self.rigidity_node = rigidity_node
#        self.braked = braked
#        self.driven = driven
#        self.reference_node = reference_node
#        self.mass = mass
#        self.spring = spring
#        self.damp = damp
#        self.face_material = face_material
#        self.tread_material = tread_material
#        
#class Wheel2(object):
#    def __init__(self, 
#                 rim_radius = None,
#                 tyre_radius = None, 
#                 numrays = None, 
#                 node1 = None, 
#                 node2 = None, 
#                 rigidity_node = None, 
#                 braked = None,
#                 driven = None, 
#                 reference_node = None, 
#                 mass = None, 
#                 rim_spring = None, 
#                 rim_damp = None,
#                 tyre_spring = None, 
#                 tyre_damp = None, 
#                 face_material = None,
#                 tread_material = None):
#        self.rim_radius = rim_radius
#        self.tyre_radius = tyre_radius
#        self.numrays = numrays
#        self.node1 = node1
#        self.node2 = node2
#        self.rigidity_node = rigidity_node
#        self.braked = braked
#        self.driven = driven
#        self.reference_node = reference_node
#        self.mass = mass
#        self.rim_spring = rim_spring
#        self.rim_damp = rim_damp
#        self.tyre_spring = tyre_spring
#        self.tyre_damp = tyre_damp
#        self.face_material = face_material
#        self.tread_material = tread_material
#        
#class Meshwheel(object):
#    def __init__(self, 
#                 tyre_radius = None,
#                 rim_radius = None, 
#                 numrays = None, 
#                 node1 = None, 
#                 node2 = None, 
#                 rigidity_node = None, 
#                 braked = None,
#                 driven = None, 
#                 reference_node = None, 
#                 mass = None, 
#                 spring = None, 
#                 damp = None,
#                 side = None,
#                 face_material = None,
#                 tread_material = None):
#        self.tyre_radius = tyre_radius
#        self.rim_radius = rim_radius
#        self.numrays = numrays
#        self.node1 = node1
#        self.node2 = node2
#        self.rigidity_node = rigidity_node
#        self.braked = braked
#        self.driven = driven
#        self.reference_node = reference_node
#        self.mass = mass
#        self.spring = spring
#        self.damp = damp
#        self.side = side
#        self.face_material = face_material
#        self.tread_material = tread_material
#        
#class Flexbodywheel(object):
#    def __init__(self, 
#                 rim_radius = None,
#                 tyre_radius = None, 
#                 numrays = None, 
#                 node1 = None, 
#                 node2 = None, 
#                 rigidity_node = None, 
#                 braked = None,
#                 driven = None, 
#                 reference_node = None, 
#                 mass = None, 
#                 rim_spring = None, 
#                 rim_damp = None,
#                 tyre_spring = None, 
#                 tyre_damp = None, 
#                 direction = None,
#                 face_material = None,
#                 tread_material = None):
#        self.rim_radius = rim_radius
#        self.tyre_radius = tyre_radius
#        self.numrays = numrays
#        self.node1 = node1
#        self.node2 = node2
#        self.rigidity_node = rigidity_node
#        self.braked = braked
#        self.driven = driven
#        self.reference_node = reference_node
#        self.mass = mass
#        self.rim_spring = rim_spring
#        self.rim_damp = rim_damp
#        self.tyre_spring = tyre_spring
#        self.tyre_damp = tyre_damp
#        self.direction = direction
#        self.face_material = face_material
#        self.tread_material = tread_material
#        
#class Camera(object):
#    def __init__(self, center = None, back = None, left = None):
#        self.center = center
#        self.back = back
#        self.left = left
#        
#class Commands2(object):
#    def __init__(self,
#                 node1 = None,
#                 node2 = None,
#                 shorten_rate = None,
#                 lengthen_rate = None,
#                 shortest_length = None,
#                 longest_length = None,
#                 shorten_key = None,
#                 lengthen_key = None,
#                 option = None,
#                 description = None):
#        self.node1 = node1
#        self.node2 = node2
#        self.shorten_rate = shorten_rate
#        self.lengthen_rate = lengthen_rate
#        self.shortest_length = shortest_length
#        self.longest_length = longest_length
#        self.shorten_key = shorten_key
#        self.lengthen_key = lengthen_key
#        self.option = option
#        self.description = description
        
class TruckParser(object):
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
        print truck_file
        if not truck_file: raise Exception("Truck file empty")            
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
                self.file_info = line
                continue

            if line.startswith("extcamera"):
                args = self._parse_args(line)
                args.pop(0)
                self.external_camera = {}
                self.external_camera['type'] = args.pop(0)
                if self.external_camera['type'] == "node":
                    self.external_camera['node'] = self._resolve_node(args.pop(0))
                continue

            if line.startswith("submesh_groundmodel"):
                args = self._parse_args(line)
                args.pop(0)
                self.submesh_ground_model = args.pop(0)
                continue

            if line.startswith("SlopeBrake"):
                self.slope_brake = line
                continue

            if line.startswith("AntiLockBrakes"):
                self.anti_lock_brake = line
                continue

            if line.startswith("TractionControl"):
                self.traction_control = line
                continue

            if line.startswith("cruisecontrol"):
                self.cruise_control = line
                continue

            if line.startswith("speedlimiter"):
                self.speed_limiter = line
                continue

            if line.startswith("fileformatversion"):
                self.file_format_version = line
                continue

            if line.startswith("author"):
                self.author = line
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
                self.prop_camera_modes = getattr(self, "prop_camera_modes", [])
                mode = {}
                self.prop_camera_modes.append(mode)

                mode['line']  = current_line
                mode['value'] = self._parse_args(line)[1]
                continue

            if line.startswith("flexbody_camera_mode"):
                self.flexbody_camera_modes = getattr(self, "flexbody_camera_modes", [])
                mode = {}
                self.flexbody_camera_modes.append(mode)

                mode['line']  = current_line
                mode['value'] = self._parse_args(line)[1]


            if line.startswith("add_animation"):
                self.add_animation = getattr(self, "animation", [])
                anim = {}
                self.add_animation.append(anim)

                args = filter(len, re.split(r',',line[13:-1]))
                anim['ratio']    = args.pop(0)
                anim['option_1'] = args.pop(0)
                anim['option_2'] = args.pop(0)
                anim['source']   = args.pop(0)
                anim['mode']     = args.pop(0)
                if args: anim['event'] = args.pop(0)
                continue

            if line.startswith("set_managedmaterials_options"):
                self.managed_materials_options = self._parse_args(line).pop(0)
                continue

            if line.startswith("set_beam_defaults_scale"):
                self.beam_defaults_scale = getattr(self, "beam_defaults_scale", [])
                scale = {}
                self.beam_defaults_scale.append(scale)

                args = self._parse_args(line)
                args.pop(0)

                scale['line']   = current_line
                scale['spring'] = args.pop(0)
                scale['damp']   = args.pop(0)
                scale['deform'] = args.pop(0)
                scale['scale_break']  = args.pop(0)
                continue

            if line.startswith("guid"):
                self.guid = self._parse_args(line)[1]
                continue

            if line.startswith("set_beam_defaults"):
                self.beam_defaults = getattr(self, "beam_defaults", [])
                defaults = {}
                self.beam_defaults.append(defaults)

                args = self._parse_args(line)
                args.pop(0)
                defaults['line']   = current_line
                defaults['spring'] = args.pop(0)
                defaults['damp']   = args.pop(0)
                defaults['deform'] = args.pop(0)
                defaults['break_force']  = args.pop(0)
                if args: defaults['diameter'] = args.pop(0)
                if args: defaults['material'] = args.pop(0)
                if args: defaults['deform_plastic'] = args.pop(0)
                continue

            if line.startswith("set_inertia_defaults"):
                self.inertia_defaults = getattr(self, 'inertia_defaults', [])
                defaults = {}
                self.inertia_defaults.append(defaults)

                args = self._parse_args(line)
                args.pop(0)

                defaults['line'] = current_line

                if len(args) == 1:
                    defaults['default_value'] = True
                    continue

                defaults['start_delay']    = args.pop(0)
                defaults['stop_delay']     = args.pop(0)
                defaults['start_function'] = args.pop(0)
                defaults['stop_function']  = args.pop(0)
                continue

            if line.startswith("set_node_defaults"):
                self.node_defaults = getattr(self, 'node_defaults', [])
                defaults = {}
                self.node_defaults.append(defaults)

                args = self._parse_args(line)
                args.pop(0)
                defaults['line']        = current_line
                defaults['load_weight'] = args.pop(0)
                defaults['friction']    = args.pop(0)
                defaults['volume']      = args.pop(0)
                defaults['surface']     = args.pop(0)
                if args: defaults['options'] = args.pop(0)
                continue

            if line.startswith("set_skeleton_settings"):
                self.skeleton_settings = line
                continue

            if line.startswith("backmesh"):
                if not hasattr(self, 'backmeshes'): self.backmeshes = []
                self.backmeshes.append(current_line)
                continue

            if line.startswith("submesh"):
                if not hasattr(self, 'submeshes'):
                    self.submeshes = []
                self.submeshes.append(current_line)
                continue

            if line.startswith("set_collision_range"):
                self.collision_range = self._parse_args(line)[1]
                continue

            if self.mode == "nodes" or self.mode == "nodes2":
                if self._comment(line): continue #Comments are not used for parsing nodes yet.

                args = self._parse_args(line)
                node = {}
                node['line'] = current_line
                node['id'] = args.pop(0)
                node['x'] = float(args.pop(0))
                node['y'] = float(args.pop(0))
                node['z'] = float(args.pop(0))
                if args: node['options'] = args.pop(0)
                if args: node['mass'] = float(args.pop(0))

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
                if self._comment(line): continue #Comments are not used for parsing beams yet
                self.beams = getattr(self, "beams", [])

                args = self._parse_args(line)

                beam = {}
                self.beams.append(beam)

                beam['line']  = current_line
                beam['node1'] = self._resolve_node(args.pop(0))
                beam['node2'] = self._resolve_node(args.pop(0))
                if args: beam['options'] = args.pop(0)
                if args: beam['support_length'] = args.pop(0)
                continue
            
            if self.mode == "triggers":
                if self._comment(line): continue
                self.triggers = getattr(self, "triggers", [])
                
                trigger = {}
                self.triggers.append(trigger)
                
                args = self._parse_args(line)
                trigger['node1'] = self._resolve_node(args.pop(0))
                trigger['node2'] = self._resolve_node(args.pop(0))
                trigger['contraction_limit'] = args.pop(0)
                trigger['extension_limit'] = args.pop(0)
                trigger['shorten_key'] = args.pop(0)
                trigger['lengthen_key'] = args.pop(0)
                if args: trigger['option'] = args.pop(0)
                if args: trigger['boundary_timer'] = args.pop(0)
                continue
                
            if self.mode == "shocks":
                if self._comment(line): continue
                self.shocks = getattr(self, "shocks", [])
                
                shock = {}
                self.shocks.append(shock)
                
                args = self._parse_args(line)
                shock['node1'] = self._resolve_node(args.pop(0))
                shock['node2'] = self._resolve_node(args.pop(0))
                shock['spring_in'] = args.pop(0)
                shock['damp_in'] = args.pop(0)
                shock['progressive_spring_in'] = 0
                shock['progressive_damp_in'] = 0
                shock['spring_out'] = shock['spring_in']
                shock['damp_out'] = shock['damp_in']
                shock['progressive_spring_out'] = 0
                shock['progressive_damp_out'] = 0
                shock['shortest_length'] = args.pop(0)
                shock['longest_length'] = args.pop(0)
                shock['precompression'] = args.pop(0)
                if args: shock['options'] = args.pop(0)
                continue
            
            if self.mode == "shocks2":
                if self._comment(line): continue
                self.shocks = getattr(self, "shocks", [])
                
                shock = {}
                self.shocks.append(shock)
                
                args = self._parse_args(line)
                shock['node1'] = self._resolve_node(args.pop(0))
                shock['node2'] = self._resolve_node(args.pop(0))
                shock['spring_in'] = args.pop(0)
                shock['damp_in'] = args.pop(0)
                shock['progressive_spring_in'] = args.pop(0)
                shock['progressive_damp_in'] = args.pop(0)
                shock['spring_out'] = args.pop(0)
                shock['damp_out'] = args.pop(0)
                shock['progressive_spring_out'] = args.pop(0)
                shock['progressive_damp_out'] = args.pop(0)
                shock['shortest_length'] = args.pop(0)
                shock['longest_length'] = args.pop(0)
                shock['precompression'] = args.pop(0)
                if args: shock['options'] = args.pop(0)
                continue
            
            if self.mode == "fixes":
                self.fixes = getattr(self, "fixes", [])
                if self._comment(line): continue
                self.fixes.append(self._resolve_node(line))
                continue
            
            if self.mode == "hydros":
                if self._comment(line): continue
                self.hydros = getattr(self, "hydros", [])
                
                hydro = {}
                self.hydros.append(hydro)
                
                args = self._parse_args(line)
                hydro['node1'] = self._resolve_node(args.pop(0))
                hydro['node2'] = self._resolve_node(args.pop(0))
                if args: hydro['ratio'] = args.pop(0)
                if args: hydro['options'] = args.pop(0)
                if args: hydro['start_delay'] = args.pop(0)
                if args: hydro['stop_delay'] = args.pop(0)
                if args: hydro['start_function'] = args.pop(0)
                if args: hydro['stop_function'] = args.pop(0)
                continue
            
            if self.mode == "animators":
                if self._comment(line): continue
                self.animators = getattr(self, "animators", [])
                
                animator = {}
                self.animators.append(animator)

                args = filter(len, re.split(r',',line[9:-1]))                
                animator['node1'] = self._resolve_node(args.pop(0))
                animator['node2'] = self._resolve_node(args.pop(0))
                animator['factor'] = args.pop(0)
                animator['option'] = args.pop(0)
                continue
                
            if self.mode == "wheels":
                if self._comment(line): continue
                self.wheels = getattr(self, "wheels", [])
                
                wheel = {}
                self.wheels.append(wheel)
                
                args = self._parse_args(line)
                wheel['radius'] = args.pop(0)
                args.pop(0)
                wheel['numrays'] = args.pop(0)
                wheel['node1'] = self._resolve_node(args.pop(0))
                wheel['node2'] = self._resolve_node(args.pop(0))
                wheel['rigidity_node'] = self._resolve_node(args.pop(0))
                wheel['braked'] = args.pop(0)
                wheel['driven'] = args.pop(0)
                wheel['reference_node'] = self._resolve_node(args.pop(0))
                wheel['mass'] = args.pop(0)
                wheel['spring'] = args.pop(0)
                wheel['damp'] = args.pop(0)
                wheel['face_material'] = args.pop(0)
                wheel['tread_material'] = args.pop(0)
                continue
            
            if self.mode == "wheels2":
                if self._comment(line): continue
                self.wheels2 = getattr(self, "wheels2", [])
                
                wheel2 = {}
                self.wheels2.append(wheel2)
                
                args = self._parse_args(line)
                wheel2['rim_radius'] = args.pop(0)
                wheel2['tyre_radius'] = args.pop(0)
                args.pop(0)
                wheel2['numrays'] = args.pop(0)
                wheel2['node1'] = self._resolve_node(args.pop(0))
                wheel2['node2'] = self._resolve_node(args.pop(0))
                wheel2['rigidity_node'] = self._resolve_node(args.pop(0))
                wheel2['braked'] = args.pop(0)
                wheel2['driven'] = args.pop(0)
                wheel2['reference_node'] = self._resolve_node(args.pop(0))
                wheel2['mass'] = args.pop(0)
                wheel2['rim_spring'] = args.pop(0)
                wheel2['rim_damp'] = args.pop(0)
                wheel2['tyre_spring'] = args.pop(0)
                wheel2['tyre_damp'] = args.pop(0)
                wheel2['face_material'] = args.pop(0)
                wheel2['tread_material'] = args.pop(0)
                continue
            
            if self.mode == "meshwheels":
                if self._comment(line): continue
                self.meshwheels = getattr(self, "meshwheels", [])
                meshwheel = self._read_meshwheel(line)
                self.meshwheels.append(meshwheel)
                continue
            
            if self.mode == "meshwheels2":
                if self._comment(line): continue
                self.meshwheels2 = getattr(self, "meshwheels2", [])
                meshwheel2 = self._read_meshwheel(line)
                self.meshwheels2.append(meshwheel2)
                continue
            
            if self.mode == "flexbodywheels":
                if self._comment(line): continue
                self.flexbodywheels = getattr(self, "flexbodywheels", [])
                
                flexbodywheel = {}
                self.wheels2.append(flexbodywheel)
                
                args = self._parse_args(line)
                flexbodywheel['rim_radius'] = args.pop(0)
                flexbodywheel['tyre_radius'] = args.pop(0)
                args.pop(0)
                flexbodywheel['numrays'] = args.pop(0)
                flexbodywheel['node1'] = self._resolve_node(args.pop(0))
                flexbodywheel['node2'] = self._resolve_node(args.pop(0))
                flexbodywheel['rigidity_node'] = self._resolve_node(args.pop(0))
                flexbodywheel['braked'] = args.pop(0)
                flexbodywheel['driven'] = args.pop(0)
                flexbodywheel['reference_node'] = self._resolve_node(args.pop(0))
                flexbodywheel['mass'] = args.pop(0)
                flexbodywheel['rim_spring'] = args.pop(0)
                flexbodywheel['rim_damp'] = args.pop(0)
                flexbodywheel['tyre_spring'] = args.pop(0)
                flexbodywheel['tyre_damp'] = args.pop(0)
                flexbodywheel['direction'] = args.pop(0)
                flexbodywheel['face_material'] = args.pop(0)
                flexbodywheel['tread_material'] = args.pop(0)
                continue
            
            if self.mode == "globals":
                if self._comment(line): continue
                self.globals = line
                continue
            
            if self.mode == "cameras":
                if self._comment(line): continue
                self.cameras = getattr(self, "cameras", [])
                
                camera = {}
                self.cameras.append(camera)
                
                args = self._parse_args(line)
                camera['center'] = args.pop(0)
                camera['back'] = args.pop(0)
                camera['left'] = args.pop(0)
                continue
            
            if self.mode == "engine":
                if self._comment(line): continue 
                self.engine = line
                
                continue
            
            if self.mode == "texcoords":
                continue
            
            if self.mode == "cab":
                continue
            
            if self.mode == "commands":
                continue
            
            print "\tunparsed: %s" % line
    
    def _read_meshwheel(self, line):
        meshwheel = {}
        args = self._parse_args(line)
        meshwheel['tyre_radius'] = args.pop(0)
        meshwheel['rim_radius'] = args.pop(0)
        args.pop(0)
        meshwheel['numrays'] = args.pop(0)
        meshwheel['node1'] = self._resolve_node(args.pop(0))
        meshwheel['node2'] = self._resolve_node(args.pop(0))
        meshwheel['rigidity_node'] = self._resolve_node(args.pop(0))
        meshwheel['braked'] = args.pop(0)
        meshwheel['driven'] = args.pop(0)
        meshwheel['reference_node'] = self._resolve_node(args.pop(0))
        meshwheel['mass'] = args.pop(0)
        meshwheel['spring'] = args.pop(0)
        meshwheel['damp'] = args.pop(0)
        meshwheel['side'] = args.pop(0)
        meshwheel['face_material'] = args.pop(0)
        meshwheel['tread_material'] = args.pop(0)
        return meshwheel

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
            copy_node.id = int(node['id'])
        except:
            node_name = node['id']
            if node_name not in self.named_nodes: self.named_nodes[node_name] = self.free_node
            copy_node['id'] = self.named_nodes[node_name]

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
    