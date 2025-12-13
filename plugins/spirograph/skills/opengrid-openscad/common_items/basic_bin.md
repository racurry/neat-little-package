# Basic Bin

Standard open-top bin with four walls and floor. Most versatile pattern. Good for small parts, screws, hardware.

```openscad
module basic_bin() {
    union() {
        // Bottom floor
        translate([-wall_thickness, 0, -base_thickness])
            cube([
                internal_width + wall_thickness*2,
                internal_depth + wall_thickness,
                base_thickness
            ]);

        // Left wall
        translate([-wall_thickness, 0, 0])
            cube([
                wall_thickness,
                internal_depth + wall_thickness,
                internal_height
            ]);

        // Right wall
        translate([internal_width, 0, 0])
            cube([
                wall_thickness,
                internal_depth + wall_thickness,
                internal_height
            ]);

        // Front capture lip
        translate([0, internal_depth, 0])
            cube([
                internal_width,
                wall_thickness,
                internal_height
            ]);
    }
}
```

**Typical dimensions**:

- Small parts: 50×40×50mm (internal)
- Medium storage: 80×60×60mm
- Large bins: 120×80×80mm

**Customization ideas**:

- Add label recess on front
- Add drainage holes in bottom
- Round the corners for easier cleaning
