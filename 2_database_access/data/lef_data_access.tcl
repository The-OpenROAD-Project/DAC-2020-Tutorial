set db [odb::dbDatabase_create]
set lib [odb::read_lef $db "data/gscl45nm.lef"]
set tech [$lib getTech]

# Basic LEF checks"
puts "LEF version: [$tech getLefVersion]"
puts "LEF version string: [$tech getLefVersionStr]"

puts "manufacturing grid size: [$tech getManufacturingGrid]"
puts "case sensitive: [$tech getNamesCaseSensitive]"
puts "num routing layers: [$tech getRoutingLayerCount]"
puts "num vias: [$tech getViaCount]"
puts "num layers: [$tech getLayerCount]"
puts "units: [set units [$tech getLefUnits]]"

# Via rules checks
set via_rules [$tech getViaGenerateRules]

puts "Number of via rules: [llength $via_rules]"

set via_rule [lindex $via_rules 0]
puts "via rule name: [$via_rule getName]"
puts "via_rule default: [$via_rule isDefault]"

puts "via_rule layer count: [$via_rule getViaLayerRuleCount]"

set viaLayerRule [$via_rule getViaLayerRule 0]

set lower_rule [$via_rule getViaLayerRule 0]
set upper_rule [$via_rule getViaLayerRule 1]
set cut_rule   [$via_rule getViaLayerRule 2]

# Check layer names
set lower_layer [$lower_rule getLayer]
set upper_layer [$upper_rule getLayer]
set cut_layer   [$cut_rule getLayer]

puts "via M2_M1 lower: [$lower_layer getName]"
puts "via M2_M1 upper: [$upper_layer getName]"
puts "via M2_M1 cut: [$cut_layer getName]"

# Check via rule details
puts "lower has enclosure: [$lower_rule hasEnclosure]"
puts "lower has rect:      [$lower_rule hasRect]"
puts "lower has spacing:   [$lower_rule hasSpacing]"
puts "upper has enclosure: [$upper_rule hasEnclosure]"
puts "upper has rect:      [$upper_rule hasRect]"
puts "upper has spacing:   [$upper_rule hasSpacing]"
puts "cut has enclosure:   [$cut_rule hasEnclosure]"
puts "cut has rect:        [$cut_rule hasRect]"
puts "cut has spacing:     [$cut_rule hasSpacing]"

puts "lower enclosure: [$lower_rule getEnclosure]"
puts "upper enclosure: [$upper_rule getEnclosure]"

set cut_rect [$cut_rule getRect]
puts "cut rect:       [list [$cut_rect xMin] [$cut_rect yMin] [$cut_rect xMax] [$cut_rect yMax]]"
puts "cut spacing:     [$cut_rule getSpacing]"

set layers [$tech getLayers]
puts "returned layers: [llength $layers]"

set layer [lindex $layers 2]
puts "layer name: [$layer getName]"
puts "layer below: [[$layer getLowerLayer] getName]"
puts "layer above: [[$layer getUpperLayer] getName]"

puts "layer hasAlias:              [$layer hasAlias]"
puts "layer hasArea:               [$layer hasArea]"
puts "layer hasDefaultAntennaRule: [$layer hasDefaultAntennaRule]"
puts "layer hasMaxWidth:           [$layer hasMaxWidth]"
puts "layer hasMinStep:            [$layer hasMinStep]"
puts "layer hasOxide2AntennaRule:  [$layer hasOxide2AntennaRule]"
puts "layer hasProtrusion:         [$layer hasProtrusion]"
puts "layer hasV55SpacingRules:    [$layer hasV55SpacingRules]"

puts "layer type: [$layer getType]"
puts "layer direction: [$layer getDirection]"
puts "layer pitch: [$layer getPitch]"
puts "layer width: [$layer getWidth]"
puts "layer spacing: [$layer getSpacing]"
puts "layer resistance: [$layer getResistance]"
puts "layer capacitance: [$layer getCapacitance]"

exit