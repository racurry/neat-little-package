# T Intersection Connector

3-way junction for edges and perpendicular joins. One full-width channel + one half-width channel.

## When to Use

**Use for:**

- Edge connections (divider meets drawer wall perpendicularly)
- Asymmetric layouts (divider extends only one direction)
- T-shaped junctions

**Layout example:**

```
     |
  ───┼
     |
```

## Module Calls

```openscad
// Base piece (with Gridfinity/openGrid/Flat base)
NeoGrid_T_Intersection_Base(
    Material_Thickness,
    Channel_Depth = 20,
    Wall_Thickness = 4,
    grid_size = 42
);

// Top piece (caps junction)
NeoGrid_T_Intersection_Top(
    Material_Thickness,
    Channel_Depth = 20,
    Wall_Thickness = 4,
    grid_size = 42
);
```

## Channel Geometry

**Three channels in T configuration**:

**Full-width channel** (X-axis):

- Extends full width: `grid_size × grid_x` (42mm default)
- Through-channel for continuous divider
- Supports divider running full length

**Half-width channels** (Y-axis):

- Single channel perpendicular to full-width
- Length: `(grid_size × grid_y) / 2 + Material_Thickness/2 + Wall_Thickness`
- Only one direction (half of X Intersection)
- Use when divider doesn't extend to far side

**Material insertion**:

- All channels have top chamfers for easy insertion
- Retention spikes (optional) in channels
- Friction fit: ±0.15mm tolerance

## Print Orientation

**Both pieces print upright**:

- Base: Base profile at bottom, channels opening upward
- Top: Channels opening downward, flat surface at top
- No supports needed

## Common Use Cases

**Drawer edge junctions:**

```
Drawer wall
─────────────
     |
  ───┼     (T Intersection against wall)
     |
```

**Asymmetric compartments:**

```
  ───┼───  (Full divider spans width)
     |     (Perpendicular divider only needed one side)
```

**Grid edge closures:**

- Regular grid meets drawer edge
- T Intersections cap ends of cross-dividers
- Alternative to Straight End connectors (T is stronger)

## Assembly

1. Place base piece at junction location
2. Insert full-width divider through X-axis channel
3. Insert half-width divider into Y-axis channel
4. Place top piece, pressing down until seated

## Example Layout

**User: "2×3 grid against drawer edge"**

Components:

- Interior: 2 X Intersections (interior junctions)
- Edge (perpendicular): 6 T Intersections (where dividers meet edge)
- Edge (parallel): 0 (dividers run along edge, no connector needed)
- Corners: 4 L Intersections

## Common Issues

**Full-width channel too short:**

- Verify grid_size matches Selected_Base (42mm for Gridfinity)
- Check grid_x/grid_y if multi-tile (Gridfinity only)

**Half-width channel wrong direction:**

- Rotate connector 90° or 180° as needed
- QuackWorks code: Half channel extends in +Y direction
- Use `zrot()` in OpenSCAD to reorient if needed

**Top doesn't align:**

- Ensure dividers are perpendicular (90° angle)
- Check divider lengths match channel depths
- Verify Material_Thickness is consistent across all dividers
