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
        for l in truck_file_contents.splitlines():
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
                self.external_camera = args.pop(0)
                if self.external_camera == "node":
                    self.external_camera_node = args.pop(0)

            if line.startswith("submesh_groundmodel"):
                args = self._parse_args(line)
                args.pop(0)
                self.submesh_ground_model = args.pop(0)

            if line.startswith("SlopeBrake"):
                args = self._parse_args(line)
                args.pop(0)
                self.slope_regulating_force = args.pop(0)
                self.slope_attack_angle = args.pop(0)
                self.slope_release_angle = args.pop(0)

            if line.startswith("AntiLockBrakes"):
                args = self._parse_args(line)
                args.pop(0)
                self.anti_lock_regulating_force = args.pop(0)
                self.anti_lock_min_speed = args.pop(0)
                self.anti_lock_pulse_rate = args.pop(0)


            print line

    def _parse_args(self, data):
        unfiltered_args = re.split(r":|\||,| |\t", data)
        return filter(len, unfiltered_args)
        
#Importer()
x = TruckFileReader()
x.load_truck(mxs.getopenfilename())
print x.file_info['file_version']