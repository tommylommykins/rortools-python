import re

class TruckFileReader:
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
        self.resolve_node_ids()

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
                    print "MATCH"
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
                self.file_info = {}
                self.file_info['unique_id']    = args.pop(0)
                self.file_info['category_id']  = args.pop(0)
                self.file_info['file_version'] = args.pop(0)
                continue

            if line.startswith("extcamera"):
                args = self._parse_args(line)
                args.pop(0)
                self.external_camera = {}
                self.external_camera['type'] = args.pop(0)
                if self.external_camera['type'] == "node":
                    self.external_camera['node'] = args.pop(0)
                else:
                    self.external_camera['node'] = -1
                continue

            if line.startswith("submesh_groundmodel"):
                args = self._parse_args(line)
                args.pop(0)
                self.submesh_ground_model = args.pop(0)
                continue

            if line.startswith("SlopeBrake"):
                args = self._parse_args(line)
                args.pop(0)
                self.slope_brake = {}
                self.slope_brake['regulating_force'] = args.pop(0)
                self.slope_brake['attack_angle']     = args.pop(0)
                self.slope_brake['release_angle']    = args.pop(0)
                continue

            if line.startswith("AntiLockBrakes"):
                args = filter(len, re.split(r',',line))
                args.pop(0)
                self.anti_lock = {}
                self.anti_lock['regulating_force'] = args.pop(0)
                self.anti_lock['min_speed']        = args.pop(0)
                self.anti_lock['pulse_rate']       = args.pop(0)
                self.anti_lock['mode']             = args.pop(0)
                continue

            if line.startswith("TractionControl"):
                args = filter(len, re.split(r',',line))
                args.pop(0)
                self.traction_control = {}
                self.traction_control['regulating_force'] = args.pop(0)
                self.traction_control['wheelslip']        = args.pop(0)
                self.traction_control['fadespeed']        = args.pop(0)
                self.traction_control['pulse_rate']       = args.pop(0)
                self.traction_control['mode']             = args.pop(0)
                continue

            if line.startswith("cruisecontrol"):
                args = self._parse_args(line)
                args.pop(0)
                self.cruise_control = {}
                self.cruise_control['low_limit'] = args.pop(0)
                self.cruise_control['autobrake'] = args.pop(0)
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
                self.author = {}
                self.author['type']  = args.pop(0)
                self.author['id']    = args.pop(0)
                self.author['name']  = args.pop(0)
                self.author['email'] = args.pop(0)
                continue

            if line.startswith("slidenode_connect_instantly"):
                self.slidenode_connect_instantly = true
                continue

            if line.startswith("enable_advanced_deformation"):
                self.enable_advanced_deformation = true
                continue

            if line.startswith("lockgroup_default_nolock"):
                self.lockgroup_default_nolock = true
                continue

            if line.startswith("set_shadows"):
                self.shadow_mode = self._parse_args(line)[1]
                continue

            #broken -- needs to be parsed with props
            if line.startswith("prop_camera_mode"):
                if not hasattr(self, "prop_camera_modes"):
                    self.prop_camera_modes = []
                mode = {}
                self.prop_camera_modes.append(mode)

                mode['line']  = current_line
                mode['value'] = self._parse_args(line)[1]
                continue

            if line.startswith("flexbody_camera_mode"):
                if not hasattr(self, "flexbody_camera_modes"):
                    self.flexbody_camera_modes = []
                mode = {}
                self.flexbody_camera_modes.append(mode)

                mode['line']  = current_line
                mode['value'] = self._parse_args(line)[1]


            if line.startswith("add_animation"):
                if not hasattr(self, "animation"):
                    self.animation = []
                anim = {}
                self.animation.append(anim)

                args = filter(len, re.split(r',',line))
                args.pop(0)
                anim['ratio']    = args.pop(0)
                anim['option_1'] = args.pop(0)
                anim['option_2'] = args.pop(0)
                anim['source']   = args.pop(0)
                anim['mode']     = args.pop(0)
                if args:
                    anim['event'] = args.pop(0)
                else:
                    anim['event'] = ""
                continue

            if line.startswith("set_managedmaterials_options"):
                self.managed_materials_options = self._parse_args(line).pop(0)
                continue

            if line.startswith("set_beam_defaults_scale"):
                if not hasattr(self, "beam_defaults_scale"):
                    self.beam_defaults_scale = []
                scale = {}
                self.beam_defaults_scale.append(scale)

                args = self._parse_args(line)
                args.pop(0)

                scale['line']   = current_line
                scale['spring'] = args.pop(0)
                scale['damp']   = args.pop(0)
                scale['deform'] = args.pop(0)
                scale['break']  = args.pop(0)
                continue

            if line.startswith("guid"):
                self.guid = self._parse_args(line)[1]
                continue

            if line.startswith("set_beam_defaults"):
                if not hasattr(self, "beam_defaults"):
                    self.beam_defaults = []
                defaults = {}
                self.beam_defaults.append(defaults)

                args = self._parse_args(line)
                args.pop(0)
                defaults['line']   = current_line
                defaults['spring'] = args.pop(0)
                defaults['damp']   = args.pop(0)
                defaults['deform'] = args.pop(0)
                defaults['break']  = args.pop(0)
                if args:
                    defaults['diameter'] = args.pop(0)
                else:
                    defaults['diamater'] = -1

                if args:
                    defaults['material'] = args.pop(0)
                else:
                    defaults['material'] = -1

                if args:
                    defaults['deform_plastic'] = args.pop(0)
                else:
                    defaults['deform_plastic'] = -1
                continue

            if line.startswith("set_inertia_defaults"):
                if not hasattr(self, 'inertia_defaults'):
                    self.inertia_defaults = []
                defaults = {}
                self.inertia_defaults.append(defaults)

                args = self._parse_args(line)
                args.pop(0)

                defaults['line'] = current_line

                if len(args) == 1:
                    defaults['default'] = True
                    continue

                defaults['start_delay']    = args.pop(0)
                defaults['stop_delay']     = args.pop(0)
                defaults['start_function'] = args.pop(0)
                defaults['stop_function']  = args.pop(0)
                continue

            if line.startswith("set_node_defaults"):
                if not hasattr(self, 'node_defaults'):
                    self.node_defaults = []
                defaults = {}
                self.node_defaults.append(defaults)

                args = self._parse_args(line)
                args.pop(0)
                defaults['line']        = current_line
                defaults['load_weight'] = args.pop(0)
                defaults['friction']    = args.pop(0)
                defaults['volume']      = args.pop(0)
                defaults['surface']     = args.pop(0)
                defaults['options']     = args.pop(0)
                continue

            if line.startswith("set_skeleton_settings"):
                args = self._parse_args(line)
                args.pop(0)
                self.skeleton_settings = {}
                self.skeleton_settings['sight_range'] = args.pop(0)
                self.skeleton_settings['beam_diameter'] = args.pop(0)
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
                if self.comment(line):
                    continue

                print line
                if not hasattr(self, "unresolved_nodes"):
                    self.unresolved_nodes = []
                node = {}
                self.unresolved_nodes.append(node)

                args = self._parse_args(line)
                node['id'] = args.pop(0)
                node['x'] = float(args.pop(0))
                node['y'] = float(args.pop(0))
                node['z'] = float(args.pop(0))
                if args:
                    node['options'] = args.pop(0)
                else:
                    node['options'] = ""

                if args:
                    node['mass'] = float(args.pop(0))
                else:
                    node['mass'] = ""
                continue

            #print line

    def resolve_node_ids(self):
        """Creates a mapping between named nodes and their actual node IDs
        """
        self.nodes = []
        self.named_nodes = {}
        free_node = -1
        for node in self.unresolved_nodes:
            free_node += 1

            try:
                copy_node = dict(node)
                copy_node['id'] = int(node['id'])
                self.nodes.append(copy_node)
            except:
                #If the ID is not a number then it is a named node
                node_name = node['id']
                copy_node = dict(node)
                copy_node['id'] = free_node
                self.nodes.append(copy_node)
                self.named_nodes[node_name] = free_node

    def _parse_args(self, data):
        unfiltered_args = re.split(r":|\||,| |\t", data)
        return filter(len, unfiltered_args)

    def comment(self, line):
        return line[0] == ";"
    