puts File.read("sections.txt").scan(/\".*?"/).map {|s| s.gsub(/"/,"")}.delete_if {|s| s =~ /BTS_(IN_SECTION|SECTION(?!CONFIG)|COMMENT)/}.inspect