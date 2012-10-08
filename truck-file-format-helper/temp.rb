class PythonMaker
  def python_code &b
    instance_eval &b
  end
  
  def python_indent &b
    python_code(&b).split.map {|l| indent_line l}.join("\n")
  end
  
  def lines *contents
    acc = ""
    contents.each {|thing| acc << "#{thing}\n"}
    acc
  end
  
  private 
  def indent_line line
    "    #{line}"
  end
end

def stuff
  maker = PythonMaker.new
  baz = "lololol"
  maker.python_code do
    lines "foo",
    "bar",
    baz,
    python_indent {
      lines "baz",
      "derpina"
    }
  end
end

puts stuff