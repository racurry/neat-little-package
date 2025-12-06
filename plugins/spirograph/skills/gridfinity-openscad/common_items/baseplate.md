# Gridfinity Baseplate

Grid baseplate with Z-shaped sockets that hold Gridfinity bins. Used for drawers, desktops, or custom mounting.

## When to Use

- Creating custom drawer organizer base
- Desktop organization platform
- Magnetic mounting surface (with magnets)
- Non-standard bin arrangements

## Module Code

```openscad
// Gridfinity Baseplate Module
// Creates baseplate with sockets for bins

// Parameters
grid_x = 5;              // Grid units wide
grid_y = 4;              // Grid units deep

// Gridfinity constants
grid_size = 42;          // Grid spacing
bin_size = 41.5;         // Bin dimension
corner_radius = 3.75;    // Fillet radius

// Baseplate structure
baseplate_thickness = 5;     // Main platform thickness
socket_depth = 4.75;         // Depth of socket (Z-profile height)
rim_height = 0.8;            // Raised rim around each socket

// Optional features
include_magnets = false;
magnet_diameter = 6;
magnet_depth = 2;
include_mounting_holes = false;
mounting_hole_diameter = 3.2;  // M3 clearance

// Calculated dimensions
plate_width = grid_size * grid_x;
plate_depth = grid_size * grid_y;

module socket_profile() {
    // Z-shaped socket that holds bin base
    // This is the inverse of the bin's base profile

    difference() {
        // Outer socket boundary
        rounded_square(bin_size, bin_size, corner_radius, socket_depth);

        // Socket interior (hollow for bin base to fit)
        translate([wall_gap, wall_gap, -0.1])
            rounded_square(
                bin_size - wall_gap*2,
                bin_size - wall_gap*2,
                corner_radius - wall_gap,
                socket_depth + 0.2
            );

        // Central depression (allows bin base to seat)
        translate([4, 4, rim_height])
            rounded_square(
                bin_size - 8,
                bin_size - 8,
                corner_radius - 4,
                socket_depth
            );
    }

    wall_gap = 0.25;  // Clearance for bin to fit
}

module mounting_holes_array() {
    // Optional screw holes for securing baseplate
    hole_offset = 10;  // Distance from edge

    // Four corners
    translate([hole_offset, hole_offset, -0.1])
        cylinder(d=mounting_hole_diameter, h=baseplate_thickness+0.2, $fn=20);
    translate([plate_width-hole_offset, hole_offset, -0.1])
        cylinder(d=mounting_hole_diameter, h=baseplate_thickness+0.2, $fn=20);
    translate([hole_offset, plate_depth-hole_offset, -0.1])
        cylinder(d=mounting_hole_diameter, h=baseplate_thickness+0.2, $fn=20);
    translate([plate_width-hole_offset, plate_depth-hole_offset, -0.1])
        cylinder(d=mounting_hole_diameter, h=baseplate_thickness+0.2, $fn=20);
}

module magnet_holes_array() {
    // Magnet holes aligned with bin magnet positions
    magnet_offset = 8;  // From edge of each grid unit

    for (x = [0:grid_x-1]) {
        for (y = [0:grid_y-1]) {
            translate([x * grid_size, y * grid_size, -0.1]) {
                // Four corners per grid unit
                translate([magnet_offset, magnet_offset, 0])
                    cylinder(d=magnet_diameter, h=magnet_depth+0.1, $fn=30);
                translate([grid_size-magnet_offset, magnet_offset, 0])
                    cylinder(d=magnet_diameter, h=magnet_depth+0.1, $fn=30);
                translate([magnet_offset, grid_size-magnet_offset, 0])
                    cylinder(d=magnet_diameter, h=magnet_depth+0.1, $fn=30);
                translate([grid_size-magnet_offset, grid_size-magnet_offset, 0])
                    cylinder(d=magnet_diameter, h=magnet_depth+0.1, $fn=30);
            }
        }
    }
}

module rounded_square(width, depth, radius, height) {
    // Helper: Rounded rectangle
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
difference() {
    union() {
        // Base platform
        rounded_square(plate_width, plate_depth, corner_radius*2, baseplate_thickness);

        // Raised sockets for each grid position
        for (x = [0:grid_x-1]) {
            for (y = [0:grid_y-1]) {
                translate([x * grid_size + (grid_size - bin_size)/2,
                          y * grid_size + (grid_size - bin_size)/2,
                          baseplate_thickness])
                    socket_profile();
            }
        }
    }

    // Optional features
    if (include_magnets) {
        translate([(grid_size - bin_size)/2, (grid_size - bin_size)/2, 0])
            magnet_holes_array();
    }

    if (include_mounting_holes) {
        mounting_holes_array();
    }
}
```

## Key Dimensions

**Grid spacing**: 42mm center-to-center
**Socket size**: 41.5mm (matches bin base)
**Socket depth**: ~4.75mm (Z-profile engagement)
**Baseplate thickness**: 5mm (can be thicker for rigidity)

**Clearances**:

- 0.25mm gap around socket for bin fit
- 0.5mm total tolerance per bin

## Usage Examples

**Standard 5×4 drawer organizer**:

```openscad
grid_x = 5;
grid_y = 4;
include_magnets = false;
include_mounting_holes = true;
```

Result: 210mm × 168mm baseplate with screw mounting

**Magnetic desktop platform 3×3**:

```openscad
grid_x = 3;
grid_y = 3;
include_magnets = true;
include_mounting_holes = false;
baseplate_thickness = 6;  // Extra thickness for stability
```

Result: 126mm × 126mm magnetic baseplate

**Large toolbox insert 8×6**:

```openscad
grid_x = 8;
grid_y = 6;
include_magnets = false;
include_mounting_holes = true;
baseplate_thickness = 7;  // Thicker for large span
```

Result: 336mm × 252mm reinforced baseplate

## Design Considerations

**Baseplate thickness**:

- 5mm: Standard, works for most sizes
- 6-7mm: Recommended for grids larger than 5×5
- 8mm+: Very large baseplates or heavy loads

**Magnet polarity**:

- Keep consistent orientation across all magnets
- Mark polarity on underside for reference
- Test with first bin to ensure attraction (not repulsion)

**Mounting holes**:

- M3 clearance (3.2mm) for screws
- Countersink option for flush mounting
- Consider edge spacing for drawer clearance

**Print orientation**:

- Print face-up (sockets on top)
- No supports needed if designed correctly
- May need brim for large baseplates (warping prevention)

## Common Modifications

**Add countersunk mounting holes**:

```openscad
// Replace mounting_hole_diameter cylinder with:
translate([hole_offset, hole_offset, baseplate_thickness - 2])
    cylinder(d1=mounting_hole_diameter, d2=6, h=2.1, $fn=30);
translate([hole_offset, hole_offset, -0.1])
    cylinder(d=mounting_hole_diameter, h=baseplate_thickness-1.9, $fn=20);
```

**Add drawer label area**:

```openscad
// Add to difference section:
translate([plate_width/2, -5, baseplate_thickness/2])
    cube([plate_width*0.8, 10, 3], center=true);
```

**Add anti-slip texture**:

```openscad
// Add to bottom surface:
for (x = [5:10:plate_width-5]) {
    for (y = [5:10:plate_depth-5]) {
        translate([x, y, -0.1])
            cylinder(d=2, h=0.6, $fn=6);  // Hexagonal bumps
    }
}
```

## Exact Drawer Fit Calculation

**For custom drawer dimensions**:

```openscad
// Measure drawer interior
drawer_width = 350;
drawer_depth = 280;

// Calculate maximum grid units that fit
max_grid_x = floor(drawer_width / grid_size);   // 8 units
max_grid_y = floor(drawer_depth / grid_size);   // 6 units

// Calculate actual baseplate size
plate_width = max_grid_x * grid_size;   // 336mm (14mm margin)
plate_depth = max_grid_y * grid_size;   // 252mm (28mm margin)

// Use these values:
grid_x = 8;
grid_y = 6;
```

**Margin consideration**: Leave 5-10mm margin on each side for drawer clearance and printing tolerances.
