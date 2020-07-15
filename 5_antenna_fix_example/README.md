[:arrow_backward: Previous: Generating Report](../4_generating_reports) &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;        [Next: Visualizing using KLayout :arrow_forward:](../6_visualizing_using_klayout/README.md)

# Antenna Fix Example

Contributed by: [Mehdi Saligane](https://github.com/msaligane).

In this section, we will build an antenna checker completely in `Tcl`.

### Load Antenna Rules

```Tcl
proc load_antenna_rules { } {
  antenna_checker::load_antenna_rules
}
```

### Check Antennas

```Tcl
proc check_antennas { args } {
  sta::parse_key_args "check_antennas" args \
  keys {-path} \
  flags {}

  antenna_checker::antennachecker_set_verbose [info exists flags(-verbose)]
  antenna_checker::load_antenna_rules
  antenna_checker::check_antennas $keys(-path)
}
```

### Check Net Violations

```Tcl
proc get_met_avail_length { args } {
  sta::parse_key_args "get_met_rest_length" args \
    keys {-net_name -route_level} \
    flags {}

  if { [info exists keys(-net_name)] } {
    set netname $keys(-net_name)
    antenna_checker::antennachecker_set_net_name $netname

    if { [info exists keys(-route_level)] } {
      set rt_lv $keys(-route_level)
      sta::check_positive_integer "-route_level" $rt_lv
      antenna_checker::antennachecker_set_route_level $rt_lv
    } else {
      ord::error "no -route_level specified."
    }
  } else {
    ord::error "no -net_name specified."
  }
  antenna_checker::get_met_avail_length
}

proc check_net_violation { args } {
  sta::parse_key_args "check_net_violation" args \
  keys {-net_name} \
  flags {}

  if { [info exists keys(-net_name)] } {
    set netname $keys(-net_name)
    set res [antenna_checker::check_net_violation $netname]
    
    return $res
  } else {
    ord::error "no -net_name specified."
  }  
  
  return 0
}
```

### Add Antenna Cell

```Tcl
proc add_antenna_cell { net antenna_cell_name sink_inst antenna_inst_name } {

  set block [[[::ord::get_db] getChip] getBlock]
  set net_name [$net getName]

  set antenna_master [[::ord::get_db] findMaster $antenna_cell_name]
  set antenna_mterm [$antenna_master getMTerms]

  set inst_loc_x [lindex [$sink_inst getLocation] 0]
  set inst_loc_y [lindex [$sink_inst getLocation] 1]
  set inst_ori [$sink_inst getOrient]

  set antenna_inst [odb::dbInst_create $block $antenna_master $antenna_inst_name]
  set antenna_iterm [$antenna_inst findITerm "A"]

  $antenna_inst setLocation $inst_loc_x $inst_loc_y
  $antenna_inst setOrient $inst_ori
  $antenna_inst setPlacementStatus PLACED
  odb::dbITerm_connect $antenna_iterm $net

}
```

### Antenna Fixing

```Tcl
proc antenna_fixing {} {

  set block [[[::ord::get_db] getChip] getBlock]
  
  foreach inst [$block getInsts] {
    if {[[$inst getMaster] getType] == "CORE_SPACER"} {
      odb::dbInst_destroy $inst
    }
  }
  
  set antenna_cell_name "ANTENNA3_A9PP84TR_C14"
  
  set target_file "6_final_with_diodes"
  
  set iterate_times 0
  
  set antenna_node_counts 0
  
  while { $iterate_times < 1 } {
  
    set nets [$block getNets]
  
    foreach net $nets {
      set net_name [$net getConstName]
      set flag [check_net_violation -net_name $net_name]
      if {$flag == 0} {
        continue
      }
  
      if { [$net isSpecial] } {
        continue
      }
  
      foreach iterm [$net getITerms] {
        set inst [$iterm getInst]
  
        dict set inst_count $inst [expr [dict get $inst_count $inst] + 1]
  
        set count [dict get $inst_count $inst]
  
        set antenna_inst_name "ANTENNA"
        append antenna_inst_name "_" [$inst getName] "_" $count
  
        if {[catch {add_antenna_cell $net $antenna_cell_name $inst $antenna_inst_name} result] } {
          puts "adding node failed"
          continue
        } else {
          set antenna_inst [$block findInst $antenna_inst_name]
          dict set inst_count $antenna_inst 1
          set antenna_node_counts [expr $antenna_node_counts + 1]
        }
  
        break
  
      }
  
      if { $antenna_node_counts == 4 } {
        break
      }
    }
  
    set iterate_times [expr $iterate_times + 1]
  
  }
  
  set verilog_file_name "$target_file.v"
  write_verilog  $verilog_file_name
  
  set def_file_name "$target_file.def"
  write_def $def_file_name

}
```

### Putting It All Together

```Tcl
read_lef "data/NangateOpenCellLibrary.tech.lef"
read_lef "data/NangateOpenCellLibrary.macro.mod.lef"
read_liberty "data/NangateOpenCellLibrary_typical.lib"
read_def "data/aes_final.def"
read_sdc "data/constr.sdc"

set_propagated_clock [all_clocks]
```

TODO


## Conclusion
In this part, we have used OpenROAD `Tcl` interface to build an Antenna Checker and Fixer. This shows how far you can go with the tool using only its `Tcl` interface.

In the next section, we will give a brief overview on using KLayout for visualization.

[:arrow_backward: Previous: Generating Report](../4_generating_reports) &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;        [Next: Visualizing using KLayout :arrow_forward:](../6_visualizing_using_klayout/README.md)