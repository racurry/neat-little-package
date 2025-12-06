# Angled Storage

Tilts forward for better visibility and access.

```openscad
module angled_holder(angle=15) {
    intersection() {
        basic_bin();
        
        // Angled cutting plane
        translate([0, 0, 10])
            rotate([angle, 0, 0])
                cube([
                    internal_width + wall_thickness*2,
                    internal_depth * 2,
                    internal_height * 2
                ]);
    }
}
```

**Good for**:

- Spray cans (tilt forward for easy grabbing)
- Bottles (better visibility of labels)
- Small boxes (easier to see contents)

**Typical angle**: 10-20 degrees
