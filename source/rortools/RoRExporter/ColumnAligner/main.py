class RoRColumnAligner(object):
    def ror_align_by_column(self, truck_file):
        """Aligns the lines of a truck_file 
        """
        truck_file_sections = self._split_file(truck_file)
        aligned_sections = map(self._align_group, truck_file_sections)
        ret = []
        for section in aligned_sections:
            for line in section:
                ret.append(line)
        return "\n".join(ret)
        
    def _split_file(self, truck_file):
        """Splits a truck file into constituent sections for the purposes of creating groups to independently align by column.
        """
        grouper = RoRSectionGrouper()
        for line in truck_file.splitlines():
            if grouper.new_group_needed(line):
                grouper.new_group()
            grouper.add_line(line)
        return grouper.get_groups()
    
    def _align_group(self, group):
        max_lengths = self._max_lengths(group)
        if not max_lengths:
            return group
        ret = []
        for line in group:
            new_line = ""
            if self._line_should_be_ignored(line):
                ret.append(line)
            else:
                for i, field in enumerate(line.split(",")):
                    pad_length = max_lengths[i] - len(field)
                    new_field = (" " * pad_length) + field + ", "
                    new_line = new_line + new_field
                ret.append(new_line[:-2])
        return ret
    
    def _max_lengths(self, group):
        max_lengths = []
        for line in group:
            if self._line_should_be_ignored(line):
                continue
            column_lengths = map(len, line.split(","))
            for i, length in enumerate(column_lengths):
                if i + 1 > len(max_lengths):
                    max_lengths.append(length)
                    continue
                if length > max_lengths[i]:
                    max_lengths[i] = length
        return max_lengths
    
    def _line_should_be_ignored(self, line):
        if line.startswith("set_beam_defaults") or \
           line.startswith(";") or \
           len(line.split(",")) == 1:
            return True
                
class RoRSectionGrouper(object):
    def __init__(self):
        self.groups = []
        self.new_group()
        
    def new_group(self):
        self.current_group = []
        self.groups.append(self.current_group)
    
    def new_group_needed(self, line):
        line = line.strip()
        if not line:
            return True
        if ("," not in line) and (" " not in line):
            return True
        return False
    
    def add_line(self, line):
        self.current_group.append(line)
        
    def get_groups(self):
        return self.groups