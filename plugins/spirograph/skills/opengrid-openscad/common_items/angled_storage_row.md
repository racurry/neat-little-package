# Angled Storage Row

Multiple round items tilted at an angle for better visibility. Based on QuackWorks MultiConnectRoundRow pattern.

**Use cases**: Screwdriver racks, pen/marker organizers, drill bit storage, spray bottles - any round items where you want to see what's stored and grab easily.

```openscad
module angled_storage_row(
    itemDiameter = 25,        // Diameter of items
    itemsWide = 3,            // Number of items horizontally
    itemsDeep = 2,            // Number of rows front-to-back
    holeDepth = 15,           // How deep items sit in holder
    itemAngle = 30,           // Tilt angle (0-45°)
    shelfStepdown = 5,        // Vertical spacing between rows
    distanceBetweenEach = 2,  // Spacing between items
    baseThickness = 2,        // Floor thickness
    chamferTop = true,        // Ease insertion
    holeChamfer = 0.7         // Chamfer depth
) {
    // Calculate total dimensions
    totalWidth = itemsWide * (itemDiameter + distanceBetweenEach) - distanceBetweenEach;

    // Tilt angle math: front-to-back depth increases with angle
    angleRadians = itemAngle * PI / 180;
    rowDepth = itemDiameter + distanceBetweenEach;

    difference() {
        union() {
            // Create grid of holders
            for (row = [0:itemsDeep-1]) {
                for (col = [0:itemsWide-1]) {
                    // Calculate position with stepdown
                    xPos = col * (itemDiameter + distanceBetweenEach);
                    yPos = row * rowDepth;
                    zPos = -row * shelfStepdown;  // Step down each row

                    translate([xPos, yPos, zPos]) {
                        // Base under each item
                        translate([0, 0, -baseThickness])
                            cylinder(
                                h = baseThickness,
                                d = itemDiameter + distanceBetweenEach,
                                $fn = 40
                            );

                        // Angled rim
                        rotate([itemAngle, 0, 0]) {
                            difference() {
                                // Outer rim
                                cylinder(
                                    h = holeDepth,
                                    d = itemDiameter + 4,  // 2mm wall
                                    $fn = 60
                                );

                                // Inner hole
                                translate([0, 0, chamferTop ? holeChamfer : -1])
                                    cylinder(
                                        h = holeDepth + 2,
                                        d = itemDiameter,
                                        $fn = 60
                                    );

                                // Top chamfer
                                if (chamferTop) {
                                    cylinder(
                                        h = holeChamfer,
                                        d1 = itemDiameter + holeChamfer*2,
                                        d2 = itemDiameter,
                                        $fn = 60
                                    );
                                }
                            }
                        }
                    }
                }
            }

            // Connect with base plate
            translate([0, 0, -(itemsDeep-1) * shelfStepdown - baseThickness])
                cube([
                    totalWidth,
                    itemsDeep * rowDepth,
                    baseThickness
                ]);
        }
    }
}
```

**Angle recommendations**:

- 0°: Vertical storage (like vertical_holder.md)
- 15-20°: Slight tilt for visibility (pens, markers)
- 30-35°: Good visibility and access (screwdrivers, bottles)
- 45°+: Maximum visibility but may need front wall (see `forceFlatFront` in QuackWorks)

**Typical configurations**:

- Pen/marker rack: 3 wide × 2 deep, 15mm diameter, 30° angle, 5mm stepdown
- Screwdriver organizer: 5 wide × 2 deep, 25mm diameter, 35° angle, 10mm stepdown
- Drill bit holder: 6 wide × 3 deep, 12mm diameter, 30° angle, 8mm stepdown

**QuackWorks reference**:

Based on `MultiConnectRoundRow.scad`.

Fetch current code from: https://github.com/AndyLevesque/QuackWorks/tree/main/VerticalMountingSeries

**Advanced QuackWorks features**:

```openscad
// Force flat front (avoid overhangs at high angles)
forceFlatFront = false;       // Set true if angle > 45°

// Additional backer height for heavy items
additionalBackerHeight = 0;   // Extra support height (mm)

// Tolerance tuning
slotTolerance = 1.00;
dimpleScale = 1.0;

// On-ramp for easier mounting
onRampEnabled = true;
onRampHalfOffset = true;      // Stagger for better grip
```

**Design notes**:

- Shelf stepdown creates "stadium seating" effect - see items in back rows
- Keep angle reasonable (30-40°) to avoid needing supports during print
- For items that roll (pens), use higher rim walls
- For heavy items (spray bottles), use more rows deep for stability
