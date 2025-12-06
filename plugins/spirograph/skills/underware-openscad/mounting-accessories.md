# Mounting and Accessories: Keyholes, Hooks, Item Holders, Connectors

Reference for generating Underware mounting accessories and add-ons.

## QuackWorks Reference Files

**Source files:**

- Keyholes: `Underware_keyholes.scad`
- Hooks: `Underware_Hooks.scad`
- Item Holders: `Underware_Item_Holder.scad`
- Connectors: `Underware_Connectors.scad`

**Fetch from**: https://github.com/AndyLevesque/QuackWorks/tree/main/Underware

## Accessory Selection Guide

| Accessory | Purpose | Use Case |
|-----------|---------|----------|
| Keyholes | Wall mounting without OpenGrid | Direct drywall/wood surface mounting |
| Hooks | Hang items from channel | Cable loops, lightweight tools, accessories |
| Item Holders | Clamp items to channel | Phone holders, tool clips, attachments |
| Connectors | Join channel sections | Threaded snap connections between channels |

## Keyholes (Wall Mounting)

### When to Use Keyholes

**Use when:**

- Mounting directly to drywall/wood wall (no OpenGrid board)
- Need permanent fixed installation
- Using standard wall anchors or screws
- Budget-conscious installation (no OpenGrid board cost)

**Don't use when:**

- Have OpenGrid/Multiboard already installed → Use channel's built-in mounting
- Need repositionable system → OpenGrid better
- Renting (can't drill holes) → Use adhesive or magnetic mounting

### Keyhole Specific Parameters

```openscad
/*[Keyhole Configuration]*/
Keyhole_Width_in_Units = 1;        // Width matching channel width
Number_of_Keyholes = 3;            // How many keyhole slots
Keyhole_Spacing = 25;              // Distance between keyholes (mm)
Screw_Head_Diameter = 8;           // Screw head size (mm)
Screw_Shaft_Diameter = 4;          // Screw shaft size (mm)
```

### Keyhole Mounting Workflow

**Step 1: Print keyhole base**

- Keyhole base replaces standard Underware base
- Contains vertical slots for hanging on wall screws

**Step 2: Install wall screws**

```
1. Mark screw positions (spacing from Number_of_Keyholes × Keyhole_Spacing)
2. Drill pilot holes
3. Install screws leaving ~3mm exposed (screw heads stick out)
4. Hang keyhole base on screw heads
5. Slide down to lock into narrow slot
```

**Step 3: Attach channel top**

- Snap Underware top onto keyhole base (standard snap connection)

### Keyhole Configurations

#### Configuration 1: Standard 3-Hole Mount

```openscad
// Typical desk/wall installation (75mm span)
Keyhole_Width_in_Units = 1;        // Match 1-unit channel
Number_of_Keyholes = 3;            // 3 screws for stability
Keyhole_Spacing = 25;              // Grid-aligned spacing
Screw_Head_Diameter = 8;           // Standard #6 screw
Screw_Shaft_Diameter = 4;          // 4mm shaft
```

**Result**: 3 keyholes spanning 50mm (2 × 25mm), stable 3-point mount.

#### Configuration 2: Long Run Multi-Keyhole

```openscad
// Long wall run requiring multiple attachment points
Keyhole_Width_in_Units = 1;
Number_of_Keyholes = 6;            // Every 25mm for 125mm run
Keyhole_Spacing = 25;
Screw_Head_Diameter = 8;
Screw_Shaft_Diameter = 4;
```

**Result**: 6 keyholes spanning 125mm, prevents sagging on long channels.

### Keyhole vs Channel Mounting Methods

**Keyholes are ALTERNATIVE to** channel mounting methods:

```
Standard channel mounting:
- Threaded Snap Connector → OpenGrid boards
- Direct Multiboard Screw → Multiboard holes
- Magnet → Magnetic surfaces
- Wood Screw → Direct wood/desk

Keyhole mounting:
- Separate keyhole base piece
- Replaces standard channel base
- Direct wall hanging (no board needed)
```

**Don't mix**: Use either keyhole base OR standard channel base with mounting method, not both.

## Hooks (Item Hanging)

### When to Use Hooks

**Use when:**

- Hanging lightweight items from installed channels (cables, tools, accessories)
- Need removable/repositionable hanging points
- Organizing cable loops (slack management)
- Adding functionality to existing channel runs

**Don't use when:**

- Items too heavy (>500g per hook) → Use item holders or direct mounting
- Need enclosed storage → Use OpenGrid bins instead
- Items need secure clamping → Use item holders

### Hook Specific Parameters

```openscad
/*[Hook Configuration]*/
Hook_Length = 30;                  // Projection from channel (mm)
Hook_Diameter = 5;                 // Thickness of hook (mm)
Hook_Angle = 90;                   // Hook bend angle (degrees)
Number_of_Hooks = 1;               // Hooks per piece
```

### Hook Mounting

**Integration with channels:**

- Hooks attach to TOP of Underware top piece
- Items rest in hook, held by gravity
- Removable (not permanent attachment)

**Hook_Length decision:**

| Item to hang | Recommended length | Notes |
|--------------|-------------------|-------|
| Thin cables (USB, audio) | 20mm | Minimal projection |
| Power cables | 30mm | Standard |
| Coiled cables | 40-50mm | Larger loop diameter |
| Small tools (screwdrivers) | 40mm | Tool handle clearance |

**Hook_Angle options:**

- **90°**: Standard J-hook (perpendicular to channel)
- **45°**: Angled hook (easier insertion, less retention)
- **120°**: Secure hook (harder to remove, more retention)

### Hook Configurations

#### Configuration 1: Cable Management Hooks

```openscad
// Hang slack cable loops along desk run
Hook_Length = 30;                  // Standard cable loop size
Hook_Diameter = 5;                 // Strong enough for cable weight
Hook_Angle = 90;                   // Standard J-hook
Number_of_Hooks = 1;               // Individual hooks, space as needed
```

**Use for**: Organizing excess cable length, keeping cables tidy.

#### Configuration 2: Tool Hanging

```openscad
// Hang screwdrivers, pliers, light hand tools
Hook_Length = 40;                  // Tool handle clearance
Hook_Diameter = 6;                 // Thicker for tool weight
Hook_Angle = 120;                  // Secure retention
Number_of_Hooks = 1;
```

**Use for**: Workshop organization, frequently-accessed tools.

## Item Holders (Clamping Attachment)

### When to Use Item Holders

**Use when:**

- Securely holding specific items (phones, tablets, tools)
- Need custom-fit holder for particular object
- Items too heavy for hooks (clamping more secure)
- Creating dedicated storage spots (phone charging station, etc.)

**Don't use when:**

- Generic hanging sufficient → Use hooks (simpler)
- Items change frequently → Hooks more flexible
- Need large storage → Use OpenGrid bins

### Item Holder Design Pattern

**Clamshell structure:**

```
Top half (clips to channel)
    ┌─────────────┐
    │   Item      │  ← Custom-shaped cavity for specific item
    │   cavity    │
    └─────────────┘
Bottom half (attaches to top half)

Both halves clamp item between them
```

**Customization required**: Item holders need custom cavity shape for each item type.

### Item Holder Parameters

```openscad
/*[Item Holder Configuration]*/
Item_Width = 80;                   // Width of item to hold (mm)
Item_Depth = 10;                   // Depth/thickness of item (mm)
Item_Height = 150;                 // Height of item (mm)
Holder_Grip_Depth = 5;             // How much to clamp (mm)
```

### Item Holder Configurations

#### Configuration 1: Phone Charging Dock

```openscad
// Hold phone vertically for charging
Item_Width = 75;                   // Phone width
Item_Depth = 10;                   // Phone thickness
Item_Height = 160;                 // Phone height
Holder_Grip_Depth = 8;             // Secure grip without blocking ports
Channel_Width_in_Units = 2;        // Wider channel for stability
```

**Result**: Phone holder clips to channel, holds phone upright for desk charging.

#### Configuration 2: Screwdriver Holder

```openscad
// Secure screwdriver storage
Item_Width = 30;                   // Handle width
Item_Depth = 30;                   // Handle diameter
Item_Height = 200;                 // Total screwdriver length
Holder_Grip_Depth = 10;            // Firm handle grip
```

**Result**: Screwdriver clamped securely, easily removable.

## Connectors (Channel Joining)

### When to Use Connectors

**Use when:**

- Joining two channel sections (modularity)
- Creating removable connections between channels
- Building extensible cable management systems
- Need alignment between channel segments

**Don't use when:**

- Channels can print as one piece → Single channel simpler
- Using different channel types → Channels designed to snap together directly
- Need permanent joint → Print as single piece

### Connector Types

**Threaded Snap Connector (Standard)**:

- Same connector used for OpenGrid board mounting
- Threads into channel base, protrudes for connection
- Opposite channel snaps onto protruding connector

**Parameters:**

```openscad
/*[Connector Configuration]*/
Connector_Type = "Threaded Snap";  // Standard for Underware
Connector_Count = 1;               // Per channel end
```

### Connector Use Pattern

**Modular channel system:**

```
Channel 1 Base                Channel 2 Base
    ┌──────┐                      ┌──────┐
    │      │  ← Connector →       │      │
    └──────┘                      └──────┘

Channel 1 Top (clips onto both bases + connector)
```

**Benefits:**

- Print shorter channel segments (faster, less failure risk)
- Mix and match channel types
- Repair single section without reprinting entire run
- Reconfigure layouts

### Connector Configuration

```openscad
// Standard threaded snap connector for joining channels
Connector_Type = "Threaded Snap";
Connector_Count = 1;               // One connector per joint

// Same threading parameters as standard Underware mounting:
Pitch_Sm = 3;
Outer_Diameter_Sm = 6.747;
Flank_Angle_Sm = 60;
Thread_Depth_Sm = 0.5;
```

## Mounting Method Decision Matrix

**Built-in channel mounting** (no separate accessories):

| Method | Surface | Hardware | Repositionable | Cost |
|--------|---------|----------|----------------|------|
| Threaded Snap Connector | OpenGrid/Multiboard | Snap connectors | Yes | Medium |
| Direct Multiboard Screw | Multiboard | Screws | No | Low |
| Direct Multipoint Screw | Honeycomb Wall | Screws | No | Low |
| Magnet | Metal surfaces | Magnets | Yes | Medium |
| Wood Screw | Wood/drywall | Screws | No | Very low |
| Flat | Any (with adhesive) | Adhesive strips | No | Very low |

**Keyhole mounting** (separate accessory):

| Method | Surface | Hardware | Repositionable | Cost |
|--------|---------|----------|----------------|------|
| Keyholes | Drywall/wood | Wall screws | Limited | Very low |

**Selection guide:**

- **Have OpenGrid** → Threaded Snap Connector (best integration)
- **Bare wall, permanent** → Keyholes or Wood Screw
- **Bare wall, temporary** → Magnet or Flat with adhesive
- **Metal desk underside** → Magnet
- **Honeycomb Storage Wall** → Direct Multipoint Screw

## Accessories Quality Checklist

**Before delivering accessory code:**

**Keyhole validation:**

- ✓ `Number_of_Keyholes` appropriate for channel length (rule: 1 per 25-50mm)
- ✓ `Keyhole_Spacing` matches wall stud spacing if possible (typically 400-600mm)
- ✓ `Screw_Head_Diameter` matches user's available screws
- ✓ Explained keyhole replaces standard channel base (not addition)

**Hook validation:**

- ✓ `Hook_Length` sufficient for item diameter + clearance
- ✓ `Hook_Diameter` strong enough for item weight (5mm standard, 6mm+ for tools)
- ✓ `Hook_Angle` provides appropriate retention (90° standard, 120° secure)
- ✓ Explained hooks attach to channel top (not base)

**Item holder validation:**

- ✓ Item dimensions measured accurately (width, depth, height)
- ✓ `Holder_Grip_Depth` provides secure hold without damaging item
- ✓ Cavity shape customized to item (not generic rectangle)
- ✓ Channel width sufficient for holder + item stability

**Connector validation:**

- ✓ Connector type matches channel mounting system (Threaded Snap standard)
- ✓ Thread parameters match Underware standard spec
- ✓ Explained connector usage (joining channel sections)
- ✓ Noted connector count per joint (typically 1)

**Code compliance:**

- ✓ Complete module code copied from QuackWorks (specific accessory file)
- ✓ Attribution comments intact
- ✓ BOSL2 includes present (if required by accessory)
- ✓ Parameters match standard Underware conventions

**User guidance:**

- ✓ Explained accessory selection rationale (vs. built-in mounting)
- ✓ Documented installation workflow (print → install hardware → attach)
- ✓ Noted compatibility (which channels/systems work with accessory)
- ✓ Provided use case examples (what items to hang/hold)

## Common Accessory Pitfalls

### Pitfall #1: Mixing Keyholes with Channel Mounting

**Problem**: Code includes both keyhole base and `Mounting_Method = "Threaded Snap Connector"`.

**Why it fails**: These are mutually exclusive - keyhole is a replacement base, not compatible with channel mounting methods.

**Fix**: Choose one approach:

```openscad
// Option 1: Keyhole mounting (no channel base mounting)
// Generate keyhole base from Underware_keyholes.scad

// Option 2: Channel mounting (no keyholes)
Mounting_Method = "Threaded Snap Connector";
// Generate standard channel base
```

### Pitfall #2: Hook Length Too Short

**Problem**: User wants to hang coiled power cable, `Hook_Length = 20`.

**Why it fails**: 20mm too short for cable loop diameter (typically 40-60mm).

**Fix**: Size hooks to item:

```openscad
// Measure item to hang
Coiled_Cable_Diameter = 50;  // 50mm loop
Hook_Length = 50;            // Match or slightly larger
```

### Pitfall #3: Item Holder Generic Shape

**Problem**: Generating rectangular cavity for oddly-shaped item.

**Why it fails**: Generic rectangle doesn't secure irregular items.

**Fix**: Custom-model cavity:

```openscad
// Don't just use cuboid for cavity
// DO trace item profile, create custom shape:

// Example: Phone with rounded corners
module phone_cavity() {
    hull() {
        // Corner radius matching phone
        for(x = [-35, 35], y = [-75, 75])
            translate([x, y, 0])
                cylinder(r=5, h=item_depth);
    }
}
```

### Pitfall #4: Over-Complicating Simple Use Case

**Problem**: User wants to hang USB cable, code generates custom item holder.

**Why it fails**: Simple hook sufficient, item holder overkill.

**Fix**: Use simplest accessory for need:

```openscad
// USB cable hanging → Simple hook (not item holder)
Hook_Length = 25;
Hook_Diameter = 5;
Hook_Angle = 90;
// Done - no complex clamshell needed
```

### Pitfall #5: Forgetting Connector Threading Match

**Problem**: Custom connector code with different thread parameters than Underware standard.

**Why it fails**: Connectors won't thread into channel bases (mismatched threads).

**Fix**: Always use Underware standard threading:

```openscad
// ALWAYS use these exact values for Underware threading:
Pitch_Sm = 3;
Outer_Diameter_Sm = 6.747;
Flank_Angle_Sm = 60;
Thread_Depth_Sm = 0.5;
Slop = 0.075;
// Never modify - standard across all Underware pieces
```
