# Shelf Bracket

Creates a shelf support with triangular brace.

```openscad
module shelf_bracket(
    shelf_width=100,
    shelf_depth=150,
    shelf_height=80
) {
    union() {
        // Vertical back support
        cube([shelf_width, wall_thickness*2, shelf_height]);
        
        // Triangular support brace
        translate([0, 0, shelf_height - shelf_depth])
            linear_extrude(height = shelf_width)
                polygon([
                    [0, 0],
                    [shelf_depth, 0],
                    [0, shelf_depth]
                ]);
        
        // Shelf rest (top surface)
        translate([0, 0, shelf_height])
            cube([shelf_width, shelf_depth, wall_thickness*2]);
        
        // Front lip (prevents items sliding off)
        translate([0, shelf_depth - wall_thickness, shelf_height])
            cube([shelf_width, wall_thickness, 10]);
    }
}
```

**Typical dimensions**:

- Light duty: width=100mm, depth=120mm
- Medium duty: width=150mm, depth=150mm
- Heavy duty: Use 4+ MultiConnect slots, increase wall_thickness to 3mm

**Load capacity**:

- Depends on MultiConnect connector count
- 2 slots: ~5kg
- 3 slots: ~8kg
- 4+ slots: ~12kg (test with your setup)

______________________________________________________________________
