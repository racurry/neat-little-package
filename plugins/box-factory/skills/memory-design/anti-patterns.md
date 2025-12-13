# Memory Anti-Patterns

Common mistakes when organizing Claude Code memory and how to fix them.

## Anti-Pattern #1: Duplicate Rules Across Files

**Problem:** Same rule in multiple files

```
# code-style.md
- Use 2-space indentation for TypeScript

# typescript.md
- Use 2-space indentation

# frontend/react.md
- Use 2-space indentation for React components
```

**Why it fails:** Maintenance burden, inconsistency risk, token waste

**Better:** Single source of truth

```
# code-style.md (unconditional)
- Use 2-space indentation for all code

# No duplication in other files
```

## Anti-Pattern #2: Path-Specific for Project-Wide Rules

**Problem:** Using `paths` for rules that should apply everywhere

```markdown
---
paths: src/**/*
---

# Code Style

- Write clear, maintainable code
- Use meaningful variable names
```

**Why it fails:** These rules apply everywhere, `paths` is unnecessary restriction

**Better:** Omit `paths` field (unconditional)

## Anti-Pattern #3: Too Many Granular Files

**Problem:** Over-modularization

```
.claude/rules/
├── indentation.md        # 3 lines
├── semicolons.md         # 2 lines
├── quotes.md             # 2 lines
├── imports.md            # 4 lines
└── [50 more tiny files]
```

**Why it fails:** Organization overhead exceeds benefit, discovery harder

**Better:** Group related rules

```
.claude/rules/
├── code-style.md         # Indentation, semicolons, quotes, imports
├── testing.md            # Test patterns
└── security.md           # Security practices
```

**Guideline:** Each file should have >20 lines of substantive content

## Anti-Pattern #4: Putting Secrets in Memory

**Problem:** Storing credentials in committed CLAUDE.md

```markdown
# CLAUDE.md (in git)
- Database password: super-secret-123
- API key: sk-abc123xyz
```

**Why it fails:** Security risk, credentials in version control

**Better:** Use CLAUDE.local.md (gitignored)

```markdown
# CLAUDE.local.md (gitignored)
- Database password: super-secret-123
- Local API endpoint: http://localhost:3000
```

## Anti-Pattern #5: Overly Complex Path Globs

**Problem:** Path patterns that are hard to understand

```yaml
paths: "{src/{api,services,utils},lib/{core,shared}}/{!(test),__tests__}/**/*.{ts,tsx,!(spec|test).js}"
```

**Why it fails:** Unreadable, error-prone, hard to maintain, over-engineered

**Better:** Split into multiple simpler rules or make unconditional

```yaml
paths: "{src,lib}/**/*.{ts,tsx}"
```

## Anti-Pattern #6: Import Depth Explosion

**Problem:** Deep import chains approaching the 5-hop limit

```
CLAUDE.md
  └─ @a.md
      └─ @b.md
          └─ @c.md
              └─ @d.md
                  └─ @e.md  # At limit!
```

**Why it fails:** Fragile, hard to debug, hits recursion limit

**Better:** Flatten hierarchy

```
CLAUDE.md
  ├─ @a.md
  ├─ @b.md
  └─ @c.md  # Max 1-2 levels deep
```

## Quick Reference

| Anti-Pattern          | Fix                            |
| --------------------- | ------------------------------ |
| Duplicate rules       | Single source of truth         |
| Path-specific for all | Remove `paths` field           |
| Too many tiny files   | Group into >20 line files      |
| Secrets in git        | Use CLAUDE.local.md            |
| Complex globs         | Simplify or make unconditional |
| Deep import chains    | Flatten to 1-2 levels          |
