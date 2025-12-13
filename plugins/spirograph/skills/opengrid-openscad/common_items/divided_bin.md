# Divided Bin

Bin with internal dividers for organizing multiple item types.

```openscad
module divided_bin(dividers_x=1, dividers_y=0) {
    union() {
        basic_bin();  // Start with basic bin
        
        // Vertical dividers (X direction)
        if (dividers_x > 0) {
            for (i = [1:dividers_x]) {
                translate([
                    (internal_width / (dividers_x + 1)) * i - wall_thickness/2,
                    0,
                    0
                ])
                    cube([
                        wall_thickness,
                        internal_depth,
                        internal_height - 2  // Slightly shorter for easier access
                    ]);
            }
        }
        
        // Horizontal dividers (Y direction)
        if (dividers_y > 0) {
            for (i = [1:dividers_y]) {
                translate([
                    0,
                    (internal_depth / (dividers_y + 1)) * i - wall_thickness/2,
                    0
                ])
                    cube([
                        internal_width,
                        wall_thickness,
                        internal_height - 2
                    ]);
            }
        }
    }
}
```

**Usage**:

```openscad
// 2 vertical sections
divided_bin(dividers_x=1, dividers_y=0);

// 3 vertical × 2 horizontal = 6 compartments
divided_bin(dividers_x=2, dividers_y=1);

// 4 vertical sections
divided_bin(dividers_x=3, dividers_y=0);
```

**Typical dimensions**:

- Wider than tall for multiple vertical divisions
- internal_width: 80-150mm
- Divider spacing: 25-40mm sections work well

______________________________________________________________________
