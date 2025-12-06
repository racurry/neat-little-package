# L Intersection Connector

Corner junction for 90° turns. Two perpendicular half-width channels.

## When to Use

**Use for:**

- Corner connections (drawer corners)
- 90° turns in divider layout
- L-shaped junctions

**Layout example:**

```
     |
     └───
```

## Module Calls

```openscad
// Base piece (with Gridfinity/openGrid/Flat base)
NeoGrid_L_Intersection_Base(
    Material_Thickness,
    Channel_Depth = 20,
    Wall_Thickness = 4,
    grid_size = 42
);

// Top piece (caps junction)
NeoGrid_L_Intersection_Top(
    Material_Thickness,
    Channel_Depth = 20,
    Wall_Thickness = 4,
    grid_size = 42
);
```

## Channel Geometry

**Two perpendicular half-width channels**:

**X-axis channel**:

- Length: `(grid_size × grid_x) / 2 + Wall_Thickness + Material_Thickness/2`
- Extends in one direction only (not through-channel)

**Y-axis channel**:

- Length: `(grid_size × grid_y) / 2 + Wall_Thickness + Material_Thickness/2`
- Perpendicular to X-axis channel
- Forms 90° corner

**Material insertion**:

- Top chamfers on both channels
- Optional retention spikes
- Friction fit: ±0.15mm tolerance

## Print Orientation

**Both pieces print upright**:

- Base: Base profile at bottom, L-shaped channels opening upward
- Top: L-shaped channels opening downward
- No supports needed

## Common Use Cases

**Drawer corners:**

```
Drawer corner
┌─────────
│    |
│    └───  (L Intersection in corner)
```

**Grid corners:**

- Where regular grid meets two drawer edges simultaneously
- All four drawer corners in grid layout

**90° layout changes:**

- Path divider layout turns corner
- Asymmetric compartments with corner dividers

## Assembly

1. Place base piece at corner location
2. Insert first divider into one channel
3. Insert second divider into perpendicular channel
4. Verify 90° angle between dividers
5. Place top piece, pressing down until seated

## Orientation Notes

**L Intersection has rotational orientation**:

```
Default orientation (QuackWorks):
     |
     └───

Rotate 90° (zrot(90)):
  ───┘
     |

Rotate 180° (zrot(180)):
  ───┐
     |

Rotate 270° (zrot(270)):
     |
  ───┘
```

**In OpenSCAD**: Use `zrot(angle)` to orient connector for specific corner.

## Example Layout

**User: "Grid in rectangular drawer"**

Components:

- 4 L Intersections (one per drawer corner)
- Orientation per corner:
  - Front-left: `zrot(0)` - channels extend right and back
  - Front-right: `zrot(90)` - channels extend left and back
  - Back-right: `zrot(180)` - channels extend left and forward
  - Back-left: `zrot(270)` - channels extend right and forward

## Common Issues

**Wrong corner orientation:**

- Use `zrot()` to rotate L Intersection to match corner
- Channels should extend away from corner (not into drawer walls)

**Dividers not 90°:**

- Ensure dividers cut square (90° edges)
- Check corner angle in drawer (some drawers not perfectly square)
- Minor misalignment acceptable (connectors have some flex)

**Gaps at drawer edge:**

- L Intersection doesn't touch drawer wall directly
- Use Vertical Trim or Straight End for wall contact if needed
- Or plan divider lengths to reach wall closely
