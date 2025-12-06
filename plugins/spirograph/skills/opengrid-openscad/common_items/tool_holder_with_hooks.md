# Tool Holder with Hooks

Horizontal storage for tools on cantilever hooks.

```openscad
module tool_holder(
    hook_count=3,
    hook_spacing=40,
    hook_length=60,
    hook_height=100
) {
    union() {
        // Back support plate
        cube([
            hook_count * hook_spacing,
            wall_thickness,
            hook_height
        ]);
        
        // Individual hooks
        for (i = [0:hook_count-1]) {
            translate([
                hook_spacing/2 + i * hook_spacing - wall_thickness/2,
                0,
                hook_height - 30
            ]) {
                hook_arm(hook_length);
            }
        }
    }
}

module hook_arm(length) {
    union() {
        // Vertical support
        cube([wall_thickness*2, wall_thickness, 40]);
        
        // Horizontal arm
        translate([0, 0, 40])
            cube([wall_thickness*2, length, wall_thickness*2]);
        
        // Upturned tip (prevents sliding off)
        translate([0, length, 40])
            cube([wall_thickness*2, wall_thickness, 10]);
    }
}
```

**Good for**:

- Screwdrivers, pliers, wrenches
- Hammers, measuring tape
- Paint brushes
- Anything with a handle to hang

**Dimensions**:

- hook_length: 40-80mm depending on tool size
- hook_spacing: 30-50mm between hooks
- hook_height: 80-150mm

---
