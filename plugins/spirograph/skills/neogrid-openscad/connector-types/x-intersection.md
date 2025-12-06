# X Intersection Connector

4-way junction for interior grid points. Most versatile and commonly used connector.

## When to Use

**Use for:**

- Interior grid intersections (where 4 dividers cross)
- Regular grid layouts
- Test prints (verify material fit before batch printing)

**Layout example:**

```
     |
  ───┼───
     |
```

## Module Calls

```openscad
// Base piece (with Gridfinity/openGrid/Flat base)
NeoGrid_X_Intersection_Base(
    Material_Thickness,
    Channel_Depth = 20,
    Wall_Thickness = 4,
    grid_size = 42
);

// Top piece (caps junction)
NeoGrid_X_Intersection_Top(
    Material_Thickness,
    Channel_Depth = 20,
    Wall_Thickness = 4,
    grid_size = 42
);
```

## Multi-Tile Support (Gridfinity Only)

**X Intersection supports multi-tile bases**:

```openscad
// Expand base to 2×3 Gridfinity tiles (84mm × 126mm)
grid_x = 2;  // 2 tiles wide
grid_y = 3;  // 3 tiles deep

// Channels extend full grid_size × grid_x/grid_y
// Channel length X-axis: 42mm × grid_x
// Channel length Y-axis: 42mm × grid_y
```

**Use case**: Large drawer divider systems spanning multiple Gridfinity grid squares.

**Limitation**: Only Gridfinity base supports multi-tile. Flat/openGrid/None use single tile only.

## Channel Geometry

**Four perpendicular channels**:

- Two channels along X-axis (left-right)
- Two channels along Y-axis (front-back)
- All channels same width: `Material_Thickness`
- All channels same depth: `Channel_Depth` (default 20mm)

**Material insertion**:

- Chamfers at top of channels ease insertion
- Retention spikes (optional) grip soft materials (MDF)
- Friction fit: ±0.15mm tolerance on Material_Thickness

## Print Orientation

**Both pieces print upright** (as displayed in OpenSCAD):

- Base: Gridfinity/openGrid profile at bottom, channels opening upward
- Top: Channels opening downward, flat surface at top
- No supports needed for either piece

## Assembly

1. Place base piece in drawer (snap to baseplate or adhere if Flat base)
2. Insert dividers into four channels (perpendicular cross pattern)
3. Place top piece over junction, pressing down until fully seated
4. Top piece locks dividers vertically

## Example Layout Calculation

**User: "3×3 grid in 300mm × 300mm drawer"**

Components needed:

- Interior junctions: 4 X Intersections (where grid lines cross)
- Edge junctions: 8 T Intersections (where dividers meet edges)
- Corner junctions: 4 L Intersections (drawer corners)
- Total: 4 X + 8 T + 4 L = 16 connectors + 16 tops

Dividers:

- 6 dividers running X-axis (3 rows × 2 spans each)
- 6 dividers running Y-axis (3 columns × 2 spans each)
- Length: ~100mm each (300mm ÷ 3)

**Start with one X Intersection**: Print base + top, test material fit, then batch remaining.

## Common Issues

**Dividers too loose:**

- Decrease Material_Thickness by 0.1-0.2mm
- Reprint one connector to verify before batch

**Dividers too tight:**

- Increase Material_Thickness by 0.1-0.2mm
- Check if painted material measured AFTER painting

**Top doesn't seat fully:**

- Verify dividers are cut square (90° edges)
- Check channels aren't overfilled with debris
- Ensure Material_Thickness matches actual material

**Base doesn't fit Gridfinity:**

- Verify Selected_Base = "Gridfinity"
- Check baseplate is genuine Gridfinity (42mm grid)
- Ensure grid_size = 42 (not custom value)
