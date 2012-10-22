from Py3dsMax import mxs
from ..MaxObjects import BeamThing
from ..MaxObjects import Beam

class BeamObjectBuilder(object):
    def make_node_beam(self, node_positions, beams, comments, beam_defaults, object_holder):
        """Generates the 3ds Max representation of the beams of a truck.
        """
        default_beam_defaults = {'line': 0, 'spring':-1,
                                 'damp':-1, 'deform':-1,
                                 'break_force': 0 }
        beam_defaults.append(default_beam_defaults)
        beam_set = BeamObjectSet("beam_1", beam_defaults[-1], object_holder)
        self.comment_tracker = CommentTracker(comments)
        self.beam_default_tracker = BeamDefaultTracker(beam_defaults)
        for beam in beams:
            #Create a new beam object if necessary
            if self._new_beam_section_required(beam, beam_defaults):
                comment = self.comment_tracker.applicable_comment(beam)
                defaults = self.beam_default_tracker.applicable_beam_default(beam)
                beam_set.delete_old_set_and_make_new_set(comment, defaults)
            
            #Add a beam
            node1 = node_positions[beam['node1']]
            node2 = node_positions[beam['node2']]
            beam_object = beam_set.select_beam_object(beam, self._get_category(node1, node2))
            
            beam_object.draw_line(node1, node2)
        beam_set.delete_unused_beam_objects()
        
    def _get_category(self, node1, node2):
        node1_cat = node1.separation_category
        node2_cat = node2.separation_category
        return Category(node1_cat, node2_cat)
    
    def _new_beam_section_required(self, beam, beam_defaults):
        if not (self.comment_tracker.new_comment_in_beam_section(beam) or
                self.beam_default_tracker.new_beam_default_in_beam_section(beam)):
            return False
        
        self.previous_beam_default = self.beam_default_tracker.applicable_beam_default(beam)
        return True
    
class Category(object):
    def __init__(self, category1=None, category2=None):
        if category1 is None:
            category1 = ""
        if category2 is None:
            category2 = ""
        self.category1 = str(category1)
        self.category2 = str(category2)
        
    def key(self):
        return (self.category1, self.category2)
    
    def __hash__(self):
        return self.key().__hash__()
        
    def __eq__(self, other):
        return self.key().__eq__(other.key())
    
class CategoryManager(object):
    """Class for holding beams of different categories.
    """
    def __init__(self, beam_object_set):
        self.categories = getattr(self, "categories", {})
        self.new_category(Category("default_category",), beam_object_set)
        
    def new_category(self, category, beam_object_set):
        """Creates a new category. The specified argument must be a category object.
        """ 
        if category in self.categories:
            return
        self.categories[category] = beam_object_set
        
    def has_category(self, category):
        return category in self.categories
    
    def get_category(self, category):
        if not category:
            return self.categories[Category("default_category")]
        
        return self.categories[category]
                  
class CommentTracker(object):
    """Keeps track of which comment was the last comment seen according to line number.
    Detects when a new comment has been found.
    Comments must be processed in line-number-order for functionality to be correct.
    """
    def __init__(self, comments):
        self.comments = sorted(comments, key=lambda comment: comment['line_no'])
        self.previous_comment = None
    
    def applicable_comment(self, beam):
        """Gets previous comment relative to the line of the specified beam in the truck file.
        """
        specified_line = beam['line']
        for comment in reversed(self.comments):
            if comment['line_no'] < specified_line: return comment['text']
        return None
    
    def new_comment_in_beam_section(self, beam):
        """To provide differentiation between beams, whenever a comment is reached in the
        truck file, a new 3dsmax spline object is created. This method detects when a new
        comment has been found. 
        """
        current_comment = self.applicable_comment(beam)
        if self.previous_comment == current_comment: return False
        self.previous_comment = current_comment
        return True
    
class BeamDefaultTracker(object):
    """Keeps track of which set_beam_defaults was the last one seen according to line number.
    """
    def __init__(self, beam_defaults):
        self.defaults = sorted(beam_defaults, key=lambda default: default['line'])
        self.previous_default = None
        
    def applicable_beam_default(self, beam):
        """Gets the set_beam_defaults entry which is is effect at the line specified
        Returns None if there is no set_beam_defaults at before the line."""
        specified_line = beam['line'] 
        for default in reversed(self.defaults):
            if default['line'] < specified_line:
                return default

    def new_beam_default_in_beam_section(self, beam):
        """To correctly implement set_beam_defaults, a new set of beam objects must be created
        whenever a new set_beam_defaults appears. This method detects when the new defaults has
        appeared."""
        current_default = self.applicable_beam_default(beam)
        if self.previous_default == current_default: return False
        self.previous_default = current_default
        return True 

class BeamObjectSet(object):
    def __init__(self, name, beam_defaults, object_holder):
        """To help separate beams in the editor, they are grouped according to comments in the truck file:
        Wherever there is a comment in the beams section, a new Max object is created for all subsequent
        beams, whose name is taken from that comment.
        Individual beams can take various arguments in truck files. 3ds max cannot easily support this,
        so instead beams with the same arguments are grouped together.
        """
        self.name = name
        self.beam_defaults = beam_defaults
        self.object_holder = object_holder
        new_set = self._new_set(self.name,
                                self.beam_defaults,
                                Category("default_category"))
        self.category_manager = CategoryManager(new_set)
        self.delete_old_set_and_make_new_set(self.name, self.beam_defaults)
        
    def delete_old_set_and_make_new_set(self, name, beam_defaults):
        #delete old set
        self.delete_unused_beam_objects()
        
        #make new set
        self.name = name
        self.beam_defaults = beam_defaults
        self.category_manager = CategoryManager(self._new_set(name, beam_defaults, Category("default_category")))
        
    
    def _new_set(self, name, beam_defaults, category):
        """This method creates a set of beam objects, one for each possible combination of arguments
        so that individual beams can be placed in the appropriate subgroups. For each beam that 
        is imported, the appropriate subgroup is chosen by _select_beam_object. 
        """
        combinations = self._all_combinations(("invisible", "rope", "support"))
        beam_object_set = {}
        
        for combination in combinations: 
            python_name = "_".join(combination)
            beam_object = Beam.RoRBeam(name)
            beam_object.apply_beam_defaults(beam_defaults)
            beam_object_set[python_name] = beam_object
            
            for property_name in combination:
                setattr(beam_object, property_name, True)
            
            beam_object.apply_category(category)
                
        #normal (ie. no options) is a special case:
        normal = Beam.RoRBeam(name)
        normal.apply_beam_defaults(beam_defaults)
        normal.apply_category(category)
        beam_object_set['normal'] = normal
        return beam_object_set
    
    def delete_unused_beam_objects(self):
        """Deletes all objects in a beam object set if they contain no beams.
        Done because beam objects are pregenerated without first finding out whether
        all combinations are actually are needed or not, so some non-useful ones are
        generated. 
        """
        for the_set in self.category_manager.categories.values():
            for key, beam_object in the_set.items():
                if mxs.numSplines(beam_object.max_object) == 0:
                    mxs.delete(beam_object.max_object)
                    del the_set[key]
        self._add_objects_to_object_holder(self.object_holder)
                
    def _add_objects_to_object_holder(self, object_holder):
        for the_set in self.category_manager.categories.values():
            for beam_object in the_set.itervalues():
                object_holder.add_object(beam_object.max_object)

    def select_beam_object(self, beam, category):
        """Selects a beam object from a set, so that a beam may be placed into the correct one.
        The correct object is chosen by inspection of the arguments on the beam itself. 
        """
        if not self.category_manager.has_category(category):
            self.category_manager.new_category(category, self._new_set(self.name,
                                                                       self.beam_defaults,
                                                                       category))
        beam_object_set = self.category_manager.get_category(category)
        if not 'options' in beam: return beam_object_set['normal']
        
        option = "".join(sorted(list(beam['options'].strip().lower())))
        
        if 'n' in option: return self.beam_object_set['normal']
        
        if 'i' in option and 'r' in option and 's' in option:
            return beam_object_set['invisible_rope_support']
        
        if 'i' in option and 'r' in option: return beam_object_set['invisible_rope']
        if 'i' in option and 's' in option: return beam_object_set['invisible_support']
        if 'r' in option and 's' in option: return beam_object_set['rope_support']
        
        if 'i' in option: return beam_object_set['invisible']
        if 'r' in option: return beam_object_set['rope']
        if 's' in option: return beam_object_set['support']

        #default, used for invalid arguments 
        return beam_object_set['normal']
    
    def _all_combinations(self, lst):
        """Generates the set of all possible combinations of all lengths of items in a list"""
        import itertools
        ret = []
        for i in range(len(lst)):
            length = i + 1
            ret.extend(list(itertools.combinations(lst, length)))
        return ret
    
def import_beams(node_positions, beams, comments, beam_defaults, object_holder):
    builder = BeamObjectBuilder()
    builder.make_node_beam(node_positions, beams, comments, beam_defaults, object_holder)
    