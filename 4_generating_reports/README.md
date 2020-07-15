[:arrow_backward: Previous: Autonomous Flow](../3_rtl_to_gds_autonomous_flow) &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;        [Next: Antenna Fix Example :arrow_forward:](../5_antenna_fix_example)

# Generating Reports

At this point, we have successfully run OpenROAD flow and got all results of the flow. In this part, we will learn how to generate reports for a routed design.


## Load Design

We start by loading the design.

```Tcl
read_lef "data/NangateOpenCellLibrary.tech.lef"
read_lef "data/NangateOpenCellLibrary.macro.mod.lef"
read_liberty "data/NangateOpenCellLibrary_typical.lib"
read_def "data/aes_final.def"
read_sdc "data/constr.sdc"
```

### Report Minimum Path Delay

```Tcl
report_checks -path_delay min -fields {slew cap input nets fanout} -format full_clock_expanded
```

### Report Maximum Path Delay

```Tcl
report_checks -path_delay max -fields {slew cap input nets fanout} -format full_clock_expanded
```

### Report Total Negative Slack (TNS)

```Tcl
report_tns
```

### Report Worst Negative Slack (WNS)

```Tcl
report_wns
```

### Report Power

```Tcl
report_power
```

### Report Design Area

```Tcl
report_design_area
```

## Conclusion
In this section, we have shown how to report essential metrics for your design.

> Did you notice that these metrics are reported by default in the autonomous flow?

In the next section, we will show an example for **Antenna Fixing** using only the Tcl interface of OpenROAD.

[:arrow_backward: Previous: Autonomous Flow](../3_rtl_to_gds_autonomous_flow) &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;        [Next: Antenna Fix Example :arrow_forward:](../5_antenna_fix_example)