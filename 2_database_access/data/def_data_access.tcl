set db [odb::dbDatabase_create]
set lib [odb::read_lef $db "data/NangateOpenCellLibrary.mod.lef"]
set tech [$lib getTech]
set chip [odb::read_def $db "data/gcd_floorplan.def"]

# Block checks
set block [$chip getBlock]
puts "block name: [$block getName]"
set units [$block getDefUnits]
puts "def units: $units"
puts "number of children: [llength [set children [$block getChildren]]]"
puts "number of instances: [llength [set insts [$block getInsts]]]"
puts "number of pins: [llength [set bterms [$block getBTerms]]]"
puts "number of obstructions: [llength [set obstructions [$block getObstructions]]]"
puts "number of blockages: [llength [set blockages [$block getBlockages]]]"
puts "number of nets: [llength [set nets [$block getNets]]]"
puts "number of vias: [llength [set vias [$block getVias]]]"
puts "number of rows: [llength [set rows [$block getRows]]]"

set bbox [$block getBBox]
puts "bbox: [list [$bbox xMin] [$bbox yMin] [$bbox xMax] [$bbox yMax]]"
puts "block gcell grid: [$block getGCellGrid]"

set die_area_rect [$block getDieArea]
puts "block die area: [list [$die_area_rect xMin] [$die_area_rect yMin] [$die_area_rect xMax] [$die_area_rect yMax]]"
puts "number of regions: [llength [set regions [$block getRegions]]]"
puts "number of nondefault rules: [llength [set non_default_rules [$block getNonDefaultRules]]]"

# Row checks
set row [lindex $rows 0] 
puts "row name: [$row getName]"
puts "row site: [$row getSite] getName]"
puts "row origin: [$row getOrigin]"
puts "row orientation: [$row getOrient]"
puts "row direction: [$row getDirection]"
puts "row site count: [$row getSiteCount]"
puts "row site spacing: [$row getSpacing]"
puts "row bbox: [list [[$row getBBox] xMin] [[$row getBBox] yMin] [[$row getBBox] xMax] [[$row getBBox] yMax]]"

# Instance checks
set inst [lindex $insts 0]
puts "instance name: [$inst getName]"
puts "orientation: [$inst getOrient]"
puts "origin: [list [[$inst getBBox] xMin] [[$inst getBBox] yMin]]"
puts "placement status: [$inst getPlacementStatus]"
puts "master cell: [[set master [$inst getMaster]] getName]"
puts "number of inst pins: [llength [set iterms [$inst getITerms]]]"
puts "instance halo: [$inst getHalo]"

# Cell master checks
puts "master name: [$master getName]"
puts "master origin: [$master getOrigin]"
puts "master width: [$master getWidth]"
puts "master height: [$master getHeight]"
puts "master type: [$master getType]"
puts "master logically equiv: [$master getLEQ]"
puts "master electrially equiv: [$master getEEQ]"
puts "master symmetry: [list [$master getSymmetryX] [$master getSymmetryY] [$master getSymmetryR90]]"
puts "master number of terms: [llength [$master getMTerms]]"
puts "master library: [[$master getLib] getName]"
puts "master num obstructions: [llength [$master getObstructions]]"
set rect [$master getPlacementBoundary]
puts "master placement boundary: [list [$rect xMin] [$rect yMin] [$rect xMax] [$rect yMax]]"
puts "master term count: [$master getMTermCount]"
puts "master site: [[$master getSite] getName]"

# Net checks
set net [lindex $nets 0]
puts "net name: [$net getName]"
puts "net weight: [$net getWeight]"
puts "net term count: [$net getTermCount]"
puts "net iterm count: [$net getITermCount]"
puts "net bterm count: [$net getBTermCount]"
puts "net sigType: [$net getSigType]"
puts "net wires: [$net getWire]"
puts "net swires: [$net getSWires]"
puts "net global wire: [$net getGlobalWire]"
puts "net non default rule: [$net getNonDefaultRule]"

exit