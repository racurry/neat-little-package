---
name: opengrid-openscad
description: Interpretive guidance for generating OpenSCAD code for OpenGrid/MultiConnect wall-mounted organizers. Provides pattern selection frameworks, mounting system integration, and dimensional constraints specific to this ecosystem. Use when generating OpenSCAD files for OpenGrid items.
---

# OpenGrid OpenSCAD Code Generation

Generates OpenSCAD code for wall-mounted storage items compatible with OpenGrid boards (28mm grid) and MultiConnect mounting system.

## Required Reading Before Generating Code

**Official specifications:**

- **OpenGrid Spec**: 28mm grid spacing standard
- **MultiConnect Mounting**: Slotted backplate system using `multiconnectBack()` module (see ./common_items/backplate_mount.md)

**Pattern references** (read as needed):

- ./common_items/*.md - Full OpenSCAD modules for each pattern
- ./enhancements.md - Optional feature modules

## Core Understanding (Critical Architecture)

### What Makes OpenGrid Different From Generic 3D Modeling

**Grid constraint**: All items must align to 28mm grid. This affects:

- Mounting backplate width (multiples of 28mm via `distanceBetweenSlots=28`)
- Horizontal dimensions should consider grid alignment for aesthetic consistency
- Vertical dimensions are unconstrained

**MultiConnect mounting system**: Items don't attach directly to wall. They:

1. Have slotted backplate created by `multiconnectBack(width, height, 28)`
2. Slide onto MultiConnect connectors mounted to OpenGrid board
3. Can be repositioned without tools

**Critical parameter relationships**:

```openscad
// These are interdependent:
backWidth = internal_width + wall_thickness*2;  // Total object width
slotCount = floor(backWidth/28);                // Number of connectors
actual_slots = max(1, slotCount);               // Minimum 1 slot
```

**Why this matters**: User requests "50mm wide bin" but code must account for walls, ensure at least one mounting slot, and ideally align to grid aesthetically.

## Pattern Selection Framework (Decision Layer)

### When User Requests Storage

Use this decision tree to select pattern:

| User wants to store | Primary pattern | Alternative | Read module |
|---------------------|----------------|-------------|-------------|
| Small hardware (screws, bits) | Basic Bin | Shallow Tray (if flat) | basic_bin.md |
| Writing tools (pens, markers) | Vertical Holder | Basic Bin (if few items) | vertical_holder.md |
| Hand tools (screwdrivers, pliers) | Tool Holder with Hooks | Hook Array (if lightweight) | tool_holder_with_hooks.md |
| Bottles, spray cans | Basic Bin (deep) | Angled Storage (if visibility needed) | basic_bin.md, angled_storage.md |
| Mixed items in sections | Divided Bin | Multiple basic bins | divided_bin.md |
| Light shelving needs | Shelf Bracket | N/A | shelf_bracket.md |
| Easy-access items (cables, tape) | Open Basket | Basic Bin with finger scoop | open_basket.md |
| Keys, lightweight hangables | Hook Array | Tool Holder | hook_array.md |

### When Pattern Is Unclear

**Ask these questions:**

1. **Access pattern**: Top access (bin), side access (basket), or hanging (hooks)?
2. **Item orientation**: Vertical storage or horizontal?
3. **Item count**: Single type or mixed organization?
4. **Visibility**: Need to see contents from front?

**Default**: When unclear, use Basic Bin - most versatile, user can refine.

## Code Generation Best Practices

### Parameter Organization

**Always declare these parameters** at top of file:

```openscad
// User-facing dimensions (what they care about)
internal_width = 80;    // Interior space for items
internal_depth = 60;
internal_height = 60;

// Structural parameters (print quality)
wall_thickness = 2.5;   // 2.5-3mm for PETG/PLA
base_thickness = 2.5;

// Mounting parameters (OpenGrid specific)
distanceBetweenSlots = 28;  // ALWAYS 28 for OpenGrid
```

**Why this order**: User dimensions first (what they specified), then structural (printer constraints), then ecosystem constants.

### Mounting Integration Pattern

**Every item needs mounting**. Standard integration:

```openscad
union() {
    // Your item (bin, holder, etc.)
    basic_bin();  // or other pattern

    // MultiConnect backplate
    translate([0, 0, 0])
        multiconnectBack(
            backWidth = internal_width + wall_thickness*2,
            backHeight = internal_height + 20,  // Extend above for strength
            distanceBetweenSlots = 28           // Always 28
        );
}
```

**Common mistake**: Forgetting to extend backplate above item for structural strength. Backplate should be ~20mm taller than internal_height.

### Dimensional Reasoning

**When user says "I need a bin for X"**:

1. **Estimate internal dimensions** for their items:
   - Small screws/bits: 50×40×40mm internal
   - Markers/pens vertical: 15mm diameter × 70mm deep
   - Screwdrivers horizontal: 60mm hook length
   - Spray cans: 80×80×120mm internal

2. **Calculate total dimensions**:

   ```openscad
   total_width = internal_width + wall_thickness*2;
   total_depth = internal_depth + wall_thickness;
   total_height = internal_height;  // No top wall on bins
   ```

3. **Check grid alignment** (optional but aesthetic):
   - Is total_width close to 28mm multiple? (28, 56, 84, 112mm)
   - If yes, mention to user as "this will align nicely to grid"
   - If no, not critical - mounting still works

### Pattern Module Integration

**Read the module file, don't reinvent**. Each pattern has complete module in ./common_items/:

```openscad
// DON'T write basic_bin() from scratch
// DO read ./common_items/basic_bin.md and use/adapt the module

include <path/to/modules.scad>  // If organized
// OR paste module directly (user preference)

basic_bin();  // Call the module
```

**When to adapt vs use as-is**:

- **Use as-is**: Pattern matches user need exactly
- **Adapt dimensions**: User needs different size (pass parameters)
- **Enhance**: User wants label recess, drainage, etc. (use ./enhancements.md)
- **Hybrid**: Combine patterns (divided_bin calls basic_bin)

## Enhancement Integration (When Requested)

**Only add enhancements if**:

1. User explicitly requests (e.g., "with drainage holes")
2. Use case clearly requires (e.g., spray bottle storage → drainage likely helpful)
3. You ask and confirm

**Available enhancements** (see ./enhancements.md for modules):

- **Label recess**: Angled cutout on front for labels (no support needed)
- **Drainage holes**: Grid of holes in floor for wet items
- **Rounded corners**: Hull-based smoothing for cleaning ease
- **Finger scoop**: Cylindrical cutout in front wall for access

**Integration pattern**:

```openscad
difference() {
    basic_bin();           // Base pattern

    // Enhancement as subtraction
    translate([...])
        label_recess(width=40, height=10);
}
```

## Common Pitfalls

### Pitfall #1: Insufficient Mounting Slots

**Problem**: User requests 40mm wide bin, code generates backWidth=45mm (40 + 2.5×2), results in floor(45/28)=1 slot. Bin is wider than one grid space but only has one connector - looks odd and may be unstable.

**Why it fails**: Didn't consider aesthetic/structural mismatch between item width and mounting points.

**Better approach**:

```openscad
// Either: Adjust dimensions to align to grid
internal_width = 51;  // 51 + 5 = 56mm = 2 grid spaces = 2 slots

// Or: Accept 1 slot but mention to user
echo("Note: 45mm width uses 1 mounting slot. For 2 slots, increase width to ~51mm");
```

### Pitfall #2: Forgetting Clearances

**Problem**: User wants vertical holder for 12mm pens, code uses `cylinder(d=12)`, pens don't fit.

**Why it fails**: No clearance for print tolerance and item variation.

**Better approach**:

```openscad
item_diameter = 12;
clearance = 1;  // 0.5mm per side
cylinder(d = item_diameter + clearance, $fn=40);
```

### Pitfall #3: Hardcoding Instead of Parameterizing

**Problem**: Module has magic numbers scattered throughout instead of calculated values.

**Why it fails**: User can't easily adjust; values get out of sync.

**Better approach**:

```openscad
// DON'T:
cube([82.5, 62.5, 60]);  // What are these numbers?

// DO:
cube([
    internal_width + wall_thickness*2,
    internal_depth + wall_thickness,
    internal_height
]);
```

### Pitfall #4: Overcomplicating Simple Requests

**Problem**: User wants basic bin, code generates elaborate parametric system with 15 parameters.

**Why it fails**: User just wanted a bin. Over-engineering delays delivery.

**Better approach**: Start simple, add complexity only when requested:

```openscad
// First iteration: Basic bin with hardcoded dimensions
internal_width = 80;
// ...

// Later if user wants variants: Parameterize
module customizable_bin(width=80, depth=60, height=60) { ... }
```

## Quality Checklist

**Before delivering OpenSCAD code:**

**Required elements:**

- ✓ Parameters clearly defined (internal dimensions, wall thickness, mounting parameters)
- ✓ MultiConnect backplate integrated via `multiconnectBack()`
- ✓ `distanceBetweenSlots = 28` (never other value)
- ✓ Clearances added where items fit into holes/slots
- ✓ Comments explain key calculations (slot count, dimensions)

**Pattern compliance:**

- ✓ Used appropriate pattern from decision framework
- ✓ Read module from ./common_items/ (didn't reinvent from scratch)
- ✓ Enhancements only included if requested/clearly needed

**Dimensional sanity:**

- ✓ Internal dimensions match user's items
- ✓ Total width accounts for walls: `internal + wall_thickness*2`
- ✓ Backplate height extends ~20mm above item for strength
- ✓ At least 1 mounting slot: `floor(backWidth/28) >= 1`

**Code quality:**

- ✓ Parameterized (no magic numbers)
- ✓ Clear variable names (internal_width not iw)
- ✓ Module structure (reusable components)
- ✓ `$fn` specified for cylinders/curves (e.g., `$fn=40`)

**User communication:**

- ✓ Explained pattern choice
- ✓ Stated assumed dimensions if user was vague
- ✓ Noted grid alignment if relevant
- ✓ Mentioned enhancements if applicable to use case

## Module Reference Structure

**Pattern modules** are organized as:

```
./common_items/
├── backplate_mount.md     - multiconnectBack() module (ALWAYS needed)
├── basic_bin.md           - Open-top bin (most common)
├── vertical_holder.md     - Cylindrical holes for pens/bits/etc.
├── tool_holder_with_hooks.md - Horizontal cantilever hooks
├── divided_bin.md         - Bin with internal dividers
├── shallow_tray.md        - Low-profile bin variant
├── shelf_bracket.md       - Triangular shelf support
├── open_basket.md         - Bin without front wall
├── angled_storage.md      - Forward-tilting bin
└── hook_array.md          - Simple hook row

./enhancements.md          - Optional features (labels, drainage, etc.)
```

**Workflow**:

1. Use decision framework to select pattern
2. Read selected pattern's .md file
3. Adapt dimensions to user's needs
4. Integrate multiconnectBack() mounting
5. Add enhancements if requested
6. Validate with checklist

## Documentation References

**OpenGrid Ecosystem**:

- OpenGrid: 28mm grid system for wall organization
- MultiConnect: Slotted mounting system (tool-free repositioning)
- This skill focuses on CODE GENERATION for these systems

**Related skills**:

- home-organization/SKILL.md - When to use OpenGrid vs other systems (NOT code generation)
- For system selection guidance, defer to that skill
- This skill is only for "generate OpenSCAD code for OpenGrid items"
