read_lef "data/NangateOpenCellLibrary.tech.lef"
read_lef "data/NangateOpenCellLibrary.macro.mod.lef"
read_liberty "data/NangateOpenCellLibrary_typical.lib"
read_def "data/aes_final.def"
read_sdc "data/constr.sdc"

set_propagated_clock [all_clocks]


puts "\n=========================================================================="
puts "report_checks -path_delay min"
puts "--------------------------------------------------------------------------"
report_checks -path_delay min -fields {slew cap input nets fanout} -format full_clock_expanded

puts "\n=========================================================================="
puts "report_checks -path_delay max"
puts "--------------------------------------------------------------------------"
report_checks -path_delay max -fields {slew cap input nets fanout} -format full_clock_expanded

puts "\n=========================================================================="
puts "report_tns"
puts "--------------------------------------------------------------------------"
report_tns

puts "\n=========================================================================="
puts "report_wns"
puts "--------------------------------------------------------------------------"
report_wns

puts "\n=========================================================================="
puts "report_power"
puts "--------------------------------------------------------------------------"
report_power

puts "\n=========================================================================="
puts "report_design_area"
puts "--------------------------------------------------------------------------"
report_design_area

exit