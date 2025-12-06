# Curves and Transitions: S, C, Mitre, Height Change Channels

Reference for generating smooth curve and transition channels.

## QuackWorks Reference Files

**Source files:**

- S Channel (Diagonal): `Underware_S_Channel.scad`
- C Channel (Curved): `Underware_C_Channel.scad`
- Mitre Channel: `Underware_Mitre_Channel.scad`
- Height Change Channel: `Underware_Height_Change_Channel.scad`

**Fetch from**: https://github.com/AndyLevesque/QuackWorks/tree/main/Underware

## Channel Selection by Curve Type

| Curve Need | Channel | Geometry | Use Case |
|------------|---------|----------|----------|
| Smooth diagonal transition | S Channel | Bezier curve path | Gradual X/Y position shift |
| Arc around obstacle | C Channel | Circular arc (quarter to full) | Round desk legs, poles, corners |
| 45° angled corner | Mitre Channel | 45° chamfered turn | Sharper than L, softer than 90° |
| Vertical level change | Height Change | Z-axis transition | Wall-to-desk drop, multi-level routing |

## S Channel (Smooth Diagonal)

### When to Use S Channel

**Use when:**

- Gradually shifting cable run from one position to another
- Avoiding obstacles with smooth path (no sharp corners)
- Creating ergonomic cable routing (gentle curves reduce stress)
- Transitioning between offset I Channel runs

**Don't use when:**

- Need tight 90° corner → Use L Channel
- Need perfect circle → Use C Channel
- Need straight diagonal → Use angled I Channel or Mitre

### S Channel Specific Parameters

```openscad
/*[Channel Shape]*/
Channel_Width_in_Units = 1;
Channel_Internal_Height = 12;
Units_Over = 2;                // Horizontal shift (X axis)
Units_Up = 3;                  // Vertical travel (Y axis)
Straight_Distance = 12.5;      // Straight segment before/after curve
```

**Critical understanding**: S Channel creates Bezier curve connecting:

```
Start point (0, 0) → Curve → End point (Units_Over, Units_Up)
```

**Path visualization**:

```
      ╱
     ╱  ← Smooth Bezier curve
    ╱
   ╱
──┘    ← Straight_Distance before curve
```

### S Channel Parameter Relationships

**Units_Over (X shift)**:

- Horizontal displacement from start to end
- Example: `Units_Over = 3` shifts 75mm to the right

**Units_Up (Y travel)**:

- Vertical displacement from start to end
- Example: `Units_Up = 4` travels 100mm forward

**Straight_Distance**:

- Straight sections before curve and after curve
- Default: 12.5mm (half grid unit)
- Increase for smoother entry/exit to I Channels
- Typical range: 12.5-25mm

### S Channel Configurations

#### Configuration 1: Gentle Desktop Shift

```openscad
// Shift cable run 50mm right, 100mm forward
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Units_Over = 2;              // 50mm horizontal shift
Units_Up = 4;                // 100mm forward travel
Straight_Distance = 25;      // 25mm straight before/after for I Channel connection
```

**Result**: Smooth S-curve, 50mm sideways shift over 100mm travel distance.

**Use for**: Routing around desk items, shifting to different desk zone.

#### Configuration 2: Long Gradual Transition

```openscad
// Long smooth curve for aesthetic cable routing
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Units_Over = 4;              // 100mm horizontal shift
Units_Up = 8;                // 200mm forward travel
Straight_Distance = 25;
```

**Result**: Very gentle curve, minimal cable stress, elegant appearance.

**Use for**: Visible cable runs (living room, office), where aesthetics matter.

#### Configuration 3: Tight Space Navigation

```openscad
// Navigate around obstacle in confined space
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Units_Over = 1;              // 25mm minimal shift
Units_Up = 2;                // 50mm travel
Straight_Distance = 12.5;    // Minimal straight section
```

**Result**: Tighter curve, still smoother than L Channel.

**Use for**: Tight spaces where L Channel too sharp but space limited.

## C Channel (Circular Arc)

### When to Use C Channel

**Use when:**

- Routing around circular obstacles (desk legs, poles, cylinders)
- Creating perfect arc turns (quarter circle, half circle, full circle)
- Need specific radius curve (not just smooth diagonal)
- Aesthetic circular cable routing

**Don't use when:**

- Need diagonal transition → Use S Channel
- Need 90° sharp corner → Use L Channel
- Need 45° angle → Use Mitre Channel

### C Channel Specific Parameters

```openscad
/*[Channel Shape]*/
Channel_Width_in_Units = 1;
Channel_Internal_Height = 12;
Arc_Radius_in_Units = 2;           // Radius of circular arc
Arc_Angle = 90;                    // Angle of arc (0-360 degrees)
```

**Arc_Radius_in_Units**:

- Controls curve tightness
- Smaller radius = tighter turn
- Larger radius = gentler curve
- Typical range: 2-6 units (50-150mm)

**Arc_Angle**:

- Quarter circle: 90°
- Half circle: 180°
- Three-quarter circle: 270°
- Full circle: 360° (closed loop)

### C Channel Arc Angle Guide

| Angle | Description | Use Case |
|-------|-------------|----------|
| 90° | Quarter circle | Standard corner replacement (softer than L) |
| 135° | Wide turn | Gradual direction change |
| 180° | Half circle | U-turn around obstacle |
| 270° | Three-quarter | Spiral routing |
| 360° | Full circle | Loop around pole/leg |

### C Channel Configurations

#### Configuration 1: Desk Leg Quarter Circle

```openscad
// Route around cylindrical desk leg (50mm radius)
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Arc_Radius_in_Units = 2;     // 50mm radius (clears desk leg + clearance)
Arc_Angle = 90;              // Quarter circle
```

**Result**: Clean 90° arc around desk leg, 50mm radius maintains clearance.

#### Configuration 2: Half Circle U-Turn

```openscad
// Complete 180° turn to reverse cable direction
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Arc_Radius_in_Units = 3;     // 75mm radius (gentle curve)
Arc_Angle = 180;             // Half circle
```

**Result**: Smooth U-turn, cables reverse direction without stress.

**Use for**: Routing back along same wall, creating cable loops.

#### Configuration 3: Full Circle Pole Wrap

```openscad
// Complete loop around central pole
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Arc_Radius_in_Units = 4;     // 100mm radius (pole diameter + clearance)
Arc_Angle = 360;             // Full circle
```

**Result**: Closed circular channel around pole.

**Use for**: Cable routing around support columns, aesthetic circular runs.

## Mitre Channel (45° Corner)

### When to Use Mitre Channel

**Use when:**

- Need sharper corner than S/C but softer than L (90°)
- Creating 45° angled cable routing
- Aesthetic preference for 45° chamfered look
- Space constraints prevent full L Channel

**Don't use when:**

- Need 90° corner → Use L Channel (cleaner)
- Need smooth curve → Use S or C Channel
- Need variable angle → Use S Channel with appropriate Units_Over/Up ratio

### Mitre Channel Specific Parameters

```openscad
/*[Channel Shape]*/
Channel_Width_in_Units = 1;
Channel_Internal_Height = 12;
Mitre_Type = "Inside";             // [Inside, Outside]
```

**Mitre_Type**:

- **Inside**: 45° corner on inside of turn (concave)
- **Outside**: 45° corner on outside of turn (convex)

**Geometry**:

```
Inside Mitre:           Outside Mitre:
    ┌─────                  ──┐
    │                          ╲
    │                           ╲
    └╲                           └─────
      ╲
       ───
```

### Mitre Channel Configurations

#### Configuration 1: Inside Corner (Standard)

```openscad
// 45° corner for desk edge routing (inside corner)
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Mitre_Type = "Inside";
```

**Use for**: Desk corners, wall corners (routing along inside edge).

#### Configuration 2: Outside Corner

```openscad
// 45° corner around obstacle (outside corner)
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Mitre_Type = "Outside";
```

**Use for**: Routing around protruding obstacles, external corners.

## Height Change Channel (Vertical Transition)

### When to Use Height Change Channel

**Use when:**

- Transitioning cables from wall to desk (vertical drop)
- Routing between different mounting heights
- Creating multi-level cable management systems
- Smooth Z-axis transitions (not just XY plane)

**Don't use when:**

- Only need horizontal routing → Use I, L, S, C channels
- Need simple 90° drop → Use L Channel rotated
- Need gentle vertical curve → Combine S Channel with vertical orientation

### Height Change Channel Specific Parameters

```openscad
/*[Channel Shape]*/
Channel_Width_in_Units = 1;
Channel_Internal_Height = 12;
Height_Change_Distance = 50;       // Vertical drop/rise (mm)
Horizontal_Span = 75;              // Horizontal distance during transition (mm)
```

**Parameter relationships**:

```
Angle = arctan(Height_Change_Distance / Horizontal_Span)
```

- Shallow angle: Large Horizontal_Span, small Height_Change
- Steep angle: Small Horizontal_Span, large Height_Change

### Height Change Channel Configurations

#### Configuration 1: Wall-to-Desk Drop

```openscad
// Transition from wall-mounted OpenGrid to desk surface
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Height_Change_Distance = 100;     // 100mm vertical drop
Horizontal_Span = 50;             // 50mm horizontal during drop
```

**Result**: Steep ~63° angle drop from wall to desk.

**Use for**: Bringing cables from wall-mounted board down to desk devices.

#### Configuration 2: Gradual Multi-Level Routing

```openscad
// Gentle slope between two shelf heights
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Height_Change_Distance = 150;     // 150mm rise
Horizontal_Span = 200;            // 200mm horizontal
```

**Result**: Gentle ~37° angle rise.

**Use for**: Connecting different shelf/desk levels, minimal cable stress.

## Curve/Transition Common Pitfalls

### Pitfall #1: S Channel Units Don't Match Destination

**Problem**: User wants to connect S Channel to I Channel 100mm away, code sets `Units_Up = 2` (50mm).

**Why it fails**: S Channel ends 50mm short of destination I Channel.

**Fix**: Calculate exact displacement:

```openscad
// Destination I Channel is 100mm forward, 75mm right
Units_Up = 4;    // 100mm ÷ 25mm = 4 units
Units_Over = 3;  // 75mm ÷ 25mm = 3 units
```

### Pitfall #2: C Channel Radius Too Small

**Problem**: User routing around 80mm diameter desk leg, code sets `Arc_Radius_in_Units = 2` (50mm radius).

**Why it fails**: 50mm radius < 40mm leg radius + clearance.

**Fix**: Add clearance to obstacle radius:

```openscad
// Desk leg diameter = 80mm → radius = 40mm
// Add 15mm clearance
// Total radius needed = 55mm
Arc_Radius_in_Units = 3;  // 75mm > 55mm ✓
```

### Pitfall #3: Height Change Too Steep

**Problem**: User wants 200mm drop in 50mm horizontal span (76° angle).

**Why it fails**: Cables can't bend that sharply - insulation damage, stress.

**Fix**: Increase horizontal span for gentler angle:

```openscad
// Target: <45° angle for most cables
Height_Change_Distance = 200;
Horizontal_Span = 200;        // Same distance = 45° angle
// Or larger span for even gentler:
Horizontal_Span = 300;        // 34° angle
```

**Rule of thumb**: Horizontal_Span ≥ Height_Change_Distance for safe cable bending.

### Pitfall #4: Wrong Mitre Type

**Problem**: Routing around outside desk corner, code uses `Mitre_Type = "Inside"`.

**Why it fails**: Inside mitre creates concave corner, doesn't wrap around convex obstacle.

**Fix**: Match mitre type to corner orientation:

```openscad
// Inside desk corner (routing along inside edge)
Mitre_Type = "Inside";  // Concave

// Outside desk corner (routing around outside edge)
Mitre_Type = "Outside";  // Convex
```

### Pitfall #5: S Channel Straight_Distance Too Short

**Problem**: Connecting S Channel to I Channel, `Straight_Distance = 0` causes misalignment.

**Why it fails**: No straight section for clean connection to adjacent channel.

**Fix**: Always use straight sections for connections:

```openscad
// Minimum for connections
Straight_Distance = 12.5;  // Half grid unit

// Better for clean transitions
Straight_Distance = 25;    // Full grid unit
```

## Curve/Transition Quality Checklist

**Before delivering curve/transition code:**

**S Channel validation:**

- ✓ `Units_Over` and `Units_Up` calculated to reach destination point
- ✓ `Straight_Distance` adequate for I Channel connections (12.5-25mm)
- ✓ Curve ratio (Units_Over/Units_Up) creates smooth path (avoid extreme ratios)
- ✓ Path doesn't create cable stress (gradual enough for cable bend radius)

**C Channel validation:**

- ✓ `Arc_Radius_in_Units` clears obstacles with margin (radius > obstacle + 10-15mm)
- ✓ `Arc_Angle` appropriate for routing need (90° quarter, 180° half, etc.)
- ✓ Radius not too tight for cable thickness (larger cables need larger radius)
- ✓ Full circle (360°) actually needed (vs. partial arc)

**Mitre Channel validation:**

- ✓ `Mitre_Type` matches corner orientation (Inside for concave, Outside for convex)
- ✓ 45° angle appropriate (not using when 90° L or smooth S/C better)
- ✓ Channel width accommodates cables through angled section

**Height Change validation:**

- ✓ Angle safe for cables: `arctan(Height_Change / Horizontal_Span) ≤ 45°` for most cables
- ✓ `Horizontal_Span ≥ Height_Change_Distance` (rule of thumb for gentle slope)
- ✓ Transition connects cleanly to horizontal I Channels at both ends
- ✓ Mounting method works for vertical/angled orientation

**Code compliance:**

- ✓ Complete module code copied from QuackWorks (specific curve channel file)
- ✓ Attribution comments intact
- ✓ BOSL2 includes present
- ✓ `Grid_Size = 25` unchanged

**User guidance:**

- ✓ Explained curve type selection rationale
- ✓ Documented radius/angle/distance choices with clearance reasoning
- ✓ Noted cable stress considerations (bend radius, angle limits)
- ✓ Provided connection guidance (how curve channels join to straight runs)
