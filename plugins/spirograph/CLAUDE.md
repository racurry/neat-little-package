# Spirograph Development Guidelines

## Philosophy

**Skills-Only Plugin**

Spirograph is a skills-only plugin - no agents, commands, or hooks. All functionality comes from interpretive guidance loaded when relevant.

**External Reference Pattern**

- Skills point to external sources (QuackWorks, official specs) rather than duplicating
- Fetch current specifications before generating code
- Code examples in `common_items/` subdirectories are reference patterns, not complete implementations

**System Ecosystem Approach**

- Home organization systems work together, not as alternatives
- Recommend combinations based on mounting surface and item characteristics
- Never recommend a single system in isolation without considering context

## Skill Structure

### home-organization

Decision framework for system selection. Contains:

- Reference doc pointers (`./gridfinity-reference.md`, etc.)
- Decision trees by mounting surface and item type
- Common combination patterns
- Quality checklist for recommendations

### OpenSCAD Generation Skills

Each system has a dedicated code generation skill:

| Skill | System | Key Pattern |
|-------|--------|-------------|
| `gridfinity-openscad` | Gridfinity bins/baseplates | 42mm grid, magnet mounts |
| `opengrid-openscad` | OpenGrid wall items | 28mm grid, MultiConnect backplate |
| `neogrid-openscad` | NeoGrid drawer dividers | Hybrid (print connectors, buy dividers) |
| `underware-openscad` | Underware cable channels | Parametric sizing, OpenGrid snap-in |

### Skill Subdirectories

OpenSCAD skills use subdirectories for reference patterns:

```text
skills/<name>/
├── SKILL.md              # Main guidance
├── common_items/         # Reference OpenSCAD modules
│   ├── basic_bin.md
│   └── ...
└── enhancements.md       # Optional feature modules
```

## Code Generation Patterns

### Required Elements

Every generated OpenSCAD file must include:

1. **User-facing parameters** at top (internal dimensions)
2. **Mounting integration** (MultiConnect for OpenGrid, magnet holes for Gridfinity)
3. **Grid-appropriate constants** (28mm for OpenGrid, 42mm for Gridfinity)
4. **Clearances** for item fit (typically +1mm)

### QuackWorks Integration

Advanced patterns reference QuackWorks repository:

- Fetch current code before generating (parameters evolve)
- BOSL2 library required for advanced patterns
- License: CC BY-NC-SA 4.0 (non-commercial)

## Quality Standards

### For System Recommendations

- Gather context first (mounting surface, item size, weight, aesthetics)
- Check interoperability matrix when combining systems
- Warn about weight limits (especially French Cleat plastic vs wood)
- Reference official specs for dimensions

### For Code Generation

- Parameterize everything (no magic numbers)
- Read pattern module from `common_items/` before generating
- Add comments explaining key calculations
- Include `$fn` for all curves/cylinders
- Validate mounting slot count (`floor(width/grid_spacing) >= 1`)

## Anti-Patterns

- Recommending single system without context
- Generating code without reading pattern module
- Hardcoding dimensions instead of calculating from parameters
- Suggesting fully 3D-printed NeoGrid (defeats hybrid purpose)
- Using plastic French Cleat for heavy items (>5kg)
