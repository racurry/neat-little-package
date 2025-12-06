# Basic Gridfinity Bin

Standard Gridfinity bin with proper base profile and optional stacking lip. This is the most common pattern.

## When to Use

- Generic desktop/drawer organization
- Single-type items (all screws, all batteries, all pens)
- Standard Gridfinity applications
- User requests "Gridfinity bin" without specific customization

## Module Code

```openscad
// Gridfinity Basic Bin Module
// Standard bin with base profile and optional stacking lip

// Parameters
grid_x = 2;              // Grid units wide (1 unit = 42mm grid spacing)
grid_y = 3;              // Grid units deep
height_u = 4;            // Height units (1u = 7mm)

// Gridfinity constants
grid_size = 42;          // Grid spacing (centers of bins)
bin_size = 41.5;         // Actual bin dimension (0.5mm total tolerance)
height_unit = 7;         // Height increment
corner_radius = 3.75;    // Fillet radius
stacking_lip_height = 4.4;  // Stacking lip thickness

// Structural parameters
wall_thickness = 2.0;    // Wall thickness (1.6-2.4mm typical)
base_thickness = 2.0;    // Floor thickness above base profile

// Optional features
include_stacking_lip = true;
include_magnets = false;
magnet_diameter = 6;     // 6mm × 2mm standard
magnet_depth = 2;

// Calculated dimensions
bin_width = bin_size * grid_x;
bin_depth = bin_size * grid_y;
bin_height = height_unit * height_u;

// Base profile measurements (Z-shaped socket engagement)
base_height = 5;         // Height of base profile
base_inner = 36.5;       // Inner dimension of base
base_chamfer = 0.8;      // Chamfer at transitions

module gridfinity_base_profile() {
    // Creates the Z-shaped profile that locks into baseplate
    // This is critical - without it, bin won't engage baseplate

    difference() {
        union() {
            // Outer base perimeter
            for (x = [0:grid_x-1]) {
                for (y = [0:grid_y-1]) {
                    translate([x * grid_size, y * grid_size, 0])
                        rounded_square_base(bin_size, bin_size, corner_radius, base_height);
                }
            }
        }

        // Hollow interior (socket profile)
        translate([wall_thickness, wall_thickness, -0.1])
            for (x = [0:grid_x-1]) {
                for (y = [0:grid_y-1]) {
                    translate([x * grid_size, y * grid_size, 0])
                        rounded_square_base(
                            base_inner,
                            base_inner,
                            corner_radius - wall_thickness,
                            base_height + 0.2
                        );
                }
            }

        // Magnet holes (optional)
        if (include_magnets) {
            for (x = [0:grid_x-1]) {
                for (y = [0:grid_y-1]) {
                    translate([x * grid_size, y * grid_size, 0]) {
                        // Four corners per grid unit
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
    // Main bin body above base profile
    difference() {
        // Outer shell
        rounded_square_base(
            bin_width,
            bin_depth,
            corner_radius,
            bin_height - base_height
        );

        // Interior cavity
        translate([wall_thickness, wall_thickness, base_thickness])
            rounded_square_base(
                bin_width - wall_thickness*2,
                bin_depth - wall_thickness*2,
                corner_radius - wall_thickness,
                bin_height - base_height + 0.1
            );
    }
}

module stacking_lip() {
    // Inverted base profile at top for stacking
    // This must mirror the base profile geometry

    translate([0, 0, stacking_lip_height])
        mirror([0, 0, 1])
            gridfinity_base_profile();
}

module rounded_square_base(width, depth, radius, height) {
    // Helper: Rounded rectangle profile
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
    // Base profile (required)
    gridfinity_base_profile();

    // Bin walls
    translate([0, 0, base_height])
        bin_walls();

    // Optional stacking lip
    if (include_stacking_lip) {
        translate([0, 0, bin_height])
            stacking_lip();
    }
}
```

## Key Dimensions

**Per grid unit**:

- Grid spacing: 42mm (center-to-center)
- Bin size: 41.5mm (actual dimension)
- Tolerance: 0.5mm total (0.25mm per side)

**Base profile**:

- Height: ~5mm
- Inner dimension: ~36.5mm
- This matches Z-shaped socket in baseplate

**Height calculation**:

- Total height = height_u × 7mm
- Usable interior ≈ total - 5mm (base) - 2mm (floor) = total - 7mm
- Example: 4u (28mm) bin has ~21mm usable height

## Usage Examples

**Standard 2×3×4u bin**:

```openscad
grid_x = 2;
grid_y = 3;
height_u = 4;
include_stacking_lip = true;
include_magnets = false;
```

Result: 83mm × 124.5mm × 28mm bin with stacking capability

**Magnetic 1×1×3u bin**:

```openscad
grid_x = 1;
grid_y = 1;
height_u = 3;
include_stacking_lip = false;
include_magnets = true;
```

Result: 41.5mm × 41.5mm × 21mm bin with magnet anchoring

**Large desk organizer 4×4×6u**:

```openscad
grid_x = 4;
grid_y = 4;
height_u = 6;
include_stacking_lip = true;
include_magnets = false;
wall_thickness = 2.4;  // Thicker walls for larger bin
```

Result: 166mm × 166mm × 42mm bin with reinforced walls

## Design Considerations

**Minimum recommended height**: 3u (21mm)

- 1u bins have only ~2mm usable interior (impractical)
- 2u bins have ~7mm usable (very shallow)
- 3u bins have ~14mm usable (minimum for most items)

**Wall thickness**:

- 1.6mm: Light-duty, fast printing
- 2.0mm: Standard, good balance
- 2.4mm: Heavy-duty, larger bins

**Magnet placement**:

- 8mm from each corner edge
- 6mm diameter × 2mm depth
- Use rare-earth magnets (neodymium N52)

## Common Modifications

**Add label recess**:

```openscad
// In bin_walls() difference section, add:
translate([bin_width/2, 0, bin_height - base_height - 8])
    rotate([45, 0, 0])
        cube([bin_width*0.6, 10, 10], center=true);
```

**Add drainage holes**:

```openscad
// In bin_walls() difference section, add:
for (x = [10:10:bin_width-10]) {
    for (y = [10:10:bin_depth-10]) {
        translate([x, y, -0.1])
            cylinder(d=3, h=base_thickness+0.2, $fn=20);
    }
}
```

**Add finger scoop**:

```openscad
// In bin_walls() difference section, add:
translate([bin_width/2, -1, base_thickness + 5])
    rotate([-90, 0, 0])
        cylinder(d=20, h=wall_thickness+2, $fn=40);
```
