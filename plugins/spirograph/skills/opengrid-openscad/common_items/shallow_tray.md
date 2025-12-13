# Shallow Tray

Low-profile bin for small, flat items. Same as basic bin but shorter.

```openscad
module shallow_tray() {
    shallow_height = 20;  // Low walls for easy access
    
    union() {
        // Bottom
        translate([-wall_thickness, 0, -base_thickness])
            cube([
                internal_width + wall_thickness*2,
                internal_depth + wall_thickness,
                base_thickness
            ]);

        // Outer walls (short)
        difference() {
            cube([
                internal_width + wall_thickness*2,
                internal_depth + wall_thickness,
                shallow_height
            ]);
            translate([wall_thickness, wall_thickness, 0])
                cube([
                    internal_width,
                    internal_depth - wall_thickness,
                    shallow_height + 1
                ]);
        }
    }
}
```

**Typical dimensions**:

- internal_height: 15-25mm
- internal_depth: 40-60mm
- internal_width: 60-100mm

**Good for**:

- Paper clips, rubber bands
- SD cards, USB drives
- Small electronic components
- Jewelry, rings
