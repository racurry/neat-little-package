# Straight Runs: I Channel

Reference for generating I Channel (straight cable runs with optional cord cutouts).

## QuackWorks Reference File

**Source**: `Underware_I_Channel.scad`

**Fetch from**: https://github.com/AndyLevesque/QuackWorks/blob/main/Underware/Underware_I_Channel.scad

## When to Use I Channel

**Use I Channel when:**

- Running cables horizontally along desk/wall
- Need straight path with periodic cable exits (power strips, device connections)
- Organizing multiple parallel cables in single channel
- Creating modular runs that connect with L/T/X channels at ends

**Don't use when:**

- Need to turn corner → Use L Channel instead
- Need multi-direction junction → Use T or X Channel
- Need smooth curve → Use S or C Channel
- Need vertical transition → Use Height Change Channel

## I Channel Specific Parameters

### Length Sizing

```openscad
/*[Channel Size]*/
Channel_Length_Units = 5;  // Length in grid units (25mm each)
```

**Decision guide:**

| Desk/wall distance | Units | Actual length | Mounting points      |
| ------------------ | ----- | ------------- | -------------------- |
| Small desk run     | 3     | 75mm          | 3 holes (1 per unit) |
| Medium run         | 5     | 125mm         | 5 holes              |
| Long wall run      | 10    | 250mm         | 10 holes             |
| Full desk width    | 20    | 500mm         | 20 holes             |

**Mounting point calculation**: Each grid unit (25mm) gets one mounting hole when using OpenGrid/Multiboard methods.

### Cord Cutout Parameters (Official Specification)

These parameters control cable exit points along the channel:

```openscad
/*[Cord Cutouts]*/
Number_of_Cord_Cutouts = 0;                    // How many exit slots
Cord_Side_Cutouts = "Both Sides";              // [Left Side, Right Side, Both Sides, None]
Cord_Cutout_Width = 12;                        // Width of each slot (mm)
Distance_Between_Cutouts = 25;                 // Spacing (mm, typically grid unit)
Shift_Cutouts_Forward_or_Back = 0;             // Offset along Y axis (mm)
```

**Parameter relationships:**

```
Total cutout span = (Number_of_Cord_Cutouts - 1) × Distance_Between_Cutouts
```

Example: 3 cutouts with 25mm spacing = 50mm span (fits in 3+ unit channel)

### Cord Cutout Decision Framework (Best Practices)

**Number_of_Cord_Cutouts:**

| Use case                      | Recommended count | Reasoning                            |
| ----------------------------- | ----------------- | ------------------------------------ |
| Single device (monitor, lamp) | 1                 | One exit point for power cable       |
| Power strip with 3-4 devices  | 3                 | Spaced exits for each device         |
| Full desk cable management    | 5-6               | Multiple workstations or devices     |
| No exits (through-run)        | 0                 | Cables stay in channel entire length |

**Cord_Side_Cutouts:**

| Scenario                      | Setting                         | Why                                      |
| ----------------------------- | ------------------------------- | ---------------------------------------- |
| Devices on both sides of desk | `"Both Sides"`                  | Cables exit left and right               |
| Wall-mounted (devices below)  | `"Both Sides"`                  | Maximum flexibility                      |
| Desk edge (devices one side)  | `"Left Side"` or `"Right Side"` | Cleaner look, less material removed      |
| Testing/unsure                | `"Both Sides"`                  | Can always route cables through one side |

**Cord_Cutout_Width:**

| Cable type                     | Recommended width | Notes                             |
| ------------------------------ | ----------------- | --------------------------------- |
| Thin cables (USB, audio)       | 8-10mm            | Snug fit, cable retention         |
| Standard power cables          | 12mm              | Default, fits most power cords    |
| Thick cables (extension cords) | 15-18mm           | Bulky connectors, multiple cables |
| Very thick bundles             | 20mm+             | Consider wider channel instead    |

**Distance_Between_Cutouts:**

- **25mm (1 grid unit)**: Standard, aligns with mounting holes
- **50mm (2 grid units)**: Widely spaced devices
- **12.5mm (half unit)**: Dense device placement (USB hubs)

**Shift_Cutouts_Forward_or_Back:**

- **0 (default)**: Cutouts centered in channel
- **Positive value**: Shifts cutouts forward (away from wall)
- **Negative value**: Shifts cutouts backward (toward wall)
- **Use when**: Device connectors don't align with standard spacing

### Common I Channel Configurations

#### Configuration 1: Desktop Power Strip Management

```openscad
// User has 4 devices spaced along 150mm desk run
Channel_Width_in_Units = 1;          // 25mm wide (sufficient for 3-4 power cables)
Channel_Internal_Height = 18;        // 18mm tall (standard power cord height)
Channel_Length_Units = 6;            // 150mm long

Number_of_Cord_Cutouts = 4;          // 4 device exit points
Cord_Side_Cutouts = "Both Sides";    // Devices on both sides of desk
Cord_Cutout_Width = 12;              // Standard power cable width
Distance_Between_Cutouts = 25;       // One exit per grid unit
```

**Result**: 6-unit channel with 4 evenly-spaced exits spanning 75mm (3 × 25mm spacing).

#### Configuration 2: Clean Wall Run (No Exits)

```openscad
// User routing cables along wall to corner L channel
Channel_Width_in_Units = 1;
Channel_Internal_Height = 12;        // Minimum height for thin cables
Channel_Length_Units = 8;            // 200mm run

Number_of_Cord_Cutouts = 0;          // No exits (through-run)
Cord_Side_Cutouts = "None";          // No cutouts needed
```

**Result**: Clean enclosed channel, cables run full length to connect with corner channel.

#### Configuration 3: High-Density USB Hub

```openscad
// User has USB hub with 7 ports in 100mm space
Channel_Width_in_Units = 1;
Channel_Internal_Height = 12;        // Thin USB cables
Channel_Length_Units = 4;            // 100mm

Number_of_Cord_Cutouts = 7;          // 7 USB devices
Cord_Side_Cutouts = "Both Sides";
Cord_Cutout_Width = 8;               // Thin USB cables
Distance_Between_Cutouts = 12.5;     // Half-unit spacing (dense)
```

**Result**: Compact channel with frequent exits for densely-packed USB connections.

#### Configuration 4: Wide Channel for Cable Bundle

```openscad
// User has 10+ cables running together (server rack, AV setup)
Channel_Width_in_Units = 2;          // 50mm wide (double width)
Channel_Internal_Height = 24;        // 24mm tall (large cable stack)
Channel_Length_Units = 10;           // 250mm run

Number_of_Cord_Cutouts = 3;          // Sparse exits for major branches
Cord_Side_Cutouts = "Both Sides";
Cord_Cutout_Width = 18;              // Wide slots for multiple cables
Distance_Between_Cutouts = 50;       // 2-unit spacing
```

**Result**: Large-capacity channel for server/AV cable bundles with occasional branch points.

## Code Generation Pattern for I Channel

### Step 1: Calculate Dimensions

```
User wants: "Cable management for 4 devices across 6 inches (150mm)"

Conversion:
- 150mm ÷ 25mm = 6 grid units → Channel_Length_Units = 6
- 4 devices → Number_of_Cord_Cutouts = 4
- Assume standard power cables → Cord_Cutout_Width = 12
```

### Step 2: Generate Complete Code

```openscad
/*Generated for desktop cable management (4 devices, 150mm run)
Based on QuackWorks Underware I Channel
Licensed CC BY-NC-SA 4.0

QuackWorks: https://github.com/AndyLevesque/QuackWorks/tree/main/Underware
Documentation: https://handsonkatie.com/underware-2-0-the-made-to-measure-collection/
*/

include <BOSL2/std.scad>
include <BOSL2/rounding.scad>
include <BOSL2/threading.scad>

/*[Choose Part]*/
Base_Top_or_Both = "Both"; // [Base, Top, Both]

/*[Channel Size]*/
Channel_Width_in_Units = 1;           // 25mm wide
Channel_Internal_Height = 18;         // 18mm tall (standard power cables)
Channel_Length_Units = 6;             // 150mm long (6 × 25mm)

/*[Mounting Options]*/
Mounting_Method = "Threaded Snap Connector"; // For OpenGrid boards
Magnet_Diameter = 4.0;
Magnet_Thickness = 1.5;
Magnet_Tolerance = 0.1;
Wood_Screw_Thread_Diameter = 3.5;
Wood_Screw_Head_Diameter = 7;
Wood_Screw_Head_Height = 1.75;

/*[Cord Cutouts]*/
Number_of_Cord_Cutouts = 4;           // 4 device exit points
Cord_Side_Cutouts = "Both Sides";     // Devices on both sides
Cord_Cutout_Width = 12;               // Standard power cable width
Distance_Between_Cutouts = 25;        // One per grid unit
Shift_Cutouts_Forward_or_Back = 0;    // Centered

/*[Advanced Options]*/
Grid_Size = 25;                       // OpenGrid standard (DO NOT CHANGE)
Global_Color = "SlateBlue";
Profile_Type = "Original";
Flex_Compensation_Scaling = 0.99;
Additional_Holding_Strength = 0.0;
Slop = 0.075;

// ... [Include complete I Channel module code from QuackWorks]
// DO NOT write modules from scratch - copy from Underware_I_Channel.scad
```

### Step 3: Explain to User

**Provide this context:**

```
Generated I Channel for your desktop cable management:

Dimensions:
- 6 grid units (150mm) long
- 1 unit (25mm) wide
- 18mm internal height (fits standard power cables)

Cord exits:
- 4 cutouts spaced every 25mm (one per grid unit)
- 12mm wide slots (standard power cable size)
- Both sides enabled (devices can be on either side)

Mounting:
- Threaded snap connectors for OpenGrid/Multiboard
- 6 mounting points (one per unit)

Print settings:
- Export both Base and Top
- Base prints flat (face-down)
- Top prints upside-down (clip features up)
- No supports needed

Assembly:
- Mount base to OpenGrid board with snap connectors
- Route cables through channel
- Snap top onto base (clips lock with satisfying click)
```

## Common I Channel Pitfalls

### Pitfall #1: Cutouts Exceed Channel Length

**Problem**: User wants 8 cutouts with 25mm spacing in 4-unit channel.

```
8 cutouts × 25mm spacing = 175mm span
4-unit channel = 100mm long
❌ Cutouts don't fit
```

**Fix**: Reduce spacing or increase channel length:

```openscad
// Option 1: Reduce spacing
Number_of_Cord_Cutouts = 8;
Distance_Between_Cutouts = 12.5;     // 8 × 12.5 = 87.5mm (fits in 100mm)

// Option 2: Increase length
Channel_Length_Units = 7;            // 175mm (8 × 25 = 175mm fits)
Number_of_Cord_Cutouts = 8;
Distance_Between_Cutouts = 25;
```

### Pitfall #2: Internal Height Too Small for Cables

**Problem**: Code sets `Channel_Internal_Height = 12` for thick power cables.

**Why it fails**: 12mm is minimum height. Standard power cables are ~8mm diameter but need clearance for bending radius.

**Fix**: Use appropriate height:

```openscad
// Thin cables (USB, audio)
Channel_Internal_Height = 12;  // Minimum

// Standard power cables
Channel_Internal_Height = 18;  // Recommended

// Thick cables or bundles
Channel_Internal_Height = 24;  // Extra clearance
```

### Pitfall #3: Wrong Cutout Width for Cable Type

**Problem**: User has thick extension cord, code uses `Cord_Cutout_Width = 8`.

**Why it fails**: 8mm slot too narrow for bulky connector/plug.

**Fix**: Size cutouts to cable:

```openscad
// Match cutout width to thickest connector (not cable diameter)
Cord_Cutout_Width = 18;  // Extension cord plug width
```

### Pitfall #4: Forgetting Mounting Alignment

**Problem**: Cutouts placed at arbitrary positions, don't align with grid.

**Fix**: Use grid-aligned spacing:

```openscad
// Good: 25mm spacing aligns with grid and mounting holes
Distance_Between_Cutouts = 25;

// Acceptable: Half-unit spacing (12.5mm) for dense layouts
Distance_Between_Cutouts = 12.5;

// Avoid: Random spacing (breaks grid alignment)
// Distance_Between_Cutouts = 37;  ❌ Doesn't align to grid
```

## I Channel Quality Checklist

**Before delivering I Channel code:**

**Dimensional validation:**

- ✓ `Channel_Length_Units` sufficient for cutout span
- ✓ Calculate: `(Number_of_Cord_Cutouts - 1) × Distance_Between_Cutouts ≤ Channel_Length_Units × 25 - 25`
- ✓ `Channel_Internal_Height` appropriate for cable thickness (12mm min, 18mm standard, 24mm+ for bundles)
- ✓ `Cord_Cutout_Width` sized to thickest connector (not just cable diameter)

**Cutout configuration:**

- ✓ `Number_of_Cord_Cutouts` matches user's device count
- ✓ `Cord_Side_Cutouts` appropriate for device placement (both sides unless specific need)
- ✓ `Distance_Between_Cutouts` aligns to grid (25mm or 12.5mm increments)
- ✓ `Shift_Cutouts_Forward_or_Back = 0` unless user has specific offset need

**Code compliance:**

- ✓ Complete module code copied from QuackWorks (not written from scratch)
- ✓ Attribution comments intact
- ✓ BOSL2 includes present
- ✓ `Grid_Size = 25` unchanged

**User guidance:**

- ✓ Explained dimension choices (unit conversion from mm)
- ✓ Documented cutout configuration rationale
- ✓ Provided print orientation instructions
- ✓ Noted mounting point count (one per unit)
