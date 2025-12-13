# Advanced Bin

Enhanced bin with angled front, chamfered edges, and BOSL2 geometry. Based on QuackWorks MulticonnectBin pattern.

**Use cases**: Upgrade from basic_bin.md when you need better accessibility (angled front), cleaner geometry (BOSL2), or more professional finish.

```openscad
include <BOSL2/std.scad>

module advanced_bin(
    internalWidth = 60,       // Interior width
    internalDepth = 40,       // Interior depth
    internalHeight = 50,      // Interior height
    wallThickness = 2,        // Wall thickness
    baseThickness = 3,        // Floor thickness
    angleCut = 15,            // Front face angle (degrees)
    frontChamfer = 5          // Rounded bottom front edge
) {
    // Use BOSL2 rect_tube for cleaner geometry
    difference() {
        union() {
            // Main bin body using BOSL2
            back(0.01)
                rect_tube(
                    size = [internalWidth + wallThickness*2, internalDepth + wallThickness],
                    h = internalHeight + baseThickness,
                    wall = wallThickness,
                    chamfer = [frontChamfer, 0, 0, 0],  // Front bottom chamfer
                    ichamfer = [2, 0, 0, 0]             // Interior chamfer
                );
        }

        // Angled front cut for accessibility
        if (angleCut > 0) {
            angleRadians = angleCut * PI / 180;
            cutDepth = internalHeight / tan(angleRadians);

            translate([
                -(internalWidth + wallThickness*2)/2 - 10,
                internalDepth/2,
                internalHeight
            ])
                rotate([angleCut, 0, 0])
                    cube([
                        internalWidth + wallThickness*2 + 20,
                        cutDepth + 50,
                        internalHeight
                    ]);
        }
    }
}
```

**Why advanced_bin vs basic_bin?**

| Feature         | basic_bin.md           | advanced_bin.md    |
| --------------- | ---------------------- | ------------------ |
| Geometry        | Manual cube operations | BOSL2 rect_tube()  |
| Front angle     | None                   | Customizable 0-30° |
| Edge finish     | Sharp                  | Chamfered bottom   |
| Code complexity | Simple                 | Requires BOSL2     |
| Use case        | Quick bins             | Production quality |

**Angle recommendations**:

- 0°: No angle, maximum capacity (same as basic_bin)
- 10-15°: Slight tilt, easier to see/grab contents
- 20-25°: Good visibility, may reduce capacity
- 30°+: Maximum accessibility, consider supports

**QuackWorks reference**:

Based on `MulticonnectBin.scad`.

Fetch current code from: https://github.com/AndyLevesque/QuackWorks/tree/main/VerticalMountingSeries

**BOSL2 rect_tube() explained**:

```openscad
rect_tube(
    size = [width, depth],        // External dimensions
    h = height,                   // Total height
    wall = 2,                     // Wall thickness (uniform)
    chamfer = [5, 0, 0, 0],      // Bottom: front, back, left, right
    ichamfer = [2, 0, 0, 0]      // Interior chamfers (same order)
)
```

**Benefits of BOSL2 approach**:

- Cleaner code (one call vs multiple cube operations)
- Automatic chamfer generation (no manual hull operations)
- Consistent wall thickness (calculated internally)
- Better performance (optimized geometry)

**Typical dimensions**:

- Small parts: 60×40×50mm, angle=15°, chamfer=5mm
- Medium storage: 80×60×60mm, angle=10°, chamfer=5mm
- Large bins: 120×80×80mm, angle=0°, chamfer=8mm

**Customization examples**:

```openscad
// Deep bin with steep front (tools)
advanced_bin(
    internalWidth = 100,
    internalDepth = 60,
    internalHeight = 80,
    angleCut = 25,
    frontChamfer = 8
);

// Shallow tray with subtle angle (hardware)
advanced_bin(
    internalWidth = 80,
    internalDepth = 60,
    internalHeight = 30,
    angleCut = 10,
    frontChamfer = 3
);
```

**Integration with enhancements**:

All enhancements from `enhancements.md` work with advanced_bin:

```openscad
difference() {
    advanced_bin();

    // Add label recess
    translate([...])
        label_recess(width=40, height=10);

    // Add drainage
    for (x = [...]) {
        cylinder(h=baseThickness+2, d=5);
    }
}
```
