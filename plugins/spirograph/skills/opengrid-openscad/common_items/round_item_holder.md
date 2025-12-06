# Round Item Holder

Holds round or rectangular items in a recessed rim. Based on QuackWorks MultiConnectRoundSingleHolder pattern.

**Use cases**: Bottles, cans, jars, rectangular electronics, anything that needs a surrounding rim for stability.

```openscad
module round_item_holder(
    itemDiameter = 25,        // For round items
    itemWidth = 0,            // For rectangular (set both width/length)
    itemLength = 0,           // Set to 0 for round items
    itemShape = "Round",      // "Round" or "Rectangular"
    rimHeight = 15,           // Holder rim height
    rimThickness = 2,         // Wall thickness around item
    baseThickness = 3,        // Floor thickness
    cutoutDiameter = 0,       // Optional hole through bottom (0 = none)
    chamferTop = true,        // Ease insertion with top chamfer
    offset = 0                // Distance from back wall to rim
) {
    // Calculate dimensions
    outerDiameter = itemShape == "Round" ?
        itemDiameter + rimThickness*2 :
        max(itemWidth, itemLength) + rimThickness*2;

    difference() {
        union() {
            // Base plate
            translate([-rimThickness, 0, -baseThickness])
                cube([
                    outerDiameter,
                    outerDiameter/2 + offset,
                    baseThickness
                ]);

            // Rim walls
            if (itemShape == "Round") {
                // Round rim
                difference() {
                    cylinder(
                        h = rimHeight,
                        d = itemDiameter + rimThickness*2,
                        $fn = 60
                    );
                    translate([0, 0, chamferTop ? 0 : -1])
                        cylinder(
                            h = rimHeight + (chamferTop ? 0 : 2),
                            d = itemDiameter,
                            $fn = 60
                        );
                }

                // Top chamfer for easier insertion
                if (chamferTop) {
                    translate([0, 0, rimHeight - 1])
                        cylinder(
                            h = 1.5,
                            d1 = itemDiameter,
                            d2 = itemDiameter + 2,
                            $fn = 60
                        );
                }
            } else {
                // Rectangular rim
                difference() {
                    cube([
                        itemWidth + rimThickness*2,
                        itemLength + rimThickness*2,
                        rimHeight
                    ]);
                    translate([rimThickness, rimThickness, chamferTop ? 0 : -1])
                        cube([
                            itemWidth,
                            itemLength,
                            rimHeight + (chamferTop ? 0 : 2)
                        ]);
                }

                // Top chamfer
                if (chamferTop) {
                    translate([rimThickness, rimThickness, rimHeight - 1])
                        hull() {
                            cube([itemWidth, itemLength, 0.1]);
                            translate([-0.5, -0.5, 1])
                                cube([itemWidth + 1, itemLength + 1, 0.1]);
                        }
                }
            }
        }

        // Optional cutout through bottom
        if (cutoutDiameter > 0) {
            translate([0, 0, -baseThickness - 1])
                cylinder(
                    h = baseThickness + 2,
                    d = cutoutDiameter,
                    $fn = 40
                );
        }
    }
}
```

**Typical dimensions**:

- Small bottles (travel size): diameter=30mm, rim=15mm
- Spray cans: diameter=65mm, rim=20mm
- AA battery holder: width=14mm, length=50mm (rectangular)
- Mason jar: diameter=85mm, rim=25mm

**Multi-item row variant**:

For multiple items in a grid, see `angled_storage_row.md` which uses the same rim concept but arrays multiple holders with shelf stepdown.

**QuackWorks reference**:

This pattern is based on:

- `MultiConnectRoundSingleHolder.scad` - Single item holder
- `MultiConnectRoundRow.scad` - Multi-item grid variant

Fetch current code from: https://github.com/AndyLevesque/QuackWorks/tree/main/VerticalMountingSeries

**Key parameters from QuackWorks**:

```openscad
// Tolerance tuning (see SKILL.md Tolerance section)
slotTolerance = 1.00;         // Scale slot width
dimpleScale = 1.0;            // Scale dimple size

// On-ramp system (ease mounting)
onRampEnabled = true;
On_Ramp_Every_X_Slots = 2;    // Every 2nd slot gets guide cone
```
