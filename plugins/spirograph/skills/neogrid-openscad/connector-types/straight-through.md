# I Junction (Straight Through) Connector

In-line connection for continuous dividers. Single through-channel.

## When to Use

**Use for:**

- In-line connections (extending divider length)
- Straight runs without intersections
- Standalone divider support (when not using Gridfinity base)

**Layout example:**

```
  ───────
```

## Module Calls

```openscad
// Base piece (with Gridfinity/openGrid/Flat base)
NeoGrid_Straight_Thru_Base(
    Material_Thickness,
    Channel_Depth = 20,
    Wall_Thickness = 4,
    grid_size = 42,
    Channel_Length = 42  // Or custom length
);

// Top piece (caps junction)
NeoGrid_Straight_Thru_Top(
    Material_Thickness,
    Channel_Depth = 20,
    Wall_Thickness = 4,
    grid_size = 42,
    Channel_Length = 42  // Match base
);
```

## Channel Geometry

**Single through-channel**:

- Length: `Channel_Length` (default: `grid_size × grid_y`)
- Width: `Material_Thickness`
- Depth: `Channel_Depth` (default 20mm)
- Orientation: Along channel length direction

**Material insertion**:

- Chamfers at both ends ease insertion
- Divider slides through full length
- Retention spikes (optional) along channel length

## Channel Length Parameter

**Unique to Straight Through**: Has adjustable `Channel_Length` parameter.

```openscad
// Default: Match grid size
Channel_Length = grid_size * grid_y;  // 42mm (1 tile)

// Custom: Extend to match divider length
Channel_Length = 160;  // Match common divider length

// Multi-tile (Gridfinity):
grid_y = 3;
Channel_Length = grid_size * grid_y;  // 126mm
```

**Why adjustable**: Straight connectors often span custom distances, not grid-aligned.

## Print Orientation

**Both pieces print upright**:

- Base: Base profile at bottom, channel horizontal
- Top: Channel opening downward, flat top
- No supports needed

## Common Use Cases

### In-line Extension

**Joining short dividers into longer span**:

```
Divider 1    I Junction    Divider 2
────────────[═══════════]────────────
```

**Use case**: Hardware store only had 8' boards, need 10' divider span.

### Standalone Divider Support

**Without Gridfinity base** (Selected_Base = "None"):

```
  Drawer bottom
  ═════════════════
        │││  ← I Junction provides vertical support
      ─────
```

**Use case**: Simple drawer divider, no modular base system. I Junction acts as foot.

### Parallel Divider Runs

**Multiple parallel dividers** with no intersections:

```
  ─────────  ← Divider 1 with I Junction support

  ─────────  ← Divider 2 with I Junction support

  ─────────  ← Divider 3 with I Junction support
```

**Use case**: Long narrow drawer, dividers run lengthwise only.

## Assembly

1. Place base piece at support location
2. Insert divider through channel
3. Place top piece, pressing down
4. Divider is now supported mid-span

**Multiple I Junctions**: Space evenly along divider for continuous support.

## Example Layout

**User: "Long divider across 600mm drawer"**

Approach:

- 3 I Junctions spaced 200mm apart
- Divider runs through all three
- Each junction provides vertical support
- Alternative: Use single long divider with support at ends (Straight End connectors)

## Common Issues

**Channel_Length doesn't match divider:**

- Verify Channel_Length parameter matches your layout
- Default may be too short for custom applications
- Adjust as needed (not grid-constrained)

**Top piece doesn't align:**

- Ensure Channel_Length identical for base and top
- Check divider is straight (not bowed)
- Verify divider thickness consistent along length

**Used I Junction when X/T/L better:**

- If dividers intersect, use appropriate junction type
- I Junction only for straight-through, no branching
- Consider if intersection needed in future (use X for flexibility)
