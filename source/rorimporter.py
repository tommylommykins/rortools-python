from Py3dsMax import mxs

import re

class Importer:
    def __init__(self):
        self.load_truck_file()
    
    def load_truck_file(self):
        self.truck_file_contents = open(mxs.getopenfilename()).read()
    

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
        truck_file_contents = open(truck_file).read()

        self.mode = "NONE"
        current_line = -1
        for l in truck_file_contents.splitlines():
            current_line += 1
            line = l.strip()

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
            #if line.startswith("prop_camera_mode")
            #flexbody_camera_mode

            if line.startswith("add_animation"):
                args = filter(len, re.split(r',',line))
                args.pop(0)
                self.animation = {}
                self.animation['ratio']    = args.pop(0)
                self.animation['option_1'] = args.pop(0)
                self.animation['option_2'] = args.pop(0)
                self.animation['source']   = args.pop(0)
                self.animation['mode']     = args.pop(0)
                if args:
                    self.add_animation['event'] = args.pop(0)
                continue

            if line.startswith("set_managedmaterials_options"):
                self.managed_materials_options = self._parse_args(line).pop(0)
                continue

            #broken. Positional
            if line.startswith("set_beam_defaults_scale"):
                args = self._parse_args(line)
                args.pop(0)

                if not hasattr(self, "beam_defaults_scale"):
                    self.beam_defaults_scale = []
                scale = {}
                self.beam_defaults_scale.insert(0, scale)

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
                args = self._parse_args(line)
                args.pop(0)
                self.beam_defaults = {}


            print line

    def _parse_args(self, data):
        unfiltered_args = re.split(r":|\||,| |\t", data)
        return filter(len, unfiltered_args)
        
#Importer()
x = TruckFileReader()
x.load_truck(mxs.getopenfilename())
print x.beam_defaults_scale