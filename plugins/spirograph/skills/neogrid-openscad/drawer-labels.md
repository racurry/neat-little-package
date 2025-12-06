# Drawer Label Holders

Optional accessory for labeling drawer fronts. Separate from divider system, commonly paired with NeoGrid.

## When to Use

**Use for:**

- Labeling drawer contents from outside
- Professional appearance
- Drawer organization with multiple similar drawers
- Quick visual identification

**Not related to dividers**: Label holders mount to drawer front, not interior divider system.

## Source File

**QuackWorks**:

- File: `DrawerLabelsAndHandles.scad`
- Location: `/Users/aaron/workspace/infra/neat-little-package/.tmp/QuackWorks/NeoGrid/DrawerLabelsAndHandles.scad`
- License: CC BY-NC-SA 4.0

## Module Call

```openscad
// Main label holder (generates based on parameters)
drawerLabelHolder();
```

**Not a function-based module**: Uses global parameters (OpenSCAD Customizer style).

## Core Parameters

### Mounting

```openscad
Mount_Type = "Hook";           // Hook | Double-Sided Tape
Drawer_Thickness = 16;         // Thickness of drawer front (mm)
Double_Sided_Tape_Recess = 0;  // Recess depth for tape (mm)
```

**Hook mount** (standard):

- Hooks over top edge of drawer
- No adhesive needed
- Removable

**Tape mount**:

- Adhesive attachment to drawer front
- Permanent
- Flat back with optional tape recess

### Dimensions

```openscad
Label_Height = 25;             // Height of label slot (mm)
Label_Holder_Width = 80;       // Total width of holder (mm)
Label_Thickness = 1;           // Space for label to slide in (mm)
```

**Label size**: Print or cut labels to fit slot dimensions.

- Actual visible area < total due to borders
- Account for `Top_and_Bottom_Border_Height` and `Left_and_Right_Border_Width`

### Style

```openscad
Top_and_Bottom_Border_Height = 6.5;  // Border above/below label (mm)
Left_and_Right_Border_Width = 3;     // Border left/right of label (mm)

View_Window_Style = "Chamfered";     // Squared | Chamfered | Rounded
View_Window_Chamfer_or_Rounding_Amount = 2;  // Chamfer/rounding size (mm)

Top_and_Bottom_Chamfers = true;      // Chamfer top/bottom edges
```

## Optional Drawer Handle

**Integrated pull handle** on label holder.

### Parameters

```openscad
Drawer_Handle_Style = "None";        // None | Squared
Additional_Label_Drop = 10;          // Lower label for handle clearance (mm)
Drawer_Handle_Thickness = 2;         // Handle wall thickness (mm)
Drawer_Handle_Depth = 15;            // How far handle extends (mm)
Drawer_Handle_Lip_Height = 6;        // Vertical lip for finger grip (mm)
```

**Use case**: Small drawers without built-in handles.

**Label drop**: Lowers label so handle doesn't obscure it.

## Optional Printed Label

**Emboss text directly** on label holder (instead of paper insert).

### Parameters

```openscad
Add_Printed_Label = false;           // Emboss text instead of insert slot
textFont = "Monsterrat:style=Bold";  // Font for embossed text

Line_1_Text = "Example";             // Top line text
Line_1_Text_Height = 6;              // Font size (mm)
Line_1_Color = "#000000";            // Text color

Line_2_Text = "";                    // Bottom line (empty = single line)
Line_2_Text_Height = 8;              // Font size (mm)
Line_2_Color = "#000000";            // Text color

Label_Background_Color = "#ffffff";  // Background color
```

**Single vs dual line**:

- `Line_2_Text = ""`: Single centered line
- `Line_2_Text = "..."`: Two lines distributed vertically

**Color**: Multi-material/color printing or visual preview only.

## Optional Screw Mounting

**Reinforce with screws** (in addition to hook/tape).

### Parameters

```openscad
Screw_Mounting_Location = "None";    // None | Behind Label | Back of Hook
Distance_Between_Screws_Center_to_Center = 60;  // Spacing (mm)
Screw_Outer_Thread_Diameter = 4.1;   // Thread diameter (mm)
Screw_Head_Diameter = 7.2;           // Head diameter (mm)
Screw_Head_Inset = 0;                // Depth before chamfer (mm)
```

**Behind Label**: Screws hidden by label insert.
**Back of Hook**: Screws through back section (more secure).

## Advanced Parameters

```openscad
Holder_General_Thickness = 1;        // Wall thickness (mm)
Holder_Back_Thickness = 1.2;         // Back wall thickness (mm)
Label_Buffer_Height = 1;             // Extra height for easy insertion (mm)
Label_Vertical_Capture = 1;          // Border overlap to hold label (mm)
Drawer_Back_Dropdown_Height = 20;    // How far back extends into drawer (mm)
```

## Print Orientation

```openscad
Print_Orientation = true;            // true = print on side, false = upright
```

**Print on side** (default `true`):

- Label holder lays on side
- Minimizes support material
- Better surface finish on front

**Upright** (`false`):

- Preview orientation (as mounted on drawer)
- May require supports

## Label Insert Creation

### Paper Labels

**Dimensions**:

1. Measure holder opening: `Label_Holder_Width - Left_and_Right_Border_Width*2`
2. Height: `Label_Height - Label_Vertical_Capture*2`
3. Example: 80mm width - 6mm borders = 74mm × ~24mm

**Materials**:

- Cardstock (heavier paper, doesn't curl)
- Laminated paper (water-resistant)
- Photo paper (glossy appearance)

**Tools**:

- Label maker (if size compatible)
- Inkjet/laser printer + paper cutter
- Hand-drawn + laminate

### Printed Labels

**If using `Add_Printed_Label = true`**:

- No paper insert needed
- Text embossed directly on holder
- Permanent (can't change without reprinting)

## Example Configurations

### Standard Hook Mount

```openscad
Mount_Type = "Hook";
Drawer_Thickness = 16;
Label_Height = 25;
Label_Holder_Width = 80;
Drawer_Handle_Style = "None";
```

**Use case**: Most common setup, removable label holder.

### Tape Mount with Handle

```openscad
Mount_Type = "Double-Sided Tape";
Drawer_Thickness = 16;
Label_Height = 25;
Label_Holder_Width = 100;
Drawer_Handle_Style = "Squared";
Additional_Label_Drop = 10;
```

**Use case**: Drawers without handles, permanent label attachment.

### Embossed Text Label

```openscad
Add_Printed_Label = true;
Line_1_Text = "TOOLS";
Line_1_Text_Height = 8;
Line_2_Text = "";  // Single line
```

**Use case**: Permanent labels, multi-color printing.

## Common Use Cases

### NeoGrid Drawer System

**Pair with divider system**:

- Interior: NeoGrid dividers organize contents
- Exterior: Label holder identifies drawer
- Result: Professional organization inside and out

### Workshop Drawers

**Multiple similar drawers**:

- Each drawer: Different tool categories
- Label holders: Quick identification without opening
- Hook mount: Easily swap labels as organization changes

### Kitchen/Pantry

**Uniform drawer fronts**:

- Label holders distinguish contents
- Paper inserts allow easy re-labeling
- Clean, professional appearance

## Common Issues

**Label holder too wide for drawer**:

- Reduce `Label_Holder_Width` parameter
- Minimum: ~60mm (functional)

**Hook doesn't fit drawer thickness**:

- Measure actual drawer front thickness with calipers
- Adjust `Drawer_Thickness` parameter
- Account for drawer lip/bevel if present

**Paper label curls**:

- Use heavier cardstock (80lb+)
- Laminate paper before inserting
- Consider printed label option instead

**Handle obscures label**:

- Increase `Additional_Label_Drop` to lower label
- Reduce `Drawer_Handle_Lip_Height` if too tall
- Consider handle-less design if clearance issues persist

**Tape mount doesn't stick**:

- Clean drawer surface (isopropyl alcohol)
- Use VHB tape (3M) for permanent bond
- Increase `Double_Sided_Tape_Recess` for thicker tape
- Consider hook mount instead

## Integration with NeoGrid Code

**Separate file** from connector generation:

```openscad
// Generate connectors (Neogrid.scad)
include <Neogrid.scad>;
NeoGrid_X_Intersection_Base(...);

// Generate label holder (DrawerLabelsAndHandles.scad)
include <DrawerLabelsAndHandles.scad>;
drawerLabelHolder();
```

**Not typically combined**: Labels are optional accessory, not part of divider system code.

## Recommendation

**When to include in NeoGrid project**:

- User mentions labeling drawers
- Multiple drawers in same furniture piece
- Professional/commercial organization project

**When to skip**:

- Single drawer project
- Drawers already labeled (existing handles/labels)
- Budget/minimal filament focus
