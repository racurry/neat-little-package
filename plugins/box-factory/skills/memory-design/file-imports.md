# File Imports

Import external files into CLAUDE.md using `@path/to/import` syntax.

## Syntax (Official Specification)

```markdown
See @README for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md

# Individual Preferences (user-specific imports)
- @~/.claude/my-project-instructions.md
```

**Behavior:**

- Supports both relative and absolute paths
- Tilde expansion for home directory
- **Not evaluated inside markdown code spans or code blocks**
- Recursive imports allowed (max 5 hops)
- View loaded imports with `/memory` command

## Use Cases

- Importing shared documentation (README, package.json)
- Team members providing individual instructions via home dir
- Alternative to CLAUDE.local.md that works across git worktrees
- Modular organization without rules/ directory

## When to Use Imports vs Rules Directory (Best Practices)

**Use imports when:**

- Referring to existing project documentation
- Individual team members have personal instruction files
- Working with multiple git worktrees (imports > CLAUDE.local.md)
- Simple modular organization sufficient

**Use .claude/rules/ when:**

- Creating new Claude-specific instruction files
- Want path-specific conditional rules
- Need subdirectory organization by domain
- Prefer discovery via directory structure

**Hybrid approach is valid:**

```markdown
# CLAUDE.md
@README.md  # Import existing docs

See .claude/rules/ for:
- code-style.md - Project code standards
- testing.md - Test conventions
```

## Import Cycle Prevention

**Problem:** Recursive imports can create cycles

❌ Bad:

```
# CLAUDE.md
@.claude/extra.md

# .claude/extra.md
@CLAUDE.md  # Cycle!
```

**Solution:** Design import hierarchy like dependency tree (no cycles)

✅ Better:

```
CLAUDE.md
├── @docs/architecture.md
└── @docs/workflows.md
    └── @docs/testing.md  # Linear, no cycles
```

**Max depth:** 5 hops - Design imports to stay well under this limit

## Quality Checklist

- ✓ Import syntax only in CLAUDE.md content (not in code blocks)
- ✓ No import cycles
- ✓ Import depth < 3 hops (well under 5 limit)
- ✓ Imports point to stable, maintained files
