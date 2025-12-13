# Hook Array

Multiple simple hooks in a row.

```openscad
module hook_array(
    hook_count=5,
    hook_spacing=30
) {
    union() {
        // Back plate
        cube([
            hook_count * hook_spacing,
            wall_thickness,
            60
        ]);
        
        // Simple J-hooks
        for (i = [0:hook_count-1]) {
            translate([
                hook_spacing/2 + i * hook_spacing,
                0,
                40
            ]) {
                simple_j_hook();
            }
        }
    }
}

module simple_j_hook() {
    rotate([90, 0, 0])
        difference() {
            cylinder(h=40, d=10, $fn=30);
            translate([0, 0, -1])
                cylinder(h=42, d=6, $fn=30);
        }
}
```

**Good for**:

- Keys
- Small bags
- Headphones
- Cables
- Anything with a loop or handle

______________________________________________________________________
