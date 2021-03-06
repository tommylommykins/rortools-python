import re
import copy
        
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
        
        self.global_sections = ["globals", "engine", "help", "globeams", "engoption", "brakes", "guisettings", "minimass", "envmap",
                                "torquecurve", "advdrag", "nodecollision", "description", "videocamera"]

    #Loads a file. Iterates through it and creates data structures which can later be queried.
    def load_truck(self, truck_file):
        print truck_file
        if not truck_file: raise Exception("Truck file empty")            
        self.parse_truck(truck_file)

    def parse_truck(self, truck_file):
        """Reads a truck file. Incomplete. Sections that are written do not yet correctly
        handle expected data types of input values
        
        Note: This method very closely and deliberately follows the logic of the parser
        in serializedrig.cpp. 
        """
        truck_file_contents = open(truck_file).read()

        for line_no, line in enumerate(truck_file_contents.splitlines()):
            #try:
            if True:
                self._parse_line(line, line_no)
            #except Exception as e:
            #    print "failed to parse line %i: '%s'" % (line_no, line)
            #    raise e

    def _parse_line(self, line, line_no):
        self.mode = getattr(self, "mode", "NONE")
        line = line.strip()
        
        #skip blank lines
        if not line:
            return
        
        self.comments = getattr(self, "comments", [])
        if self._comment(line):
            comment = {}
            comment['text'] = line[1:]
            comment['line_no'] = line_no
            self.comments.append(comment)
            return

        next_line = False
        for section in self.sections:
            if line == section:
                print "MODE" + self.mode
                self.mode = section
                if line in self.global_sections:
                    self._add_global_data("\n" + line)
                #Note: In the sourcecode, the mode queue is currently never actually used for anything, so
                #it is not implemented here
                next_line = True
        if next_line:
            return

        self.truck_name_found = getattr(self, "truck_name_found", False)
        if not self.truck_name_found:
            self.truck_name = line 
            self._add_global_data(line)
            self.truck_name_found = True
            return

        if line == "end":
            return

        if line == "patchEngineTorque":
            self._add_global_data("\n" + line)
            return

        if line == "end_description":
            self._add_global_data(line)
            self.mode = "NONE"
            return

        if line == "end_comment":
            self._add_global_data(line)
            self.mode = "NONE"
            return

        #TODO: Compatibility mode
        if line == "end_section":
            self.mode = "NONE"
            self._add_global_data(line)
            return

        if self.mode == "description":
            self._add_global_data(line)
            return

        if self.mode == "comment":
            self._add_global_data(line)
            return

        if self.mode == "section":
            return

        #oneliners
        if line == "forwardcommands":
            self._add_global_data("\n" + line)
            return

        if line == "importcommands": 
            self._add_global_data("\n" + line)
            return

        if line == "rollon":
            self._add_global_data("\n" + line) 
            return

        if line == "rescuer":
            self._add_global_data("\n" + line) 
            return

        if line == "disabledefaultsounds":
            self._add_global_data("\n" + line)
            return

        #ignoring sections
        if line.startswith("sectionconfig"):
            return

        if line.startswith("section"):
            return

        #ignoring detachers
        if line.startswith("detacher_group"):
            return

        if line.startswith("fileinfo"):
            self._add_global_data(line)
            return

        self.external_camera = getattr(self, "external_camera", {})
        if line.startswith("extcamera"):
            args = self._parse_args(line)
            args.pop(0)
            self.external_camera = {}
            self.external_camera['type'] = args.pop(0)
            if self.external_camera['type'] == "node":
                self.external_camera['node'] = self._resolve_node(args.pop(0))
            return

        if line.startswith("submesh_groundmodel"):
            self._add_global_data("\n" + line)
            return

        if line.startswith("SlopeBrake"):
            self._add_global_data("\n" + line)
            return

        if line.startswith("AntiLockBrakes"):
            self._add_global_data("\n" + line)
            return

        if line.startswith("TractionControl"):
            self._add_global_data("\n" + line)
            return

        if line.startswith("cruisecontrol"):
            self._add_global_data("\n" + line)
            return

        if line.startswith("speedlimiter"):
            self._add_global_data("\n" + line)
            return

        if line.startswith("fileformatversion"):
            self._add_global_data("\n" + line)
            return

        if line.startswith("author"):
            self._add_global_data("\n" + line)
            return

        if line.startswith("slidenode_connect_instantly"):
            self._add_global_data("\n" + line)
            return

        if line.startswith("enable_advanced_deformation"):
            self._add_global_data("\n" + line)
            return

        if line.startswith("lockgroup_default_nolock"):
            self._add_global_data("\n" + line)
            return

        if line.startswith("set_shadows"):
            self._add_global_data("\n" + line)
            return

        self.prop_camera_modes = getattr(self, "prop_camera_modes", [])
        if line.startswith("prop_camera_mode"):
            mode = {}
            self.prop_camera_modes.append(mode)

            mode['line']  = line_no
            mode['value'] = self._parse_args(line)[1]
            return

        self.flexbody_camera_modes = getattr(self, "flexbody_camera_modes", [])
        if line.startswith("flexbody_camera_mode"):
            mode = {}
            self.flexbody_camera_modes.append(mode)

            mode['line']  = line_no
            mode['value'] = self._parse_args(line)[1]


        self.add_animation = getattr(self, "animation", [])
        if line.startswith("add_animation"):
            anim = {}
            self.add_animation.append(anim)

            args = filter(len, re.split(r',',line[13:-1]))
            anim['ratio']    = args.pop(0)
            anim['option_1'] = args.pop(0)
            anim['option_2'] = args.pop(0)
            anim['source']   = args.pop(0)
            anim['mode']     = args.pop(0)
            if args: anim['event'] = args.pop(0)
            return

        if line.startswith("set_managedmaterials_options"):
            self._add_global_data("\n" + line)
            return

        self.beam_defaults_scale = getattr(self, "beam_defaults_scale", [])
        if line.startswith("set_beam_defaults_scale"):
            scale = {}
            self.beam_defaults_scale.append(scale)

            args = self._parse_args(line)
            args.pop(0)

            scale['line']   = line_no
            print line
            scale['spring'] = float(args.pop(0))
            scale['damp']   = float(args.pop(0))
            scale['deform'] = float(args.pop(0))
            scale['scale_break'] = float(args.pop(0))
            return

        if line.startswith("guid"):
            self._add_global_data("\n" + line)
            return
        
        self.beam_defaults = getattr(self, "beam_defaults", [])
        if line.startswith("set_beam_defaults"):
            defaults = {}
            self.beam_defaults.append(defaults)

            args = self._parse_args(line)
            args.pop(0)
            defaults['line']   = line_no
            defaults['spring'] = float(args.pop(0))
            defaults['damp']   = float(args.pop(0))
            defaults['deform'] = float(args.pop(0))
            defaults['break_force']  = float(args.pop(0))
            if args: defaults['diameter'] = float(args.pop(0))
            if args: defaults['ror_material'] = args.pop(0)
            if args: defaults['deform_plastic'] = float(args.pop(0))
            return

        self.inertia_defaults = getattr(self, 'inertia_defaults', [])
        if line.startswith("set_inertia_defaults"):
            defaults = {}
            self.inertia_defaults.append(defaults)

            args = self._parse_args(line)
            args.pop(0)

            defaults['line'] = line_no

            if len(args) == 1:
                defaults['default_value'] = True
                return

            defaults['start_delay']    = args.pop(0)
            defaults['stop_delay']     = args.pop(0)
            defaults['start_function'] = args.pop(0)
            defaults['stop_function']  = args.pop(0)
            return

        self.node_defaults = getattr(self, 'node_defaults', [])
        if line.startswith("set_node_defaults"):
            defaults = {}
            self.node_defaults.append(defaults)

            args = self._parse_args(line)
            args.pop(0)
            defaults['line']        = line_no
            defaults['load_weight'] = args.pop(0)
            defaults['friction']    = args.pop(0)
            defaults['volume']      = args.pop(0)
            defaults['surface']     = args.pop(0)
            if args: defaults['opts'] = args.pop(0)
            return

        if line.startswith("set_skeleton_settings"):
            self._add_global_data("\n" + line)
            return

        self.backmeshes = getattr(self, "backmeshes", [])
        if line.startswith("backmesh"):
            self.backmeshes.append(line_no)
            return

        self.submeshes = getattr(self, "submeshes", [])
        if line.startswith("submesh"):
            self.submeshes.append(line_no)
            return

        if line.startswith("set_collision_range"):
            self._add_global_data("\n" + line)
            return

        if self.mode == "nodes" or self.mode == "nodes2":
            if self._comment(line): return #Comments are not used for parsing nodes yet.

            args = self._parse_args(line)
            node = {}
            node['line'] = line_no
            node['id'] = args.pop(0)
            node['x'] = float(args.pop(0))
            node['y'] = float(args.pop(0))
            node['z'] = float(args.pop(0))
            if args: node['opts'] = args.pop(0)
            if args: node['mass'] = float(args.pop(0))

            self._add_node(node)
            return

        if self.mode == "camerarail":
            return

        if self.mode == "lockgroups":
            return

        if self.mode == "hooks":
            return

        if self.mode == "triggers":
            return

        self.beams = getattr(self, "beams", [])
        if self.mode == "beams":
            if self._comment(line):
                return

            args = self._parse_args(line)

            beam = {}
            self.beams.append(beam)

            beam['line']  = line_no
            beam['node1'] = self._resolve_node(args.pop(0))
            beam['node2'] = self._resolve_node(args.pop(0))
            if args: beam['opts'] = args.pop(0)
            if args: beam['support_length'] = int(args.pop(0))
            return

        self.triggers = getattr(self, "triggers", [])
        if self.mode == "triggers":
            if self._comment(line): return
            
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
            return
            
        self.shocks = getattr(self, "shocks", [])
        if self.mode == "shocks":
            if self._comment(line): return
            
            shock = {}
            self.shocks.append(shock)
            
            args = self._parse_args(line)
            shock['node1'] = self._resolve_node(args.pop(0))
            shock['node2'] = self._resolve_node(args.pop(0))
            shock['spring_in'] = float(args.pop(0))
            shock['damp_in'] = float(args.pop(0))
            shock['progressive_spring_in'] = 0.0
            shock['progressive_damp_in'] = 0.0
            shock['spring_out'] = shock['spring_in']
            shock['damp_out'] = shock['damp_in']
            shock['progressive_spring_out'] = 0.0
            shock['progressive_damp_out'] = 0.0
            shock['shortest_length'] = float(args.pop(0))
            shock['longest_length'] = float(args.pop(0))
            shock['precompression'] = float(args.pop(0))
            if args: shock['opts'] = args.pop(0)
            return

        self.shocks = getattr(self, "shocks", [])
        if self.mode == "shocks2":
            if self._comment(line): return
            
            shock = {}
            self.shocks.append(shock)
            
            args = self._parse_args(line)
            shock['node1'] = self._resolve_node(args.pop(0))
            shock['node2'] = self._resolve_node(args.pop(0))
            shock['spring_in'] = float(args.pop(0))
            shock['damp_in'] = float(args.pop(0))
            shock['progressive_spring_in'] = float(args.pop(0))
            shock['progressive_damp_in'] = float(args.pop(0))
            shock['spring_out'] = float(args.pop(0))
            shock['damp_out'] = float(args.pop(0))
            shock['progressive_spring_out'] = float(args.pop(0))
            shock['progressive_damp_out'] = float(args.pop(0))
            shock['shortest_length'] = float(args.pop(0))
            shock['longest_length'] = float(args.pop(0))
            shock['precompression'] = float(args.pop(0))
            if args: shock['opts'] = args.pop(0)
            return

        self.fixes = getattr(self, "fixes", [])
        if self.mode == "fixes":
            if self._comment(line): return
            self.fixes.append(self._resolve_node(line))
            return
        
        self.hydros = getattr(self, "hydros", [])
        if self.mode == "hydros":
            if self._comment(line): return
            
            hydro = {}
            self.hydros.append(hydro)
            
            args = self._parse_args(line)
            hydro['node1'] = self._resolve_node(args.pop(0))
            hydro['node2'] = self._resolve_node(args.pop(0))
            if args: hydro['ratio'] = float(args.pop(0))
            if args: hydro['opts'] = args.pop(0)
            if args: hydro['start_delay'] = float(args.pop(0))
            if args: hydro['stop_delay'] = float(args.pop(0))
            if args: hydro['start_function'] = args.pop(0)
            if args: hydro['stop_function'] = args.pop(0)
            return

        self.animators = getattr(self, "animators", [])
        if self.mode == "animators":
            if self._comment(line): return
            
            animator = {}
            self.animators.append(animator)

            args = filter(len, re.split(r',',line[9:-1]))                
            animator['node1'] = self._resolve_node(args.pop(0))
            animator['node2'] = self._resolve_node(args.pop(0))
            animator['factor'] = args.pop(0)
            animator['option'] = args.pop(0)
            return

        self.wheels = getattr(self, "wheels", [])
        if self.mode == "wheels":
            if self._comment(line): return
            
            wheel = {}
            self.wheels.append(wheel)
            
            args = self._parse_args(line)
            wheel['radius'] = float(args.pop(0))
            args.pop(0)
            wheel['rays'] = int(args.pop(0))
            wheel['node1'] = self._resolve_node(args.pop(0))
            wheel['node2'] = self._resolve_node(args.pop(0))
            wheel['rigidity_node'] = self._resolve_node(args.pop(0))
            wheel['braked'] = int(args.pop(0))
            wheel['driven'] = int(args.pop(0))
            wheel['reference_node'] = self._resolve_node(args.pop(0))
            wheel['mass'] = float(args.pop(0))
            wheel['spring'] = float(args.pop(0))
            wheel['damp'] = float(args.pop(0))
            wheel['face_material'] = args.pop(0)
            wheel['tread_material'] = args.pop(0)
            return
        
        self.wheels2 = getattr(self, "wheels2", [])
        if self.mode == "wheels2":
            if self._comment(line): return
            
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
            return

        self.meshwheels = getattr(self, "meshwheels", [])
        if self.mode == "meshwheels":
            if self._comment(line): return
            meshwheel = self._read_meshwheel(line)
            self.meshwheels.append(meshwheel)
            return

        self.meshwheels2 = getattr(self, "meshwheels2", [])        
        if self.mode == "meshwheels2":
            if self._comment(line): return
            meshwheel2 = self._read_meshwheel(line)
            self.meshwheels2.append(meshwheel2)
            return

        self.flexbodywheels = getattr(self, "flexbodywheels", [])
        if self.mode == "flexbodywheels":
            if self._comment(line): return
            
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
            return
        
        if self.mode == "globals":
            self._add_global_data(line)
            return
        
        self.cameras = getattr(self, "cameras", [])
        if self.mode == "cameras":
            if self._comment(line): return
            
            camera = {}
            self.cameras.append(camera)
            
            args = self._parse_args(line)
            camera['center'] = self._resolve_node(args.pop(0))
            camera['back'] = self._resolve_node(args.pop(0))
            camera['left'] = self._resolve_node(args.pop(0))
            return
        
        if self.mode == "engine":
            self._add_global_data(line)
            return
        
        self.texcoords = getattr(self, "texcoords", [])
        if self.mode == "texcoords":
            if self._comment(line): return
            
            texcoord = {}
            self.texcoords.append(texcoord)
            
            args = self._parse_args(line)
            texcoord['line'] = line_no
            texcoord['node'] = self._resolve_node(args.pop(0))
            texcoord['u'] = float(args.pop(0))
            texcoord['v'] = float(args.pop(0))
            return
        
        self.cabs = getattr(self, "cabs", [])
        if self.mode == "cab":
            if self._comment(line): return
            
            cab = {}
            self.cabs.append(cab)
            
            args = self._parse_args(line)
            cab['line'] = line_no
            cab['node1'] = self._resolve_node(args.pop(0))
            cab['node2'] = self._resolve_node(args.pop(0))
            cab['node3'] = self._resolve_node(args.pop(0))
            if args: cab['args'] = args.pop(0)
            return
        
        self.commands = getattr(self, "commands", [])
        if self.mode == "commands" or self.mode == "commands2":
            command = {}
            self.commands.append(command)
            
            args = self._parse_args(line)
            command['node1'] = self._resolve_node(args.pop(0))
            command['node2'] = self._resolve_node(args.pop(0))
            command['short_rate'] = float(args.pop(0))
            if self.mode == "commands":
                command['long_rate'] = float(args.pop(0))
            else: #mode is commands2
                command['long_rate'] = command['short_rate']
            command['amount_short'] = float(args.pop(0))
            command['amount_long'] = float(args.pop(0))
            command['short_key'] = str(args.pop(0))
            command['long_key'] = str(args.pop(0))
            if args: command['options_var'] = args.pop(0)
            if args: command['description'] = args.pop(0)
            if args: command['start_delay'] = float(args.pop(0))
            if args: command['stop_delay'] = float(args.pop(0))
            if args: command['start_function'] = args.pop(0)
            if args: command['stop_function'] = args.pop(0)
            if args: command['affect_engine'] = int(args.pop(0))
            return
        
        self.cinecams = getattr(self, "cinecams", [])
        if self.mode == "cinecam":
            cinecam = {}
            self.cinecams.append(cinecam)
            
            args = self._parse_args(line)
            cinecam['x'] = args.pop(0)
            cinecam['y'] = args.pop(0)
            cinecam['z'] = args.pop(0)
            cinecam['nodes'] = []
            for _ in range(8): cinecam['nodes'].append(self._resolve_node(args.pop(0)))
            if args: cinecam['spring'] = float(args.pop(0))
            if args: cinecam['damp'] = float(args.pop(0))
            return
        
        if self.mode == "flares" or self.mode == "flares2": return
        
        self.contacters = getattr(self, "contacters", [])
        if self.mode == "contacters":
            if self._comment(line):
                return
            self.contacters.append(self._resolve_node(line))
        
        if self.mode == "ropes": return
        if self.mode == "props": return
        if self.mode == "globeams": return
        if self.mode == "wings": return
        if self.mode == "turboprops" or self.mode == "turboprops2": return
        if self.mode == "fusedrag": return
        if self.mode == "engoption": return
        if self.mode == "brakes": return
        if self.mode == "rotators" or self.mode == "rotators2": return
        if self.mode == "screwprops": return
        if self.mode == "guisettings": return
        if self.mode == "minimass": return
        if self.mode == "exhausts": return
        if self.mode == "particles": return
        if self.mode == "turbojets": return
        if self.mode == "rigidifiers": return
        if self.mode == "airbrakes": return
        if self.mode == "flexbodies": return
        if self.mode == "hookgroup": return
        if self.mode == "materialflarebindings": return
        if self.mode == "soundsources": return
        if self.mode == "soundsources2": return
        if self.mode == "soundsources2": return
        if self.mode == "envmap": return
        if self.mode == "managedmaterials": return
        if self.mode == "sectionconfig": return
        if self.mode == "section": return
        if self.mode == "torquecurve": return
        if self.mode == "advanceddrag": return
        if self.mode == "axles": return
        if self.mode == "railgroups": return
        
        self.slidenodes = getattr(self, "slidenodes", [])
        if self.mode == "slidenodes":
            slidenode = {}
            self.slidenodes.append(slidenode)
            
            args = self._parse_args(line)
            slidenode['nodes'] = []
            for arg in args:
                first_char = arg[0].lower()
                
                if first_char.isdigit():
                    node = self._resolve_node(arg)
                    if 'id' not in slidenode:
                        slidenode['id'] = node
                    else:
                        slidenode['nodes'].append(node)
                if first_char == "s":
                    slidenode['spring'] = float(arg[1:-1])
                    
                if first_char == "b": 
                    slidenode['break_amount'] = float(arg[1:-1])
                    
                if first_char == "t":
                    slidenode['tolerence'] = float(arg[1:-1])
             
            return
        if self.mode == "nodecollision": return
        if self.mode == "vidcam": return
            
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
    
    def _add_global_data(self, data):
        self.global_data = getattr(self, "global_data", "")
        self.global_data += data + "\n"
        

