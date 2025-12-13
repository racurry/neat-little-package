# Corners and Junctions: L, T, X, Y Channels

Reference for generating corner turns and multi-path junction channels.

## QuackWorks Reference Files

**Source files:**

- L Channel: `Underware_L_Channel.scad`
- T Channel: `Underware_T_Channel.scad`
- X Channel: `Underware_X_Channel.scad`
- Y Channel (Branch Split): `Underware_Branch_Split_Channel.scad`

**Fetch from**: https://github.com/AndyLevesque/QuackWorks/tree/main/Underware

## Channel Selection by Junction Type

| Junction Need      | Channel   | Outputs                                  | Use Case                |
| ------------------ | --------- | ---------------------------------------- | ----------------------- |
| 90° corner turn    | L Channel | 2 perpendicular                          | Desk edge, wall corner  |
| 3-way intersection | T Channel | 3 directions (1 inline, 2 perpendicular) | Main run with branch    |
| 4-way crossroads   | X Channel | 4 directions (2 perpendicular pairs)     | Cable grid intersection |
| Split 1 to 2       | Y Channel | 1 input, 2 angled outputs                | Branch to dual monitors |

## L Channel (90° Corner)

### When to Use L Channel

**Use when:**

- Turning cable run 90° around desk edge
- Routing from horizontal wall run to vertical drop
- Connecting two perpendicular I Channel runs
- Need independent arm lengths (asymmetric corner)

**Don't use when:**

- Need smooth curve → Use C Channel (quarter circle)
- Need 45° turn → Use Mitre Channel
- Need 3+ way junction → Use T or X Channel

### L Channel Specific Parameters

```openscad
/*[Channel Size]*/
Channel_Width_in_Units = 1;                    // Cross-section width
Channel_Internal_Height = 12;                  // Interior height
L_Channel_Length_in_Units_Y_Axis = 1;          // Arm extending along Y axis
L_Channel_Length_in_Units_X_Axis = 1;          // Arm extending along X axis
```

**Critical understanding**: Y and X axis lengths are **independent**. This allows asymmetric corners:

```
Y_Axis = 2, X_Axis = 4 creates:
    │ 2 units (50mm)
    │
    └────────── 4 units (100mm)
```

### L Channel Configurations

#### Configuration 1: Symmetric Desk Corner

```openscad
// Equal arms for standard desk corner turn
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
L_Channel_Length_in_Units_Y_Axis = 2;  // 50mm arm
L_Channel_Length_in_Units_X_Axis = 2;  // 50mm arm
```

**Result**: Balanced 90° turn, 50mm reach on both sides of corner.

#### Configuration 2: Long Wall to Short Drop

```openscad
// Long horizontal run, short vertical drop to device
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
L_Channel_Length_in_Units_Y_Axis = 5;  // 125mm horizontal
L_Channel_Length_in_Units_X_Axis = 1;  // 25mm vertical drop
```

**Result**: Asymmetric L, long horizontal span connects to I Channel, short drop to device below.

### L Channel Mounting Points

**Grid coverage calculation**:

```
Total grid cells = (Y_units + Width_units) × (X_units + Width_units)
Mounting points = grid cells within footprint
```

Example: Y=2, X=2, Width=1 → (2+1) × (2+1) = 9 grid cells → up to 9 mounting points.

## T Channel (3-Way Intersection)

### When to Use T Channel

**Use when:**

- Main cable run needs perpendicular branch
- Creating backbone with side exits
- Connecting 3 I Channel segments (straight + two sides)
- Need 180° inline path + 90° branch

**Don't use when:**

- Only need 90° corner → Use L Channel (simpler, less material)
- Need 4-way → Use X Channel
- Need angled split → Use Y Channel

### T Channel Specific Parameters

```openscad
/*[Channel Height and Width]*/
Channel_Width_in_Units = 1;
Channel_Internal_Height = 12;
Corner_Style = "Sharp"; // [Sharp, Mitered]
```

**Corner_Style decision:**

- **Sharp**: 90° corners, minimal space, works for thin cables
- **Mitered**: 45° chamfered corners, smoother cable routing for thick/stiff cables

### T Channel Geometry

**Fixed geometry**: T Channel is 1 grid unit wide × 2 grid units long (3-cell footprint):

```
        ┌─┐
        │ │  ← 1 unit side branch
        │ │
    ┌───┴─┴───┐
    │         │  ← 2 unit inline run (1 unit each side of center)
    └─────────┘
```

**Mounting**: 3 grid cells (center + two inline) for standard mounts.

### T Channel Configurations

#### Configuration 1: Standard T (Sharp Corners)

```openscad
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Corner_Style = "Sharp";
Mounting_Method = "Threaded Snap Connector";
```

**Use for**: Standard power cables, USB cables (flexible routing).

#### Configuration 2: Mitered T (Smooth Routing)

```openscad
Channel_Width_in_Units = 1;
Channel_Internal_Height = 24;           // Taller for thick cables
Corner_Style = "Mitered";               // 45° corners
Mounting_Method = "Threaded Snap Connector";
```

**Use for**: Thick/stiff cables (HDMI, DisplayPort, coax), cable bundles.

**Why mitered helps**: 45° chamfer provides gradual turn radius, reduces cable stress at sharp 90° corners.

## X Channel (4-Way Crossroads)

### When to Use X Channel

**Use when:**

- Creating cable grid intersection (perpendicular cable runs cross)
- Central hub for 4-direction routing
- Modular cable runway system (multiple X channels form grid)

**Don't use when:**

- Only need 3-way → Use T Channel (less material)
- Only need 2-way corner → Use L Channel
- Need different arm lengths → Use multiple T or L channels

### X Channel Geometry

**Fixed geometry**: X Channel is cross-shaped, 1 unit arms in all 4 cardinal directions:

```
        ┌─┐
        │ │  ← North
        │ │
    ┌───┼─┼───┐
    │   │ │   │  ← West & East
    └───┼─┼───┘
        │ │
        │ │  ← South
        └─┘
```

**Mounting**: 5 grid cells (center + 4 cardinal) for standard mounts.

### X Channel Configuration

```openscad
Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Mounting_Method = "Threaded Snap Connector";
```

**Parameters**: X Channel has minimal customization - primarily width and height. All arms are 1 unit long.

**Advanced use**: Connect multiple X Channels with I Channels to create modular cable grid:

```
X─I─X─I─X
│   │   │
I   I   I
│   │   │
X─I─X─I─X
```

## Y Channel (Branch Split)

### When to Use Y Channel

**Use when:**

- Splitting one cable run to two destinations (dual monitors, paired devices)
- Creating bifurcation from main run
- Need smooth diagonal transitions (not sharp 90° like T Channel)

**Don't use when:**

- Need 90° branches → Use T Channel (sharper, more compact)
- Need 3+ outputs → Use multiple Y or T channels
- Need single corner → Use L Channel

### Y Channel Specific Parameters

```openscad
/*[Channel Shape]*/
Straight_Channel_Width_in_Units = 1;      // Input section width
Straight_Section_Length_in_Units = 4;     // Input straight section length
Branch_Channel_Width_in_Units = 1;        // Output branch width
Channel_Internal_Height = 12;
Branch_Units_Out = 1;                     // Horizontal spread (X axis)
Branch_Units_Up = 1;                      // Vertical travel (Y axis)
Branch_Units_Extra_Length = 0;            // Additional straight after split
Y_Output_Direction = "Forward";           // [Forward, Turn]
```

**Critical parameters:**

- **Branch_Units_Out**: How far branches move sideways (left/right from center)
- **Branch_Units_Up**: How far branches move forward (along main cable run direction)
- **Y_Output_Direction**: "Forward" keeps branches same direction, "Turn" rotates 90°

### Y Channel Output Direction Modes

#### Forward Mode (Default)

**Geometry**:

```
        Input
          │
          │  Straight_Section_Length
          │
        ┌─┴─┐
       ╱     ╲
      ╱       ╲  Branch_Units_Up
     ╱         ╲
  Left       Right
  Output     Output
    ↓          ↓
```

**Use for**: Dual monitors side-by-side, paired devices in front of main run.

```openscad
Y_Output_Direction = "Forward";
Branch_Units_Out = 2;    // 50mm horizontal spread
Branch_Units_Up = 3;     // 75mm forward travel
```

**Result**: Branches angle outward and forward, outputs point same direction as input.

#### Turn Mode (90° Outputs)

**Geometry**:

```
        Input
          │
          │
          │
        ┌─┴─┐
       ╱     ╲
      ╱       ╲
     →         ←  Outputs perpendicular
```

**Use for**: Routing to devices on sides of desk, perpendicular device placement.

```openscad
Y_Output_Direction = "Turn";
Branch_Units_Out = 2;    // How far to sides
Branch_Units_Up = 2;     // Forward travel before turn
```

**Result**: Branches turn 90° at ends, outputs perpendicular to input direction.

### Y Channel Configurations

#### Configuration 1: Dual Monitor Split (Forward)

```openscad
// Split one cable run to two side-by-side monitors
Straight_Channel_Width_in_Units = 1;
Straight_Section_Length_in_Units = 4;   // 100mm straight input
Branch_Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;           // HDMI/DisplayPort cables
Branch_Units_Out = 2;                   // 50mm horizontal spread
Branch_Units_Up = 3;                    // 75mm forward to monitors
Branch_Units_Extra_Length = 1;          // 25mm extra reach
Y_Output_Direction = "Forward";
```

**Result**: Smooth Y-split, outputs spread 100mm apart (2 units × 2 = 50mm each side), 100mm forward travel to monitors.

#### Configuration 2: Desk Edge Side Routing (Turn)

```openscad
// Route from desk center to devices on left/right edges
Straight_Channel_Width_in_Units = 1;
Straight_Section_Length_in_Units = 3;   // 75mm input
Branch_Channel_Width_in_Units = 1;
Channel_Internal_Height = 18;
Branch_Units_Out = 3;                   // 75mm to each side
Branch_Units_Up = 2;                    // 50mm forward before turn
Y_Output_Direction = "Turn";
```

**Result**: Branches travel 50mm forward, then turn 90° toward desk edges, reaching 75mm left/right.

## Common Corner/Junction Pitfalls

### Pitfall #1: Using T Channel for Simple Corner

**Problem**: User needs 90° desk corner, code generates T Channel.

**Why it fails**: T Channel has 3 outputs (1 unused), wastes material and mounting space.

**Fix**: Use L Channel for 2-way corners:

```openscad
// ❌ Overengineered
// T Channel for 2-way corner (third output unused)

// ✓ Correct
L_Channel_Length_in_Units_Y_Axis = 2;
L_Channel_Length_in_Units_X_Axis = 2;
// Simple, efficient corner
```

### Pitfall #2: Asymmetric L Channel Confusion

**Problem**: Code sets equal Y and X lengths when user needs asymmetric corner.

**Why it fails**: User said "long wall run to short drop" but got equal 50mm arms.

**Fix**: Listen for length differences:

```openscad
// User: "3 feet horizontal, 6 inches down"
L_Channel_Length_in_Units_Y_Axis = 36;  // ~900mm (3 ft)
L_Channel_Length_in_Units_X_Axis = 6;   // ~150mm (6 in)
```

### Pitfall #3: Wrong Y Channel Output Direction

**Problem**: User wants side-by-side monitors, code uses `Y_Output_Direction = "Turn"`.

**Why it fails**: Turn mode rotates outputs 90°, cables exit perpendicular instead of forward.

**Fix**: Match output direction to device layout:

```openscad
// Side-by-side devices (same direction as input)
Y_Output_Direction = "Forward";

// Devices perpendicular to input (left/right sides)
Y_Output_Direction = "Turn";
```

### Pitfall #4: Insufficient Branch Spread

**Problem**: User has monitors 400mm apart, code sets `Branch_Units_Out = 1` (25mm spread).

**Why it fails**: 25mm × 2 = 50mm total spread, monitors are 400mm apart.

**Fix**: Calculate required spread:

```
Monitor separation = 400mm
Required spread per side = 200mm
Branch_Units_Out = 200mm ÷ 25mm = 8 units
```

```openscad
Branch_Units_Out = 8;  // 200mm each side = 400mm total
```

### Pitfall #5: Forgetting Mitered Corners for Thick Cables

**Problem**: User routing thick HDMI cables through T Channel, code uses `Corner_Style = "Sharp"`.

**Why it fails**: Sharp 90° corners stress thick/stiff cables, may crack cable insulation over time.

**Fix**: Use mitered corners for thick/stiff cables:

```openscad
// Thick cables (HDMI, DisplayPort, coax)
Corner_Style = "Mitered";
Channel_Internal_Height = 24;  // Extra height for bend radius
```

## Corner/Junction Quality Checklist

**Before delivering corner/junction code:**

**Channel selection:**

- ✓ L Channel for 2-way 90° corners (not T Channel)
- ✓ T Channel for 3-way junctions (1 inline + 2 perpendicular)
- ✓ X Channel for 4-way crossroads (not multiple T channels)
- ✓ Y Channel for smooth splits (not sharp T Channel branches)

**L Channel validation:**

- ✓ Y_Axis and X_Axis lengths match user's asymmetric needs (if any)
- ✓ Mounting footprint calculated (Y+Width) × (X+Width) grid cells
- ✓ Both arms long enough to connect to adjacent I Channels

**T/X Channel validation:**

- ✓ Corner_Style appropriate for cable thickness (Sharp for thin, Mitered for thick)
- ✓ Channel height sufficient for bend radius (18mm standard, 24mm+ for thick)
- ✓ Mounting method works with fixed geometry (can't adjust arm lengths)

**Y Channel validation:**

- ✓ `Y_Output_Direction` matches device layout (Forward for same direction, Turn for perpendicular)
- ✓ `Branch_Units_Out` provides sufficient horizontal spread for device separation
- ✓ `Branch_Units_Up` reaches far enough forward to device positions
- ✓ `Straight_Section_Length_in_Units` allows smooth transition (minimum 3-4 units)

**Code compliance:**

- ✓ Complete module code copied from QuackWorks (specific channel file)
- ✓ Attribution comments intact
- ✓ BOSL2 includes present
- ✓ `Grid_Size = 25` unchanged

**User guidance:**

- ✓ Explained channel type selection rationale
- ✓ Documented arm length/spread choices
- ✓ Noted corner style (sharp vs mitered) reasoning
- ✓ Provided assembly guidance (how channels connect)
