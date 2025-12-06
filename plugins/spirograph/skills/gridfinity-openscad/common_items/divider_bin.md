# Gridfinity Divider Bin

Bin with internal dividers for organizing multiple types of items in compartments. Built on basic bin foundation.

## When to Use

- Sorting small parts (resistors by value, screws by size)
- Mixed item categories in one bin
- Desktop organization with sections
- Electronics components storage

## Module Code

```openscad
// Gridfinity Divider Bin Module
// Extends basic bin with internal compartments

// Base bin parameters
grid_x = 3;              // Grid units wide
grid_y = 2;              // Grid units deep
height_u = 4;            // Height units

// Divider configuration
dividers_x = 2;          // Number of X-axis dividers (creates dividers_x+1 compartments)
dividers_y = 1;          // Number of Y-axis dividers
divider_thickness = 1.2; // Divider wall thickness (1.0-1.6mm)

// Gridfinity constants
grid_size = 42;
bin_size = 41.5;
height_unit = 7;
corner_radius = 3.75;
stacking_lip_height = 4.4;

// Structural parameters
wall_thickness = 2.0;
base_thickness = 2.0;

// Optional features
include_stacking_lip = true;
include_magnets = false;
magnet_diameter = 6;
magnet_depth = 2;

// Calculated dimensions
bin_width = bin_size * grid_x;
bin_depth = bin_size * grid_y;
bin_height = height_unit * height_u;
base_height = 5;

// Interior dimensions
interior_width = bin_width - wall_thickness*2;
interior_depth = bin_depth - wall_thickness*2;
interior_height = bin_height - base_height - base_thickness;

module gridfinity_base_profile() {
    // Same as basic_bin.md - base profile for socket engagement
    difference() {
        union() {
            for (x = [0:grid_x-1]) {
                for (y = [0:grid_y-1]) {
                    translate([x * grid_size, y * grid_size, 0])
                        rounded_square_base(bin_size, bin_size, corner_radius, base_height);
                }
            }
        }

        translate([wall_thickness, wall_thickness, -0.1])
            for (x = [0:grid_x-1]) {
                for (y = [0:grid_y-1]) {
                    translate([x * grid_size, y * grid_size, 0])
                        rounded_square_base(36.5, 36.5, corner_radius - wall_thickness, base_height + 0.2);
                }
            }

        if (include_magnets) {
            for (x = [0:grid_x-1]) {
                for (y = [0:grid_y-1]) {
                    translate([x * grid_size, y * grid_size, 0]) {
                        translate([8, 8, -0.1])
                            cylinder(d=magnet_diameter, h=magnet_depth+0.1, $fn=30);
                        translate([bin_size-8, 8, -0.1])
                            cylinder(d=magnet_diameter, h=magnet_depth+0.1, $fn=30);
                        translate([8, bin_size-8, -0.1])
                            cylinder(d=magnet_diameter, h=magnet_depth+0.1, $fn=30);
                        translate([bin_size-8, bin_size-8, -0.1])
                            cylinder(d=magnet_diameter, h=magnet_depth+0.1, $fn=30);
                    }
                }
            }
        }
    }
}

module bin_walls() {
    // Main bin body
    difference() {
        rounded_square_base(bin_width, bin_depth, corner_radius, bin_height - base_height);

        translate([wall_thickness, wall_thickness, base_thickness])
            rounded_square_base(
                interior_width,
                interior_depth,
                corner_radius - wall_thickness,
                bin_height - base_height + 0.1
            );
    }
}

module dividers() {
    // Internal dividers creating compartments

    // X-axis dividers (running along depth)
    for (i = [1:dividers_x]) {
        x_pos = wall_thickness + (interior_width / (dividers_x + 1)) * i;
        translate([x_pos - divider_thickness/2, wall_thickness, base_thickness])
            cube([divider_thickness, interior_depth, interior_height]);
    }

    // Y-axis dividers (running along width)
    for (i = [1:dividers_y]) {
        y_pos = wall_thickness + (interior_depth / (dividers_y + 1)) * i;
        translate([wall_thickness, y_pos - divider_thickness/2, base_thickness])
            cube([interior_width, divider_thickness, interior_height]);
    }
}

module stacking_lip() {
    translate([0, 0, stacking_lip_height])
        mirror([0, 0, 1])
            gridfinity_base_profile();
}

module rounded_square_base(width, depth, radius, height) {
    hull() {
        translate([radius, radius, 0])
            cylinder(r=radius, h=height, $fn=40);
        translate([width-radius, radius, 0])
            cylinder(r=radius, h=height, $fn=40);
        translate([radius, depth-radius, 0])
            cylinder(r=radius, h=height, $fn=40);
        translate([width-radius, depth-radius, 0])
            cylinder(r=radius, h=height, $fn=40);
    }
}

// Main assembly
union() {
    // Base profile
    gridfinity_base_profile();

    // Bin walls
    translate([0, 0, base_height])
        bin_walls();

    // Internal dividers
    translate([0, 0, base_height])
        dividers();

    // Optional stacking lip
    if (include_stacking_lip) {
        translate([0, 0, bin_height])
            stacking_lip();
    }
}
```

## Key Dimensions

**Compartment calculation**:

- X compartments: dividers_x + 1
- Y compartments: dividers_y + 1
- Total compartments: (dividers_x + 1) × (dividers_y + 1)

**Example**:

- dividers_x = 2, dividers_y = 1
- Results in 3 × 2 = 6 compartments

**Divider thickness**:

- 1.0mm: Minimum, fragile
- 1.2mm: Standard, good balance
- 1.6mm: Strong, for tall bins

## Usage Examples

**Electronics resistor organizer 4×2×3u**:

```openscad
grid_x = 4;
grid_y = 2;
height_u = 3;
dividers_x = 7;  // 8 compartments along width
dividers_y = 1;  // 2 rows
divider_thickness = 1.0;  // Thin dividers for max compartments
```

Result: 16 small compartments for resistor values

**Screw/bolt sorter 3×3×5u**:

```openscad
grid_x = 3;
grid_y = 3;
height_u = 5;
dividers_x = 2;  // 3×3 grid
dividers_y = 2;
divider_thickness = 1.2;  // Standard dividers
```

Result: 9 compartments for different screw sizes

**Bead/craft organizer 2×4×4u**:

```openscad
grid_x = 2;
grid_y = 4;
height_u = 4;
dividers_x = 1;  // 2 wide
dividers_y = 7;  // 8 deep (many small compartments)
divider_thickness = 1.0;
```

Result: 16 narrow compartments for bead colors

## Design Considerations

**Minimum compartment size**:

- Width/depth ≥ 10mm for practical use
- Smaller compartments difficult to access
- Calculate: interior_width / (dividers_x + 1) ≥ 10mm

**Divider height**:

- Typically extends full interior height
- Can be reduced for finger access to bottom
- Modify: `interior_height - 5` to leave 5mm gap

**Divider strength**:

- Thin dividers (1.0mm) may flex in tall bins
- Use thicker dividers (1.6mm) for height > 5u
- Consider adding fillet at base for reinforcement

## Common Modifications

**Asymmetric compartments** (different spacing):

```openscad
// Replace uniform dividers() module with custom positions
module dividers_custom() {
    // Manual X positions (e.g., 1/3 and 2/3 split)
    divider_positions_x = [interior_width/3, interior_width*2/3];
    for (x_pos = divider_positions_x) {
        translate([wall_thickness + x_pos - divider_thickness/2, wall_thickness, base_thickness])
            cube([divider_thickness, interior_depth, interior_height]);
    }

    // Custom Y positions
    divider_positions_y = [interior_depth/2];  // Single center divider
    for (y_pos = divider_positions_y) {
        translate([wall_thickness, wall_thickness + y_pos - divider_thickness/2, base_thickness])
            cube([interior_width, divider_thickness, interior_height]);
    }
}
```

**Low-profile dividers** (for finger access):

```openscad
// In dividers() module, replace interior_height with:
divider_height = interior_height - 8;  // 8mm gap at top for access
```

**Reinforced divider base** (filleted join):

```openscad
// Add to dividers() module (requires MCAD or custom fillet):
translate([x_pos, wall_thickness, base_thickness])
    union() {
        cube([divider_thickness, interior_depth, divider_height]);
        // Add triangular fillet at base
        for (side = [0, divider_thickness]) {
            translate([side, 0, 0])
                rotate([0, side == 0 ? 45 : -45, 0])
                    cube([1, interior_depth, 1.4]);
        }
    }
```

**Chamfered divider tops** (easier loading):

```openscad
// Replace cube with chamfered shape:
hull() {
    translate([x_pos - divider_thickness/2, wall_thickness, base_thickness])
        cube([divider_thickness, interior_depth, divider_height - 2]);
    translate([x_pos - divider_thickness/2 + 0.5, wall_thickness, base_thickness])
        cube([divider_thickness - 1, interior_depth, divider_height]);
}
```

## Compartment Size Calculation Helper

```openscad
// Calculate and display compartment dimensions
compartment_width = interior_width / (dividers_x + 1);
compartment_depth = interior_depth / (dividers_y + 1);

echo("=== Compartment Dimensions ===");
echo(str("Compartments: ", (dividers_x+1), " × ", (dividers_y+1), " = ", (dividers_x+1)*(dividers_y+1), " total"));
echo(str("Each compartment: ", compartment_width, "mm × ", compartment_depth, "mm × ", interior_height, "mm"));
echo(str("WARNING: Minimum recommended size is 10mm × 10mm"));

if (compartment_width < 10 || compartment_depth < 10) {
    echo("!!! WARNING: Compartments may be too small for practical use !!!");
}
```

## Print Considerations

**Layer adhesion**:

- Dividers can be weak points if under-extruded
- Increase flow rate by 2-3% if dividers separate
- Use PETG for better layer bonding than PLA

**Print time**:

- Dividers significantly increase print time
- 3×3×4u bin with 2×2 dividers ≈ 4-6 hours
- Consider lite_bin variant if speed critical

**Support**:

- No supports needed if divider_height > 5mm
- Very thin/tall dividers may need internal support
- Orient print with dividers aligned to print direction for strength
