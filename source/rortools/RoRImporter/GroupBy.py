def group_by_comparison_function(comparison_function, data):
    """Group data into separate bins according whether the comparison function declares
    that any two items match
    
    for example:
    group_by_comparison_function(lambda this, other: isinstance(this.__class__, other),[1, "abc", 2])
    returns
    [[1, 2], ["abc"]]
    """
    bins = []
    for item in data:
        match_index = None
        for i, a_bin in enumerate(bins):
            if comparison_function(item, a_bin[0]):
                match_index = i
                break
        if match_index is not None:
            bins[match_index].append(item)
        else:
            bins.append([item])
    return bins

class DictHelper(object):
    """A class to aid the comparisons done with group_by_comparison_function
    for use when both objects being compared are dicts.
    """
    def __init__(self):
        self.dont_autocompare = []
        
    def perform_camparison(self, this, other):
        """Compares all values of each dict to make sure they are the same,
        except where values have been explicitly forbidden from being compared
        """
        for key in this.keys():
            if key in self.dont_autocompare:
                continue
            if this[key] != other[key]:
                return False
        if not hasattr(self, "custom_comparison"):
            return True
        
        return self.custom_comparison(self.this, self.other)