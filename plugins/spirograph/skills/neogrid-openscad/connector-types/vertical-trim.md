# Vertical Trim Connector

Edge trim for drawer openings. Single piece (not base/top split).

## When to Use

**Use for:**

- Drawer front/back edges (where drawer opens)
- Visible divider edges that need finished appearance
- Protecting divider material from drawer sliding contact

**Layout example:**

```
Drawer opening
┌─────────────
│║  ← Vertical Trim on divider edge
│║
```

## Module Call

```openscad
// Single piece (no base/top split)
NeoGrid_Vertical_Trim(
    Material_Thickness,
    Wall_Thickness = 4,
    Total_Trim_Width = 42,
    Middle_Seam_Width = 5,
    Total_Trim_Height = 20
);
```

**Note**: Vertical Trim is single-piece design, unlike other connectors (no separate base/top).

## Geometry

**Two-sided clip design**:

**Cutouts**:

- Two cutouts on left and right sides
- Each cutout width: `Total_Trim_Width/2 - Middle_Seam_Width/2`
- Material slides into cutouts from sides

**Middle seam**:

- Solid section in center
- Width: `Middle_Seam_Width` (default 5mm)
- Provides structural strength

**Chamfers**:

- Chamfers on all exposed edges
- Front, back, top, bottom
- Chamfer size: `Wall_Thickness/3`

**Result**: Trim clips onto divider edge, covers raw material.

## Parameters

**Total_Trim_Width** (default 42mm):

- Overall width of trim piece
- Should match or exceed divider height
- Typically match grid_size for consistency

**Total_Trim_Height** (default 20mm):

- How tall the trim extends
- Should be ≥ drawer depth at opening
- Adjust based on divider material height

**Middle_Seam_Width** (default 5mm):

- Width of center structural section
- Narrower = easier flex for clipping
- Wider = stronger trim piece

**Material_Thickness**:

- Must match divider material (same as connectors)
- Cutout sized to grip material firmly

**Wall_Thickness** (default 4mm):

- Thickness of trim walls
- Affects strength and chamfer size

## Print Orientation

**Prints upright**:

- Stand trim vertically (as displayed in OpenSCAD)
- Cutouts face left/right
- Front face smooth (visible surface)
- No supports needed

## Installation

1. Slide trim onto divider edge from top or bottom
2. Trim clips onto material via cutouts
3. Middle seam bridges over divider edge
4. Chamfered edges face drawer opening (finished appearance)

**Multiple trims**: One per divider edge at drawer opening.

## Common Use Cases

### Drawer Front Edges

**Dividers visible when drawer opens**:

```
     Drawer front
     ┌─────────────
     │║  ║  ║  ← Vertical Trim on each divider
     │
```

**Use case**: Professional appearance, protects divider edges from wear.

### Frequent Access Drawers

**High-traffic drawers** (daily access):

- Vertical Trim prevents divider material chipping/fraying
- Especially important for MDF (fragile edges)
- Less critical for acrylic/plywood (hard edges)

### Aesthetic Upgrade

**Visible drawer organization**:

- Covers raw divider edges
- Uniform appearance across all dividers
- Optional feature (not structural)

## When NOT to Use

**Interior dividers**: No visible edge, trim unnecessary.

**Low-traffic drawers**: Rarely opened, edge wear minimal.

**Budget builds**: Trim is optional aesthetic feature.

**Already using edge connectors**: T/L/End connectors already cap divider edges.

## Example Layout

**User: "Grid layout with front-facing dividers"**

Vertical Trim count:

- Interior dividers (perpendicular to front): N trim pieces
- Parallel dividers (along drawer sides): 0 (edges not visible)
- Result: Only dividers facing drawer opening need trim

**Example**: 3×3 grid, 4 vertical dividers face front → 4 Vertical Trim pieces.

## Common Issues

**Trim won't clip onto divider:**

- Material_Thickness too large (reduce by 0.1-0.2mm)
- Middle_Seam_Width too wide (reduce for more flex)
- Divider edge not square (trim requires flat surface)

**Trim too loose:**

- Material_Thickness too small (increase by 0.1-0.2mm)
- Material variance (measure edge material thickness specifically)

**Trim too short:**

- Increase Total_Trim_Height to match divider height
- Trim should cover full visible edge

**Used trim on wrong edges:**

- Only apply to visible edges (drawer opening)
- Interior edges don't need aesthetic trim
- Waste of filament/time for hidden edges
