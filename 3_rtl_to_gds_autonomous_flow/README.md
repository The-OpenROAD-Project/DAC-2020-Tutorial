[:arrow_backward: &nbsp; Previous: Database access, features and tools](../2_database_access) &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;        [Next: Generating Reports &nbsp; :arrow_forward:](../4_generating_reports)

# RTL to GDS Autonomous Flow

In this part, we are going to run a full RTL-to-GDS flow using AES design on Nangate45. 

## Clone OpenROAD-flow

```shell
git clone https://github.com/The-OpenROAD-Project/OpenROAD-flow.git
cd OpenROAD-flow/flow
```

## Push-button Run Flow

OpenROAD-flow is based on [make](https://www.gnu.org/software/make/manual/make.html) system. It offers great usability in caching and resuming failed stages from the last successful stage.

The flow logic is defined in `OpenROAD-flow/flow/Makefile`. In the beginning of the file you will notice a few available configuration options:

```shell
# ==============================================================================
# Uncomment or add the design to run
# ==============================================================================

# DESIGN_CONFIG=./designs/nangate45/aes/config.mk
# DESIGN_CONFIG=./designs/nangate45/black_parrot/config.mk
# DESIGN_CONFIG=./designs/nangate45/bp_be_top/config.mk
# DESIGN_CONFIG=./designs/nangate45/bp_fe_top/config.mk
# DESIGN_CONFIG=./designs/nangate45/bp_multi_top/config.mk
# DESIGN_CONFIG=./designs/nangate45/dynamic_node/config.mk
# DESIGN_CONFIG=./designs/nangate45/gcd/config.mk
# DESIGN_CONFIG=./designs/nangate45/ibex/config.mk
# DESIGN_CONFIG=./designs/nangate45/jpeg/config.mk
# DESIGN_CONFIG=./designs/nangate45/swerv/config.mk
# DESIGN_CONFIG=./designs/nangate45/swerv_wrapper/config.mk
# DESIGN_CONFIG=./designs/nangate45/tiny-tests/config.mk
# DESIGN_CONFIG=./designs/nangate45/tinyRocket/config.mk

:
:
:
```

It basically sources flow configuration for a selected (uncommented) design. Have a look at config file of `./designs/nangate45/aes/config.mk` and try to get an idea of what the parameters are.

Now, uncomment this line: `DESIGN_CONFIG=./designs/nangate45/aes/config.mk` and save the file. Then, in the terminal, run `make`. This will start the autonomous flow and run all the steps from pre-processing through logic synthesis and physical design up to finishing.

## Exercises

> 1. From the `config.mk` file, what is the top-level module name?
> 2. From the `Makefile`, can you locate where the script used for synthesis is?
> 3. Where are the source files for the design located?
> 4. What is the current clock period for the design? Can you change it?
> 5. What is the final design area after the flow completes?

## Conclusion

In this part, we have run OpenROAD autonomous flow with a single command. 
We have also looked into how the flow runs and some of the tools used to complete all stages.

In the next section, we will look at the generated reports from the flow.

[:arrow_backward: &nbsp; Previous: Database access, features and tools](../2_database_access) &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;        [Next: Generating Reports &nbsp; :arrow_forward:](../4_generating_reports)