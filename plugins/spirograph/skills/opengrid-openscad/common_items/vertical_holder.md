# Vertical Holder

Stores items upright in cylindrical holes (pens, markers, drill bits, etc.).

```openscad
module vertical_holder(
    item_diameter=12,      // Diameter of items to hold
    item_depth=70,         // How deep items sit
    holder_count=4,        // Number of positions
    holder_spacing=25      // Distance between centers
) {
    difference() {
        // Solid block
        union() {
            // Base
            translate([-wall_thickness, 0, -base_thickness])
                cube([
                    holder_count * holder_spacing,
                    item_depth + wall_thickness,
                    base_thickness
                ]);
            
            // Walls around entire holder
            difference() {
                cube([
                    holder_count * holder_spacing,
                    item_depth + wall_thickness,
                    item_depth + 10  // Height above items
                ]);
                translate([wall_thickness, wall_thickness, 0])
                    cube([
                        holder_count * holder_spacing - wall_thickness*2,
                        item_depth - wall_thickness,
                        item_depth + 20
                    ]);
            }
        }
        
        // Cylindrical holes for items
        for (i = [0:holder_count-1]) {
            translate([
                holder_spacing/2 + i * holder_spacing,
                item_depth/2 + wall_thickness,
                0
            ])
                cylinder(
                    h = item_depth + 5,
                    d = item_diameter + 1,  // 0.5mm clearance per side
                    $fn = 40
                );
        }
    }
}
```

**Typical dimensions for**:

- Sharpies/markers: diameter=15mm, depth=70mm
- Pens: diameter=12mm, depth=70mm
- Drill bits: diameter=10mm, depth=60mm
- Hex keys: diameter=8mm, depth=50mm

**Customization**:

```openscad
// Different sized holes
for (i = [0:3]) {
    translate([25*i, 40, 0])
        cylinder(h=70, d=[10,12,15,18][i], $fn=40);
}
```

______________________________________________________________________
