---
name: home-organization
description: Decision framework for choosing between 3D-printed home organization systems (Gridfinity, OpenGrid, Neogrid, French Cleat, Underware). Provides interpretive guidance on system selection based on item size, mounting surface, and use case. Use when users ask which organization system to recommend or need help choosing between modular storage options.
---

# 3D-Printed Home Organization System Selection

## Required Reading Before Recommending Systems

Fetch these reference docs every time to verify current specifications:

- **./gridfinity-reference.md** - Small item desktop/drawer organization (42mm grid)
- **./opengrid-reference.md** - Wall-mounted framework (28mm grid)
- **./neogrid-reference.md** - Large item drawer dividers (hybrid 3D-printed connectors)
- **./french-cleat-reference.md** - Heavy-duty wall mounting (45° angled cleats)
- **./underware-reference.md** - Cable management channels (OpenGrid-compatible)
- **./cross-system-compatability.md** - Interoperability matrix between systems
- **./frenchfinity-reference.md** - Modular French Cleat tool holders with Gridfinity integration

## Core Understanding: System Architecture

These systems form an **ecosystem** rather than competing alternatives:

**Dimensional Relationships:**

- Gridfinity: 42mm base unit (horizontal surfaces)
- OpenGrid: 28mm base unit (vertical surfaces)
- Mathematical alignment: 3 × OpenGrid (84mm) = 2 × Gridfinity (84mm)
- Neogrid: Uses multiples of 42mm for Gridfinity compatibility
- French Cleat: Dimension-agnostic (works with any system via adapters)
- Underware: Parametric (sized to cable bundles, snaps into OpenGrid)

**Critical insight Claude might miss:** These systems are designed to **work together** in a unified home organization strategy. Users shouldn't choose "one system" - they should combine systems based on spatial context.

## Decision Framework: Which System When?

### By Mounting Surface (Official Specification)

| Surface Type | System(s) | Why |
|-------------|-----------|-----|
| Desktop/shelf | Gridfinity | Magnetic or friction-fit baseplates, easy reconfiguration |
| Drawer (small items) | Gridfinity | Bins organize loose parts, paperclips, screws, USB drives |
| Drawer (large items) | Neogrid | Hybrid approach uses cheap divider material with 3D-printed connectors |
| Wall (light items) | OpenGrid | 28mm grid with front-access snaps, living-room compatible |
| Wall (heavy items) | French Cleat | 45° gravity lock, 100kg+ capacity when mounted to studs |
| Under desk/wall cables | Underware | Click-and-slide channels, OpenGrid-native integration |

### By Item Characteristics (Best Practices)

**Use Gridfinity when:**

- Items fit in 42mm × 42mm × 7mm multiples
- Items need frequent reorganization
- Desktop or drawer placement
- Want magnetic attachment option
- Examples: drill bits, resistors, pens, USB cables, craft supplies

**Use OpenGrid when:**

- Need wall-mounted access to small items
- Want "living room compatible" aesthetics
- Items under ~5kg per mount point
- Cable routing with Underware integration
- Examples: scissors, tape dispensers, phone holders, printer tools

**Use Neogrid when:**

- Drawer items too large for Gridfinity
- Want cost-effective large dividers (not fully 3D-printed)
- Organizing clothing, kitchen utensils, workshop tools
- Need reconfigurable drawer layouts
- Examples: t-shirts, spatulas, hand tools, fabric storage

**Use French Cleat when:**

- Wall mounting items over 10kg
- Need industrial-strength attachment
- Want maximum reconfigurability (lift-and-move)
- Mounting shelves, cabinets, power tools, panels
- Examples: drill charging stations, shelving units, Frenchfinity tool walls

**Use Underware when:**

- Managing cable bundles under desks
- Need parametric sizing (custom width/height/length)
- Want OpenGrid integration
- Examples: power cables, USB hubs, cable routing, LED channels

### By Combination Strategy (Best Practices)

**Common combinations that work well:**

1. **Home office:**
   - OpenGrid on wall (scissors, tape, phone)
   - Underware under desk (cable management)
   - Gridfinity on desktop (small accessories)

2. **Workshop wall:**
   - French Cleat for heavy tools (drill station, shelves)
   - Frenchfinity holders for hand tools (wrenches, pliers)
   - Gridfinity adapter on cleat for small parts bins

3. **Bedroom drawer:**
   - Neogrid dividers for clothing sections
   - Gridfinity bins within sections for accessories (watches, jewelry)

4. **Kitchen drawer:**
   - Neogrid for utensil dividers
   - Mixed with Gridfinity for spice packets or bag clips

## Common Pitfalls

### Pitfall #1: Choosing Systems in Isolation

**Problem:** User asks "Should I use Gridfinity or OpenGrid?" without context

**Why it fails:** These systems serve different mounting surfaces - Gridfinity is horizontal, OpenGrid is vertical

**Better approach:**

```
Question: "What are you organizing and where will it be mounted?"
- Desktop → Gridfinity
- Wall → OpenGrid or French Cleat (based on weight)
- Drawer (small items) → Gridfinity
- Drawer (large items) → Neogrid
- Cables → Underware
```

### Pitfall #2: Over-Printing with Neogrid

**Problem:** User wants to 3D-print large drawer dividers entirely in plastic

**Why it fails:** Neogrid's value is using **store-bought materials** (MDF, plywood) with 3D-printed connectors

**Better approach:** Print only the X/T/L/I junction connectors (~50g each), cut dividers from 8.5mm utility board ($5 for 10+ dividers)

### Pitfall #3: Underestimating French Cleat Strength Requirements

**Problem:** User wants to use 3D-printed French cleats for heavy items (power tools, cabinets)

**Why it fails:** Load capacity of plastic cleats is ~5-10kg; wood cleats handle 50-100kg

**Better approach:**

- Items under 5kg: 3D-printed PETG cleats OK
- Items 5-20kg: Plywood cleats (18mm / ¾")
- Items over 20kg: Hardwood cleats, screwed into studs every 40cm

### Pitfall #4: Ignoring Mathematical Grid Alignment

**Problem:** User tries combining Gridfinity and OpenGrid without understanding 84mm relationship

**Why it fails:** Accessories won't align properly unless using 3:2 ratio

**Better approach:** 3 OpenGrid units (28mm × 3 = 84mm) = 2 Gridfinity units (42mm × 2 = 84mm). Design combo layouts using 84mm as the common denominator.

### Pitfall #5: Treating Underware as Fully Standalone

**Problem:** User wants Underware without OpenGrid base

**Why it fails:** While Underware 2.0 supports magnets/adhesive, it's designed for **OpenGrid integration** (native snap-in)

**Better approach:** Install OpenGrid boards under desk first, then snap Underware channels directly into grid. Use magnets/adhesive only for curved surfaces (table legs).

## System Interoperability Summary (Official Specification)

| System | Gridfinity | Underware | OpenGrid | French Cleat | Neogrid |
|--------|------------|-----------|----------|--------------|---------|
| **Gridfinity** | — | ⚙️ | ✅ | ✅ | ⚙️ |
| **Underware** | ⚙️ | — | ✅ | ⚙️ | ⚙️ |
| **OpenGrid** | ✅ | ✅ | — | ✅ | ✅ |
| **French Cleat** | ✅ | ⚙️ | ✅ | — | ⚙️ |
| **Neogrid** | ⚙️ | ⚙️ | ✅ | ⚙️ | — |

**Legend:**

- ✅ = Native compatibility or well-supported adapters
- ⚙️ = Possible but requires custom integration or indirect connection
- — = Same system

Read ./cross-system-compatability.md for detailed compatibility notes.

## Quality Checklist for Recommendations

Before suggesting a system to users, verify:

**Context gathered:**

- ✓ What items need organizing? (size, weight, frequency of access)
- ✓ Where will system be mounted? (wall, desk, drawer, under desk)
- ✓ Is reconfigurability important? (static vs. frequent changes)
- ✓ Weight of items? (<1kg, 1-5kg, 5-20kg, 20kg+)
- ✓ Aesthetic requirements? (workshop vs. living room visible)

**System selection rationale:**

- ✓ Mounting surface matches system type (horizontal vs. vertical)
- ✓ Item size appropriate for system grid (42mm vs. 28mm vs. custom)
- ✓ Load capacity sufficient for item weight
- ✓ Considered combinations rather than single-system approach
- ✓ Checked compatibility matrix if mixing systems

**Practical guidance:**

- ✓ Referenced specific dimensions from official specs
- ✓ Mentioned material requirements (PLA/PETG, plywood thickness, etc.)
- ✓ Highlighted cost-saving approaches (Neogrid hybrid, Underware iterative)
- ✓ Warned about 3D printing limitations (French Cleat load capacity)
- ✓ Suggested test prints before bulk printing

## When NOT to Use These Systems

**Don't use when:**

- User needs temporary/portable organization → Use bins/boxes instead
- Items are irregularly shaped → Custom-design holders (not modular grid)
- Rental property won't allow wall mounting → Desktop-only solutions
- User has no 3D printer access → Pre-made commercial systems
- Weight exceeds safe limits → Industrial shelving/mounting

**Alternative approaches:**

- Modular commercial systems (IKEA SKÅDIS for walls)
- Traditional drawer organizers (bamboo dividers)
- Custom woodworking (one-off solutions)
- Pegboard walls (non-3D-printed, widely available)

## Documentation References

**Official sources:**

- Gridfinity: https://gridfinity.xyz/specification/
- OpenGrid: https://www.opengrid.world/
- Neogrid: https://handsonkatie.com/neogrid-organise-your-big-items-with-this-free-and-open-source-system/
- Underware: https://handsonkatie.com/underware-2-0-the-made-to-measure-collection/
- Frenchfinity: https://frenchfinity.xyz/

**Community resources:**

- MakerWorld designs: https://makerworld.com (search by system name)
- Comprehensive guide: https://handsonkatie.com/the-ultimate-home-organisation-system/
- Gridfinity generator: https://gridfinitygenerator.com/

**Related spirograph plugin skills:**

- opengrid-openscad (code generation for OpenGrid accessories)
