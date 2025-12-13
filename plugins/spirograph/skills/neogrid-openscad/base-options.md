# Base System Options

NeoGrid connectors support four base attachment systems. Choose based on drawer setup and repositioning needs.

## Base Selection Decision Tree

```
What's in your drawer currently?
├─ Gridfinity baseplate
│  └─ Use: Selected_Base = "Gridfinity"
│     - Snaps into existing baseplate
│     - Easy repositioning
│     - Grid alignment built-in
│
├─ openGrid board (wall-mounted, rare for drawers)
│  └─ Use: Selected_Base = "openGrid"
│     - For vertical/wall applications
│     - 25mm grid spacing
│     - Full or Lite profile
│
├─ Empty drawer (no existing system)
│  ├─ Plan to add Gridfinity later?
│  │  └─ Use: Selected_Base = "Gridfinity" (future-proof)
│  │
│  └─ No plans for modular system
│     ├─ Want to reposition connectors?
│     │  └─ Use: Selected_Base = "Flat" + adhesive pads
│     │
│     └─ Permanent install
│        └─ Use: Selected_Base = "None" (minimal filament)
```

## Gridfinity Base

**Official 42mm grid system** for desktop/drawer organization.

### When to Use

- Existing Gridfinity baseplate in drawer
- Want easy repositioning without re-taping
- Future-proofing for modular system
- Precise grid alignment desired

### Parameters

```openscad
Selected_Base = "Gridfinity";
grid_size = 42;              // Auto-set (don't override)
grid_x = 1;                  // Tiles horizontally (1 = 42mm)
grid_y = 1;                  // Tiles vertically (1 = 42mm)
Added_Base_Thickness = 1;    // Extra base height (mm)
```

### Multi-Tile Support

**X Intersection only** (currently):

```openscad
// 2×3 tile base (84mm × 126mm)
grid_x = 2;
grid_y = 3;

// Connector spans multiple grid squares
// Useful for large drawer divider systems
```

**Other connectors**: Limited to 1×1 tile (42mm × 42mm base).

### Base Profile

**Z-shaped socket profile**:

- Height: ~4.75mm + Added_Base_Thickness
- Locks into Gridfinity baseplate sockets
- Allows repositioning by lifting connector

**Gridfinity baseplate required**:

- Purchase separately or 3D print
- Standard 42mm × 42mm grid
- Verify compatibility (genuine Gridfinity spec)

### Advantages

- **Repositionable**: Lift and move without tools
- **Aligned**: Grid ensures straight divider runs
- **Modular**: Mix with Gridfinity bins in same drawer
- **Standard**: Compatible with entire Gridfinity ecosystem

### Limitations

- **Requires baseplate**: Additional cost/print time
- **Height**: Adds ~5mm to drawer bottom
- **Grid constrained**: Connectors align to 42mm grid

### Example Use Case

**Mixed organization drawer**:

- Front half: Small Gridfinity bins (screws, bits)
- Back half: NeoGrid dividers (larger tools)
- Both systems snap to same Gridfinity baseplate
- Reconfigure layout as needs change

## openGrid Base

**25mm grid system** primarily for wall-mounted organization.

### When to Use

- Vertical/wall mounting (unusual for drawers)
- Existing openGrid board
- 25mm grid alignment needed

### Parameters

```openscad
Selected_Base = "openGrid";
grid_size = 25;                          // Auto-set
openGrid_Full_or_Lite = "Lite";          // Full | Lite
openGrid_Directional_Snap = false;        // Vertical mounting support
openGrid_Directional_Snap_Orientation = 1; // 1-4 (rotation)
```

### Profile Variants

**Lite** (3.4mm height):

- Lower profile
- Adequate for drawer use
- Less filament

**Full** (6.8mm height):

- Stronger engagement
- Better for vertical mounting
- More filament

### Directional Snaps

**For vertical mounting**:

- `openGrid_Directional_Snap = true;`
- Adds extra snap features for downward force resistance
- Orientation: 1-4 (rotates directional features)
- Arrow on bottom indicates "up" direction

**Drawer use**: Typically `false` (not vertical).

### Advantages

- **Smaller grid**: 25mm vs 42mm (tighter alignment)
- **Wall mounting**: Can use same connectors on wall boards

### Limitations

- **Less common**: Gridfinity more popular for drawers
- **Requires openGrid board**: Additional component
- **No multi-tile**: Single 25mm grid only

### Example Use Case

**Workshop wall + drawer combo**:

- Wall: openGrid board with tool holders
- Drawer: NeoGrid dividers with openGrid base
- Connectors compatible with both applications

## Flat Base

**Simple flat baseplate** with no snap features.

### When to Use

- No existing grid system
- Want repositioning via adhesive pads
- Custom grid spacing (not 42mm or 25mm)
- Simple, universal solution

### Parameters

```openscad
Selected_Base = "Flat";
Flat_Base_Thickness = 1.4;    // Base thickness (mm)
grid_size = 30;               // Custom grid size (default 30mm)
custom_grid_size = 0;         // Override if needed
```

### Base Profile

**Flat disc**:

- No snap features
- Thickness: `Flat_Base_Thickness` (default 1.4mm)
- Chamfered edges for smooth appearance

**Attachment**:

- Double-sided foam tape (3M, VHB)
- Adhesive pads
- Hot glue (semi-permanent)

### Grid Sizing

**Default**: 30mm grid (arbitrary, no standard)

**Custom**:

```openscad
custom_grid_size = 42;  // Mimic Gridfinity spacing without snap
grid_size = 42;         // Auto-set from custom_grid_size
```

**Use case**: Visual alignment without Gridfinity baseplate.

### Advantages

- **Simple**: No baseplate required
- **Flexible**: Any grid spacing
- **Universal**: Works in any drawer
- **Thin**: Minimal height added (~1.4mm)

### Limitations

- **Not repositionable**: Tape/adhesive is semi-permanent
- **No alignment aid**: Must position manually
- **Less stable**: No mechanical lock (relies on adhesive)

### Example Use Case

**Budget drawer organization**:

- No Gridfinity baseplate
- Use foam tape to secure connectors
- Layout planned with paper template first
- One-time setup (not frequently reconfigured)

## None (No Base)

**Connectors without base attachment**. Dividers rest on drawer bottom directly.

### When to Use

- Minimal filament usage
- Non-drawer applications
- Divider height provides stability

### Parameters

```openscad
Selected_Base = "None";
// No additional base parameters
```

### Base Profile

**None**: Connectors end at channel bottom.

**Support**: Dividers provide vertical support, connectors provide junction strength.

### Attachment

**Friction/gravity**:

- Connectors held by divider tension
- No adhesive needed
- Divider height prevents tipping

**Optional adhesive**: Small dots of hot glue if needed.

### Advantages

- **Minimal filament**: Least material usage
- **Thinnest**: No base adds no height
- **Simple**: No baseplate, no tape needed

### Limitations

- **Unstable**: Can slide if drawer jolts
- **No alignment**: Manual positioning only
- **Not repositionable**: Moving connectors moves entire layout

### Example Use Case

**Tall dividers in shallow drawer**:

- Divider height: 100mm+
- Drawer depth: 40mm
- Dividers provide inherent stability
- Base attachment unnecessary

**Temporary layouts**:

- Short-term organization
- Will be reconfigured soon
- Don't want to commit adhesive

## Base Chamfer Settings

**All base types** have chamfered bottom edges for smooth appearance.

### Parameters

```openscad
Custom_Base_Chamfer = false;       // Override auto chamfer
Custom_Base_Chamfer_Size = 2;      // Manual chamfer size (mm)
```

### Auto Chamfer Sizes

**Defaults** (when `Custom_Base_Chamfer = false`):

- Gridfinity: 5mm chamfer (matches spec)
- Flat: 4mm chamfer
- openGrid: 3mm chamfer

**Custom override**:

```openscad
Custom_Base_Chamfer = true;
Custom_Base_Chamfer_Size = 3;  // Set specific chamfer
```

**Use case**: Aesthetic preference or clearance issues.

## Print Specifications on Base

**Emboss material thickness** on bottom of base for reference.

### Parameter

```openscad
Print_Specs = true;  // Emboss Material_Thickness value on base
```

**Output**: Material thickness value (e.g., "8.5") embossed on base bottom.

**Use case**: Identify which connectors match which material after printing multiple sets.

## Mixing Base Systems

**Within single drawer**: Possible but not recommended.

- All connectors should use same base type for consistency
- Mixing Gridfinity + Flat creates uneven heights

**Across drawers**: Absolutely.

- Drawer 1: Gridfinity base (frequently reconfigured)
- Drawer 2: Flat base (permanent layout)
- Drawer 3: None (tall dividers)

## Base Selection Summary Table

| Base Type      | Height | Attachment             | Repositionable | Grid   | Multi-tile   | Use Case                      |
| -------------- | ------ | ---------------------- | -------------- | ------ | ------------ | ----------------------------- |
| **Gridfinity** | ~5mm   | Snap to baseplate      | Yes            | 42mm   | Yes (X only) | Modular system, easy reconfig |
| **openGrid**   | 3-7mm  | Snap to openGrid       | Yes            | 25mm   | No           | Wall/vertical mounting        |
| **Flat**       | ~1.5mm | Adhesive tape          | Limited        | Custom | No           | Simple, no baseplate          |
| **None**       | 0mm    | Friction/optional glue | No             | N/A    | No           | Minimal, temporary            |

## Recommendation by Drawer Use

**Frequently reconfigured** (seasonal, evolving needs):

- Gridfinity base (easy repositioning)

**One-time setup** (permanent organization):

- Flat base (simple, economical)

**Budget/minimal** (low cost, minimal filament):

- None or Flat

**Existing system** (already have Gridfinity/openGrid):

- Match existing base type
