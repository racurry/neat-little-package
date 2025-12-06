# Hybrid Approach: Material Selection

NeoGrid's core innovation is separating 3D-printed connectors from store-bought divider materials. This page details material selection, sourcing, and preparation.

## Why Hybrid?

**Economics**:

- Fully 3D-printed drawer system: 500g+ filament, $15-30, 50+ hours
- NeoGrid hybrid: 200g connectors + $5-10 materials, 10-15 hours total
- Savings: ~75% cost, ~70% time

**Flexibility**:

- Reuse connectors with different material thicknesses
- Change divider lengths without reprinting
- Swap materials as availability changes

**Quality**:

- Store-bought sheet materials are flatter than printed sheets
- Professional appearance with proper material choice
- Better strength-to-weight for large compartments

## Material Comparison Table

| Material | Thickness | Cost/sheet | Pros | Cons | Retention spikes? |
|----------|-----------|------------|------|------|-------------------|
| **uPVC utility board** | 8.5mm | Low | No painting, long lengths, UK-available | Less common in US | Optional |
| **Plywood** | 6mm, 8mm | Low | Strong, natural look, widely available | Needs finish/paint | Optional |
| **MDF** | 3mm, 6mm, 8mm | Very low | Cheapest, smooth surface, easy to cut | Heavy, soft (needs spikes) | **Yes** |
| **Acrylic** | 3mm, 6mm | Medium | Transparent, modern aesthetic, easy clean | Brittle, expensive, can crack | **No** |
| **Foam board** | 5mm (~3/16") | Very low | Lightweight, cheap, US-available | Low strength, dents easily | Optional |
| **1/4" hardboard** | 6.35mm | Low | US-standard, strong, smooth | Needs sealing (moisture) | Optional |

## Sourcing Recommendations

### UK (Europe)

**uPVC Utility/Soffit Board** (8.5mm):

- Hardware stores: Obi, Hornbach, Bauhaus, Wickes, B&Q
- Board dimensions: Typically 2400mm × 300mm or longer
- Best choice: Minimal prep, long lengths reduce cutting

**MDF/Plywood**:

- Available at all hardware stores
- Standard thicknesses: 3mm, 6mm, 8mm
- Cut to size or buy full sheets

### US (North America)

**1/4" Plywood/Hardboard** (6.35mm):

- Home Depot, Lowe's, local lumber yards
- Underlayment plywood (economical)
- Cut sheets available

**Foam Poster Board** (5mm / 3/16"):

- Craft stores (Michaels, Hobby Lobby)
- Office supply stores
- Lightweight, easy to cut with knife

**MDF**:

- Hardware stores (standard thickness options)
- Very economical for large projects

### Acrylic (Global)

**Clear/colored acrylic**:

- Plastic suppliers (TAP Plastics, local acrylic shops)
- Online retailers (Amazon, eBay)
- Standard thicknesses: 3mm, 6mm
- More expensive but premium aesthetic

## Material Thickness Measurement

**CRITICAL**: Measure actual material, not nominal specifications.

### Measurement Process

1. **Buy material first** (don't print until you have material in hand)
2. **Use digital calipers** (not ruler or tape measure)
   - Accuracy: ±0.01mm minimum
   - Multiple measurement points across sheet
   1. **If painting/finishing**:
   - Finish ONE piece first
   - Measure AFTER finish dries
   - Paint/stain adds 0.1-0.3mm thickness
3. **Record thickness** for OpenSCAD parameter
4. **Test print** one connector before batch

### Common Thickness Variations

**Nominal vs Actual**:

| Nominal | Actual range | Notes |
|---------|--------------|-------|
| 3mm | 2.9-3.2mm | Varies by manufacturer |
| 6mm | 5.8-6.3mm | Plywood especially variable |
| 1/4" (6.35mm) | 6.0-6.5mm | US lumber sizing |
| 8mm | 7.8-8.2mm | MDF typically accurate |
| 8.5mm | 8.3-8.7mm | uPVC utility board |

**Why it matters**: 0.2mm variation changes friction fit from perfect to loose/tight.

## Cutting Dividers

### Standard Lengths

**Recommended: 160mm**:

- Universal length for most home drawers
- Gridfinity-aligned: `42mm × 4 - Material_Thickness ≈ 160mm`
- Example: `42 × 4 - 8.5 = 159.5mm ≈ 160mm`
- Benefits: Flexible, works in many drawer sizes, easy to combine

**Custom lengths**:

- Formula: `(grid_size × N) - Material_Thickness`
- N = number of grid units to span
- Subtract material thickness to account for connector walls

### Cutting Tools

**MDF/Plywood**:

- Table saw (best for accuracy)
- Circular saw with guide
- Hand saw (slower, less accurate)
- Miter saw (if length allows)

**Acrylic**:

- Score and snap (3mm)
- Table saw with fine-tooth blade (6mm)
- Laser cutter (if available)

**Foam board**:

- Utility knife with straight edge
- Multiple light passes (don't force through)
- Self-healing cutting mat underneath

### Cutting Accuracy

**Target tolerance**: ±1mm on length

- Connectors have 3mm buffer (Partial_Channel_Buffer)
- Slight under-length is fine
- Over-length prevents top piece from seating

**Square edges critical**:

- Dividers must be 90° to connector base
- Use miter saw or table saw for square cuts
- Hand-sawn edges may need filing/sanding

## Surface Finishing

### MDF

**Must seal**:

- MDF absorbs moisture, swells
- Paint or primer all surfaces
- Measure thickness AFTER painting

**Process**:

1. Cut to size
2. Sand edges smooth (120 grit)
3. Prime all surfaces (spray primer easiest)
4. Light sand (220 grit)
5. Paint (2 coats)
6. Dry completely
7. Measure final thickness

### Plywood

**Optional finish**:

- Natural wood look: Clear coat (polyurethane/lacquer)
- Painted: Prime and paint like MDF
- Unfinished: Acceptable for drawer use

### Acrylic

**No finishing needed**:

- Use as-is (remove protective film)
- Optional: Polish cut edges with flame or buffing wheel

### Foam Board

**No finishing needed**:

- Lightweight option already has finished surface
- Don't paint (adds weight, reduces flexibility)

## Retention Spike Guidance

**When to use** `Retention_Spike = true`:

**MDF (soft material)**:

- Spikes grip into material for friction
- Prevents dividers from sliding in connectors
- Especially important for painted MDF (slicker surface)

**Plywood (medium hardness)**:

- Optional, test fit first
- Hardwood plywood: No spikes needed
- Softwood plywood: Spikes helpful

**Acrylic (hard material)**:

- **Never** use spikes
- Acrylic can crack from spike pressure
- Friction fit only

**Foam board (soft material)**:

- Spikes may help, but foam is fragile
- Test one connector first
- Consider friction fit only (spikes may tear foam)

## Assembly Best Practices

1. **Dry fit first**: Assemble without adhesive to verify layout
2. **Base placement**: Position bases on drawer bottom (Gridfinity baseplate or adhesive)
3. **Divider insertion**: Insert all dividers into bases before adding tops
4. **Top installation**: Press tops firmly until fully seated (should hear/feel click)
5. **Adjustments**: Reposition as needed (Gridfinity bases allow easy repositioning)

## Material Storage

**Before cutting**:

- Store sheets flat (prevent warping)
- Avoid moisture (especially MDF)
- Room temperature (thermal expansion minimal)

**After cutting**:

- Stack dividers flat with weights if needed
- Painted pieces: Dry flat for 24 hours
- Acrylic: Remove protective film only after cutting complete

## Common Material Issues

**MDF swelling**:

- Caused by moisture absorption
- Solution: Seal all edges with paint/primer
- Prevention: Store in dry location

**Plywood warping**:

- Thin plywood (3mm) most susceptible
- Solution: Use thicker stock (6mm+) or seal both sides
- Prevention: Store flat with weight

**Acrylic cracking**:

- Caused by impact or retention spikes
- Solution: Use friction fit only (no spikes)
- Prevention: Handle carefully, don't over-tighten in connectors

**Foam board crushing**:

- Caused by excessive pressure from connectors
- Solution: Increase Material_Thickness parameter by 0.1-0.2mm
- Prevention: Gentle assembly, don't force tops

## Cost Analysis Example

**3×3 grid in 300mm drawer**:

Components needed:

- 16 connectors (base + top each) = 800g filament
- 12 dividers @ 100mm each = ~0.4 square meters material

**Material costs**:

- MDF (8mm sheet): $8 (entire sheet, enough for multiple drawers)
- Plywood (6mm sheet): $12 (entire sheet)
- Acrylic (3mm sheet): $25 (entire sheet, premium option)
- Foam board (5mm): $3 (per board, may need 2)

**Filament costs** (at $20/kg):

- 800g = $16

**Total project**:

- MDF option: $16 filament + $8 material = $24
- Plywood option: $16 filament + $12 material = $28
- Acrylic option: $16 filament + $25 material = $41

**vs Fully 3D-printed**:

- 2kg filament @ $20/kg = $40 (just filament, no connectors)
- 60+ hours print time vs ~15 hours for connectors

**Result**: Hybrid approach saves $15-25 and 40+ hours even with material purchase.
