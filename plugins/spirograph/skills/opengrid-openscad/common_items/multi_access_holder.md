# Multi-Access Holder

Box with customizable cutouts on any side for multi-directional access. Based on QuackWorks VerticalItemHolder pattern.

**Use cases**: Items needing cable routing (chargers, adapters), items accessed from sides (remote controls, phones), items needing drainage, or custom access patterns.

```openscad
include <BOSL2/std.scad>

module multi_access_holder(
    internalWidth = 60,        // Interior width
    internalDepth = 15,        // Interior depth
    internalHeight = 50,       // Interior height
    wallThickness = 2,         // Wall thickness
    baseThickness = 3,         // Floor thickness
    edgeRounding = 0.5,        // Edge rounding radius
    // Front cutout
    frontCutout = true,
    frontLowerCapture = 10,    // How much front wall at bottom
    frontUpperCapture = 5,     // How much front wall at top
    frontLateralCapture = 3,   // How much front wall on sides
    // Bottom cutout (drainage/access)
    bottomCutout = false,
    bottomFrontCapture = 3,
    bottomBackCapture = 3,
    bottomSideCapture = 3,
    // Cord cutout (cable routing)
    cordCutout = false,
    cordCutoutDiameter = 10,
    cordCutoutLateralOffset = 0,
    cordCutoutDepthOffset = 0,
    // Side cutouts
    rightCutout = false,
    rightLowerCapture = 7,
    rightUpperCapture = 0,
    rightLateralCapture = 3,
    leftCutout = false,
    leftLowerCapture = 7,
    leftUpperCapture = 0,
    leftLateralCapture = 3
) {
    difference() {
        // Main body with rounded edges
        translate([0, 0, -baseThickness])
            offset3d(edgeRounding)
                cube([
                    internalWidth + wallThickness*2,
                    internalDepth + wallThickness,
                    internalHeight + baseThickness
                ]);

        // Interior cavity
        translate([wallThickness, wallThickness, 0])
            cube([internalWidth, internalDepth - wallThickness, internalHeight + 1]);

        // Front cutout
        if (frontCutout) {
            translate([
                wallThickness + frontLateralCapture,
                internalDepth + wallThickness - 1,
                frontLowerCapture
            ])
                cube([
                    internalWidth - frontLateralCapture*2,
                    wallThickness + 2,
                    internalHeight - frontLowerCapture - frontUpperCapture
                ]);
        }

        // Bottom cutout
        if (bottomCutout) {
            translate([
                wallThickness + bottomSideCapture,
                wallThickness + bottomFrontCapture,
                -baseThickness - 1
            ])
                cube([
                    internalWidth - bottomSideCapture*2,
                    internalDepth - wallThickness - bottomFrontCapture - bottomBackCapture,
                    baseThickness + 2
                ]);
        }

        // Cord cutout (slot from bottom through front)
        if (cordCutout) {
            translate([
                wallThickness + internalWidth/2 + cordCutoutLateralOffset,
                wallThickness + internalDepth/2 + cordCutoutDepthOffset,
                -baseThickness - 1
            ]) {
                // Vertical hole through bottom
                cylinder(h = baseThickness + 2, d = cordCutoutDiameter, $fn=30);

                // Horizontal slot through front
                translate([0, 0, baseThickness])
                    rotate([90, 0, 0])
                        cylinder(
                            h = internalDepth,
                            d = cordCutoutDiameter,
                            $fn = 30
                        );
            }
        }

        // Right side cutout
        if (rightCutout) {
            translate([
                internalWidth + wallThickness - 1,
                wallThickness + rightLateralCapture,
                rightLowerCapture
            ])
                cube([
                    wallThickness + 2,
                    internalDepth - wallThickness - rightLateralCapture*2,
                    internalHeight - rightLowerCapture - rightUpperCapture
                ]);
        }

        // Left side cutout
        if (leftCutout) {
            translate([
                -1,
                wallThickness + leftLateralCapture,
                leftLowerCapture
            ])
                cube([
                    wallThickness + 2,
                    internalDepth - wallThickness - leftLateralCapture*2,
                    internalHeight - leftLowerCapture - leftUpperCapture
                ]);
        }
    }
}
```

**Common configurations**:

```openscad
// Phone charger holder (front open, cord slot)
multi_access_holder(
    internalWidth = 80,
    internalDepth = 20,
    internalHeight = 60,
    frontCutout = true,
    frontLowerCapture = 15,   // Capture bottom to hold phone
    frontUpperCapture = 0,    // Open top for easy access
    cordCutout = true,
    cordCutoutDiameter = 10
);

// Remote control holder (front and top open)
multi_access_holder(
    internalWidth = 60,
    internalDepth = 15,
    internalHeight = 50,
    frontCutout = true,
    frontLowerCapture = 10,
    frontUpperCapture = 0,    // Full access from top
    edgeRounding = 1.0        // Smooth edges
);

// Adapter/cable organizer (drainage, front access)
multi_access_holder(
    internalWidth = 100,
    internalDepth = 30,
    internalHeight = 40,
    frontCutout = true,
    frontLowerCapture = 8,
    bottomCutout = true,      // Drainage holes
    bottomSideCapture = 5
);

// Multi-tool caddy (access from all sides)
multi_access_holder(
    internalWidth = 80,
    internalDepth = 25,
    internalHeight = 60,
    frontCutout = true,
    frontLowerCapture = 10,
    leftCutout = true,
    leftLowerCapture = 10,
    rightCutout = true,
    rightLowerCapture = 10
);
```

**QuackWorks reference**:

Based on `VerticalItemHolder.scad`.

Fetch current code from: https://github.com/AndyLevesque/QuackWorks/tree/main/VerticalMountingSeries

**Capture parameter logic**:

- **Lower capture**: Wall height from bottom (holds item in place)
- **Upper capture**: Wall height from top (prevents tipping, 0=open top)
- **Lateral capture**: Wall width on sides (prevents sliding out)

**Example: Phone holder**

```
         ┌─────────┐  ← frontUpperCapture = 0 (open top)
         │         │
         │ PHONE   │
         │         │
    ────►│         │◄──── frontLateralCapture = 3mm (side walls)
         │         │
         └─────────┘  ← frontLowerCapture = 15mm (holds bottom)
```

**Design notes**:

- Edge rounding (BOSL2 `offset3d()`) prevents snags and looks professional
- Set `upperCapture = 0` for open-top access
- Use `bottomCutout` for items that might drip (spray bottles, wet items)
- Cord cutout combines vertical hole with horizontal slot for cable routing
- For backplate-only mode (remixing), set all dimensions to 0 in QuackWorks version

**BOSL2 offset3d() explained**:

```openscad
offset3d(r = 0.5)  // Rounds all edges by 0.5mm
    cube([100, 50, 60]);
```

Applies radius to all edges, creating smooth transitions. More sophisticated than manual chamfers.
