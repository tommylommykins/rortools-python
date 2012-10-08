require 'yaml'

class YamlInterpreter
  def initialize yaml_string
    @data = YAML::load yaml_string
    @data.delete "separators"
    @data.delete "ranges"
    @data.delete "ui_controls"
  end
  
  def make_custattribute section_name
    ret = new_line "global ror#{section_name} = attributes #{section_name}type"
    ret += max_indent do
      ret = new_line "parameters #{section_name}parameters rollout:#{section_name}rollout"
      ret += max_indent do
        ret = ""
        @data[section_name].each do |member|
          next if member['ui_control'].nil?
          current_line = ""
          current_line += "#{member['name']} ui:ui#{member['name']} type:#{max_type member['type']} default:#{member['default'].inspect}"
          ret += new_line current_line
        end
        ret
      end
      ret += new_line "rollout #{section_name}rollout \"RoR Data\""
      ret += max_indent do
        ret = ""
        @data[section_name].each do |member|
          next if member['ui_control'].nil?
          current_line = "#{member['ui_control']} ui#{member['name']} \"#{member['description']}\""
          current_line += " range:#{member['range']}" if member['range']
          current_line += " scale:#{member['scale']}" if member['scale']
          ret += new_line current_line
          ret
        end
        ret
      end
      ret
    end
    ret
  end
  
  def make_python_parser section_name
    ret = new_line "self.#{section_name} = getattr(self, #{section_name}, [])"
    ret += new_line "if self.mode == #{section_name}:"
    ret += python_indent do
      ret  = new_line "if self._comment(line): return" 
      ret += new_line
      ret += new_line "the_dict = {}"
      ret += new_line "self.#{section_name}.append(the_dict)"
      ret += new_line
      ret += new_line "args = self._parse_args(line)"
      @data[section_name].each do |member|
        current_line = ""
        current_line += "if args: " if member['optional']
        current_line += "the_dict['#{member['name']}'] = "
        if member['name'] =~ /node\d/
          current_line += "self._resolve_node(args.pop(0))"
        else
          current_line += "#{python_type member['type']}(args.pop(0))"
        end
        ret += new_line current_line
      end
      ret += new_line "return" 
    end
    ret
  end
  
  def make_python_exporter section_name
    ret = new_line "def render(self):"
    ret += python_indent do
      ret = new_line "if not self.has_custattribute(\"#{section_name}type:#{section_name}type\"):"
      ret += python_indent do
        ret = new_line "mxs.custattributes.add(self.max_object, mxs.ror#{section_name})"
        ret
      end
      ret += new_line
      ret += new_line "ret = \"\""
      ret += new_line "for node1, node2 in self.all_beams():"
      ret += python_indent do
        ret = ""
        @data[section_name].each do |member|
          current_line = "ret += #{member['separator'].inspect} + str("
          if member['ui_control'].nil?
            if member['name'] =~ /node\d/
              current_line += "self.nodes.index(self.nearest_node(#{member['name']}))"
            else
              current_line += "**#{member['name']} goes here**"
            end
          else
            current_line += "self.max_object.#{member['name']})"
          end
          ret += new_line current_line
        end
        ret
      end
      ret += new_line "return ret"
      ret
    end
    ret
  end
  
  private
  
  def python_type type_string
    case type_string
    when "string"
      "str"
    when "float"
      "float"
    else
      raise "unknown type: #{type_string}"
    end
  end
  
  def max_type type_string
    case type_string
    when "string"
      "#string"
    when "float"
      "#float"
    else
      raise "unknown type: #{type_string}"
    end
  end
  
  def python_indent &b
    indent = " " * 4
    yield.lines.map {|line| "#{indent}#{line}"}.join
  end
  
  def max_indent &b
    indent = " " * 4
    new_line('(') +
    yield.lines.map {|line| "#{indent}#{line}"}.join +
    new_line(')')
  end
  
  def new_line contents=""
    "#{contents}\n"
  end
end

x = YamlInterpreter.new File.read "truck-file-line-descriptions.yml"
puts x.make_python_parser "shocks2"
puts x.make_custattribute "shocks2"
puts x.make_python_exporter "shocks2"