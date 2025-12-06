# Curved Hook

Cantilever hook with curved arc for hanging items. Based on QuackWorks MultiConnectRoundHook pattern.

**Use cases**: Hanging headphones, cables, bags, lightweight tools - anything that benefits from a smooth curved surface rather than a straight hook.

```openscad
module curved_hook(
    hookDiameter = 75,        // Curve diameter (0-200mm)
    angle = 180,              // Hook curve angle (0-180°)
    hookWidth = 10,           // Width of hook material
    hookInternalDepth = 25,   // How far hook extends from wall
    hookBottomThickness = 5,  // Thickness of hook material
    backHeight = 40,          // Height of mounting back
    enableMinkowski = true,   // Rounded edges via BOSL2
    r = 2.3                   // Bevel radius if minkowski enabled
) {
    // Calculate hook geometry
    hookRadius = hookDiameter / 2;
    hookAngle = -angle + 180;

    module roundHook(useMinkowski) {
        adjust = useMinkowski ? r : 0;

        translate([hookWidth/2 - adjust, hookInternalDepth + hookBottomThickness, hookRadius])
            rotate([0, -90, 0])
                linear_extrude(hookWidth - 2*adjust) {
                    difference() {
                        // Outer arc
                        circle(hookRadius - adjust, $fn=66);

                        // Inner arc (creates wall thickness)
                        circle(hookRadius - hookBottomThickness + adjust, $fn=66);

                        // Cut to create hook shape
                        rotate([0, 0, hookAngle - 90])
                            translate([0, -hookRadius*2, hookRadius/2])
                                square([hookRadius*2, hookRadius*2]);

                        // Additional cuts for hook opening
                        translate([0, -hookRadius*2, hookRadius/2])
                            rotate([0, 0, -hookAngle - 180])
                                square([hookRadius*2, hookRadius*1.1]);

                        // Cut bottom flat
                        rotate([0, 0, 0])
                            translate([-hookRadius*2, -hookRadius*2, hookRadius/2])
                                square([hookRadius*2, hookRadius*2]);

                        // Final opening cut
                        rotate([0, 0, hookAngle])
                            translate([0, -hookRadius*2, hookRadius/2])
                                square([hookRadius*2, hookRadius*2]);
                    }
                }
    }

    if (enableMinkowski) {
        minkowski() {
            roundHook(true);
            sphere(r, $fn=32);
        }
    } else {
        roundHook(false);
    }
}
```

**Angle guide**:

- 90°: Quarter circle, gentle J-hook
- 120°: More secure, good for cables
- 180°: Half circle, maximum hold (headphones, bags)

**Diameter recommendations**:

- Small items (cables, keys): 40-50mm diameter
- Medium items (headphones): 60-80mm diameter
- Large items (bags, coats): 100-150mm diameter

**QuackWorks reference**:

Based on `MultiConnectRoundHook.scad` (remixed by Moritz Weller).

Fetch current code from: https://github.com/AndyLevesque/QuackWorks/tree/main/VerticalMountingSeries

**BOSL2 integration**:

This pattern uses BOSL2's minkowski sphere for rounded edges:

```openscad
include <BOSL2/std.scad>

// Enable rounded edges (more filament, nicer look)
enableMinkowski = true;
r = 2.3;  // Bevel radius

// Disable for faster print, sharper edges
enableMinkowski = false;
```

**Design notes**:

- Minkowski adds ~10-20% print time but creates smooth, snag-free edges
- For heavy items, increase `hookBottomThickness` to 7-10mm
- Internal depth controls how far hook projects from wall
- Higher angles (>135°) provide more security but harder to remove items
- Test fit with lighter items before scaling up for production

**Typical configurations**:

- Headphone hook: 75mm diameter, 180° angle, 25mm depth
- Cable management: 50mm diameter, 120° angle, 20mm depth
- Bag hook: 120mm diameter, 150° angle, 40mm depth
