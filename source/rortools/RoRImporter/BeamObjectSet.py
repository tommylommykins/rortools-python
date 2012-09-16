from Py3dsMax import mxs
import BeamObject

class BeamObjectSet(object):
    def __init__(self, name, beam_defaults):
        """To help separate beams in the editor, they are grouped according to comments in the truck file:
        Wherever there is a comment in the beams section, a new Max object is created for all subsequent
        beams, whose name is taken from that comment.
        Individual beams can take various arguments in truck files. 3ds max cannot easily support this,
        so instead beams with the same arguments are grouped together.

        This method creates a set of beam objects, one for each possible combination of arguments
        so that individual beams can be placed in the appropriate subgroups. For each beam that 
        is imported, the appropriate subgroup is chosen by _select_beam_object. 
        """
        #the old beam object set becomes unused at this point, so any empty objects should be
        #deleted now.
        combinations = self._all_combinations(("invisible", "rope", "support"))
        self.beam_object_set = {}
        
        for combination in combinations: 
            python_name = "_".join(combination)
            beam_object = BeamObject.RoRBeam(name)
            beam_object.apply_beam_defaults(beam_defaults)
            self.beam_object_set[python_name] = beam_object
            
            for property_name in combination:
                setattr(beam_object, property_name, True)
                
        #normal (ie. no options) is a special case:
        normal = BeamObject.RoRBeam(name)
        normal.apply_beam_defaults(beam_defaults)
        self.beam_object_set['normal'] = normal
        
    
    def _all_combinations(self, lst):
        """Generates the set of all possible combinations of all lengths of items in a list"""
        import itertools
        ret = []
        for i in range(len(lst)):
            length = i + 1
            ret.extend(list(itertools.combinations(lst, length)))
        return ret
    
    def delete_unused_beam_objects(self):
        """Deletes all objects in a beam object set if they contain no beams.
        Done because beam objects are pregenerated without first finding out whether
        all combinations are actually are needed or not, so some non-useful ones are
        generated.
        """
        if not hasattr(self, "beam_object_set"): 
            return
        for beam_object in self.beam_object_set.itervalues():
            if mxs.numSplines(beam_object.max_object) == 0:
                mxs.delete(beam_object.max_object)
                
    def select_beam_object(self, beam):
        """Selects a beam object from a set, so that a beam may be placed into the correct one.
        The correct object is chosen by inspection of the arguments on the beam itself. 
        """
        if not 'options' in beam: return self.beam_object_set['normal']
        
        option = "".join(sorted(list(beam['options'].strip().lower())))
        
        if 'n' in option: return self.beam_object_set['normal']
        
        if 'i' in option and 'r' in option and 's' in option:
            return self.beam_object_set['invisible_rope_support']
        
        if 'i' in option and 'r' in option: return self.beam_object_set['invisible_rope']
        if 'i' in option and 's' in option: return self.beam_object_set['invisible_support']
        if 'r' in option and 's' in option: return self.beam_object_set['rope_support']
        
        if 'i' in option: return self.beam_object_set['invisible']
        if 'r' in option: return self.beam_object_set['rope']
        if 's' in option: return self.beam_object_set['support']

        #default, used for invalid arguments 
        return self.beam_object_set['normal']
    