# Straight End Connector

Terminator for open divider ends. Partial channel with buffer for cutting tolerance.

## When to Use

**Use for:**

- Open divider ends (not meeting other dividers)
- Edge terminations (against drawer walls)
- End caps for divider runs

**Layout example:**

```
     |
     └  (end cap)
```

## Module Calls

```openscad
// Base piece (with Gridfinity/openGrid/Flat base)
NeoGrid_Straight_End_Base(
    Material_Thickness,
    Channel_Depth = 20,
    Wall_Thickness = 4,
    grid_size = 42
);

// Top piece (caps end)
NeoGrid_Straight_End_Top(
    Material_Thickness,
    Channel_Depth = 20,
    Wall_Thickness = 4,
    grid_size = 42
);
```

## Channel Geometry

**Partial channel** (not through-channel):

**Channel length**:

- Length: `Channel_Length - Partial_Channel_Buffer`
- Default buffer: 3mm (allows divider cutting tolerance)
- Channel doesn't extend through connector fully

**Material insertion**:

- Chamfer at open end eases insertion
- Closed end prevents divider from passing through
- Retention spikes (optional) grip divider

**Buffer purpose**: Accommodates imprecise divider cuts. Divider can be slightly short without gap showing.

## Print Orientation

**Both pieces print upright**:

- Base: Base profile at bottom, partial channel opening upward
- Top: Partial channel opening downward
- No supports needed

## Common Use Cases

### Drawer Edge Termination

**Divider ends at drawer wall**:

```
Drawer wall
─────────────
     |
     └  ← Straight End against wall
```

**Use case**: Grid layout where some dividers end before reaching far edge.

### Open Compartment End

**Asymmetric layout** with partial dividers:

```
  ┌─────┬───┐
  │     │   └  ← Straight End (divider stops mid-drawer)
  └─────┴─────
```

**Use case**: One large compartment + smaller sections.

### Alternative to T/L for Edges

**Instead of T/L Intersection** at drawer edge:

- **T Intersection**: Stronger, three-way junction
- **Straight End**: Simpler, just caps one divider
- **Choice**: Use Straight End if no perpendicular divider needed

## Assembly

1. Place base piece at divider end location
2. Insert divider into partial channel
3. Divider stops at closed end of channel
4. Place top piece, pressing down

**Buffer allows**: Divider 3mm shorter than channel, still looks complete.

## Partial_Channel_Buffer Parameter

**Hidden parameter** in QuackWorks code:

```openscad
Partial_Channel_Buffer = 3;  // Default
```

**Purpose**: Forgiveness for imprecise cuts.

**Calculation**:

```openscad
// Actual channel depth:
effective_channel_length = Channel_Length - Partial_Channel_Buffer;
// Example: 42mm - 3mm = 39mm usable channel
```

**Divider cutting guidance**: Cut dividers 2-3mm shorter than full span to account for buffer.

## Example Layout

**User: "Dividers meet drawer wall on one side only"**

Components:

- Interior junctions: X or T Intersections (as appropriate)
- Wall edge: Straight End connectors (cap dividers at wall)
- Result: Dividers terminate cleanly without through-channel

**Count**: One Straight End per divider that ends at edge (doesn't continue).

## Orientation

**Straight End has directional orientation**:

```openscad
// Default: Open end faces left, closed end right
// Use zrot() to reorient:

zrot(0);    // Open left
zrot(90);   // Open forward
zrot(180);  // Open right
zrot(270);  // Open backward
```

**Position closed end**: Toward drawer wall or desired termination point.

## Common Issues

**Gap between divider and connector:**

- Divider too short (cut longer or accept gap)
- Buffer too large (reduce Partial_Channel_Buffer if editing source)

**Divider won't insert fully:**

- Divider too long (trim 2-3mm)
- Channel blocked (check for debris)

**Used Straight End instead of T/L:**

- If perpendicular divider needed later, replace with T or L
- Straight End is simpler but less versatile than T for edges

**Wrong orientation:**

- Rotate with `zrot()` to face open end toward divider direction
- Closed end should face termination point (wall/edge)
