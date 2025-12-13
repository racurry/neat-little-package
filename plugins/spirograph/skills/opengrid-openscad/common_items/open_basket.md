# Open Basket (No Front)

Bin without front wall for easy access from top and front.

```openscad
module open_basket() {
    union() {
        // Bottom
        translate([-wall_thickness, 0, -base_thickness])
            cube([
                internal_width + wall_thickness*2,
                internal_depth,
                base_thickness
            ]);

        // Left wall
        translate([-wall_thickness, 0, 0])
            cube([
                wall_thickness,
                internal_depth,
                internal_height
            ]);

        // Right wall
        translate([internal_width, 0, 0])
            cube([
                wall_thickness,
                internal_depth,
                internal_height
            ]);

        // No front wall - open access
    }
}
```

**Good for**:

- Cables, zip ties (reach in from front)
- Frequently accessed items
- Items that lean against back (notebooks, clipboards)

______________________________________________________________________
