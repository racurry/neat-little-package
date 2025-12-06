# Gridfinity Lite Bin

Thin-wall variant optimized for vase mode / spiral printing. Significantly faster print times and lower filament usage while maintaining Gridfinity compatibility.

## When to Use

- Need bins quickly (print time critical)
- Minimizing filament cost/usage
- Lightweight applications
- Drawer organization where strength isn't critical
- User explicitly requests "vase mode" or "fast print"

## Module Code

```openscad
// Gridfinity Lite Bin Module
// Thin-wall design for vase mode printing

// Grid dimensions
grid_x = 2;              // Grid units wide
grid_y = 2;              // Grid units deep
height_u = 4;            // Height units

// Gridfinity constants
grid_size = 42;
bin_size = 41.5;
height_unit = 7;
corner_radius = 3.75;

// Lite bin parameters
wall_thickness = 1.2;    // Single-wall thickness (typically 3× nozzle width)
base_height = 5;         // Base profile height
floor_layers = 3;        // Number of solid floor layers (× layer_height)
layer_height = 0.2;      // Expected print layer height

// Optional (rarely used in vase mode)
include_magnets = false;
magnet_diameter = 6;
magnet_depth = 2;

// Calculated dimensions
bin_width = bin_size * grid_x;
bin_depth = bin_size * grid_y;
bin_height = height_unit * height_u;
floor_thickness = floor_layers * layer_height;

module lite_base_profile() {
    // Simplified base profile for vase mode compatibility
    // Single-wall spiral cannot create complex geometry
    // This is a compromise that maintains functional compatibility

    difference() {
        // Outer perimeter (continuous spiral path)
        for (x = [0:grid_x-1]) {
            for (y = [0:grid_y-1]) {
                translate([x * grid_size, y * grid_size, 0])
                    rounded_square(bin_size, bin_size, corner_radius, base_height);
            }
        }

        // Inner cavity (vase mode will create this automatically)
        translate([wall_thickness, wall_thickness, floor_thickness])
            for (x = [0:grid_x-1]) {
                for (y = [0:grid_y-1]) {
                    translate([x * grid_size, y * grid_size, 0])
                        rounded_square(
                            bin_size - wall_thickness*2,
                            bin_size - wall_thickness*2,
                            corner_radius - wall_thickness,
                            base_height
                        );
                }
            }

        // Simplified socket engagement (stepped profile)
        // Not as secure as standard bins but works for light use
        translate([wall_thickness + 1.5, wall_thickness + 1.5, floor_thickness])
            for (x = [0:grid_x-1]) {
                for (y = [0:grid_y-1]) {
                    translate([x * grid_size, y * grid_size, 0])
                        rounded_square(
                            bin_size - wall_thickness*2 - 3,
                            bin_size - wall_thickness*2 - 3,
                            corner_radius - wall_thickness - 1.5,
                            2.5
                        );
                }
            }

        // Magnet holes (optional, but disables true vase mode)
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

module lite_bin_walls() {
    // Continuous single-wall body for vase mode
    difference() {
        // Outer shell
        rounded_square(bin_width, bin_depth, corner_radius, bin_height - base_height);

        // Interior (vase mode spirals this automatically)
        translate([wall_thickness, wall_thickness, -0.1])
            rounded_square(
                bin_width - wall_thickness*2,
                bin_depth - wall_thickness*2,
                corner_radius - wall_thickness,
                bin_height - base_height + 0.2
            );
    }
}

module rounded_square(width, depth, radius, height) {
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
    // Simplified base
    lite_base_profile();

    // Continuous wall body
    translate([0, 0, base_height])
        lite_bin_walls();
}
```

## Key Dimensions

**Wall thickness**:

- Typically 3× nozzle diameter
- 0.4mm nozzle → 1.2mm wall
- 0.6mm nozzle → 1.8mm wall

**Floor thickness**:

- 3-5 solid layers before vase mode starts
- 3 layers @ 0.2mm = 0.6mm floor
- Provides rigidity without adding time

**Base profile**:

- Simplified compared to standard bins
- Sufficient for drawer organization
- Less secure on baseplates (acceptable trade-off)

## Vase Mode Slicer Settings

**Enable vase mode**:

- PrusaSlicer: "Spiral vase" mode
- Cura: "Spiralize outer contour"
- Bambu Studio: "Spiral vase"

**Critical settings**:

```
Bottom layers: 3-5 (solid floor)
Perimeters: 1 (vase mode forces this)
Top layers: 0 (vase mode = no top)
Infill: 0% (not used in vase mode)
Layer height: 0.2mm recommended
```

**Speed recommendations**:

- Print speed: 80-120 mm/s (fast, single wall)
- First layer: 30-40 mm/s (adhesion)
- 2×2×4u bin ≈ 1-1.5 hours (vs 3-4 hours standard)

## Usage Examples

**Fast desk organizer 2×2×4u**:

```openscad
grid_x = 2;
grid_y = 2;
height_u = 4;
wall_thickness = 1.2;  // For 0.4mm nozzle
```

Print time: ~1.5 hours (vs 4 hours standard bin)

**Drawer parts organizer 3×1×3u**:

```openscad
grid_x = 3;
grid_y = 1;
height_u = 3;
wall_thickness = 1.2;
```

Result: Lightweight shallow bin, very fast print

**Large but quick bin 4×4×5u**:

```openscad
grid_x = 4;
grid_y = 4;
height_u = 5;
wall_thickness = 1.6;  // Slightly thicker for large size
layer_height = 0.3;    // Thicker layers for speed
```

Result: Large bin in ~3-4 hours (standard would be 8+ hours)

## Design Considerations

**Strength limitations**:

- Single wall is fragile compared to standard bins
- Not suitable for heavy items or rough handling
- Adequate for light desktop/drawer organization
- Cannot be stacked with load (no stacking lip)

**Base engagement**:

- Simplified base profile is less secure than standard
- Works fine in drawers (lateral movement limited)
- May slide on desktop baseplates (use magnets if critical)
- Trade-off accepted for speed/cost savings

**Customization restrictions**:

- No dividers (would break vase mode)
- No stacking lip (incompatible with spiral)
- Magnets possible but disable true vase mode
- Label recess must be external only

## Print Optimization

**Orientation**:

- Always print upright (Z-axis = bin height)
- Vase mode requires continuous spiral path
- Do not rotate or print on side

**Nozzle size impact**:

```
0.4mm nozzle:
  wall_thickness = 1.2mm (3 × 0.4mm)
  Fine detail, slower

0.6mm nozzle:
  wall_thickness = 1.8mm (3 × 0.6mm)
  Faster print, thicker/stronger wall
  Recommended for large bins
```

**Layer height optimization**:

```
0.15mm: Fine detail, slower
0.20mm: Standard, good balance (recommended)
0.25mm: Fast, coarser
0.30mm: Very fast, visible layers
```

**Material recommendations**:

- PLA: Fastest, rigid, good for most use
- PETG: Stronger, flexible, better for rough handling
- ABS: Strong but warp-prone (not recommended)

## Common Modifications

**Thicker floor** (for heavier items):

```openscad
floor_layers = 5;  // 1mm floor @ 0.2mm layers
```

**External label clip** (vase-mode compatible):

```openscad
// Add to exterior, does not break spiral:
translate([bin_width/2, -2, bin_height - 10])
    rotate([90, 0, 0])
        difference() {
            cylinder(d=8, h=3, $fn=30);
            cylinder(d=6, h=3.2, $fn=30);
        }
```

**Drainage slots** (bottom floor):

```openscad
// Add to lite_base_profile difference section:
for (x = [10:15:bin_width-10]) {
    translate([x, bin_depth/2, -0.1])
        cube([2, bin_depth-wall_thickness*4, floor_thickness+0.2]);
}
```

## Performance Comparison

**2×3×4u bin comparison**:

| Aspect | Standard Bin | Lite Bin |
|--------|--------------|----------|
| Print time | 3-4 hours | 1-2 hours |
| Filament | 25-30g | 8-12g |
| Strength | High | Low-Medium |
| Base grip | Excellent | Good |
| Stackable | Yes (with lip) | No |
| Cost | $0.75-1.00 | $0.25-0.40 |

**When to choose lite**:

- Speed is priority
- Drawer organization (not desktop)
- Light items (paper clips, SD cards, small parts)
- Cost-sensitive projects (many bins needed)

**When to choose standard**:

- Durability critical
- Stacking required
- Heavy items
- Desktop use (better base engagement)

## Non-Vase Mode Lite Bin

**Can also print lite bins in normal mode**:

```
Slicer settings (normal mode):
Perimeters: 2-3 (instead of vase mode's 1)
Top layers: 3
Bottom layers: 3
Infill: 10-15%
```

**Benefits**:

- Allows dividers, magnet holes, complex features
- Still faster/cheaper than standard wall thickness
- Slightly stronger than pure vase mode
- Top closure (vs open top in vase mode)

**Trade-offs**:

- Longer print time than vase mode
- More filament than vase mode
- Still weaker than standard bins
