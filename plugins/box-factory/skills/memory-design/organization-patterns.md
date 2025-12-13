# Organization Patterns

Common patterns for structuring Claude Code memory across projects.

## Pattern 1: Simple Project (Monolithic)

```
project/
├── CLAUDE.md              # All project memory (< 200 lines)
└── CLAUDE.local.md        # Personal overrides
```

**When to use:** Small projects, simple conventions, interconnected guidance

## Pattern 2: Modular Project (Rules Directory)

```
project/
├── .claude/
│   ├── CLAUDE.md          # Overview + common instructions (~50 lines)
│   └── rules/
│       ├── code-style.md  # Language-agnostic style rules
│       ├── testing.md     # Testing conventions
│       ├── api-design.md  # API standards
│       └── security.md    # Security requirements
```

**When to use:** Growing projects, multiple independent domains, >200 total lines

## Pattern 3: Domain-Organized Project

```
project/
├── .claude/
│   ├── CLAUDE.md
│   └── rules/
│       ├── frontend/
│       │   ├── react.md        # paths: src/frontend/**/*.tsx
│       │   └── styles.md       # paths: src/frontend/**/*.css
│       ├── backend/
│       │   ├── api.md          # paths: src/api/**/*.ts
│       │   └── database.md     # paths: src/db/**/*
│       └── general.md          # No paths (unconditional)
```

**When to use:** Clear frontend/backend separation, different conventions per domain

## Pattern 4: Shared Rules with Symlinks

```
project/
├── .claude/
│   ├── CLAUDE.md
│   └── rules/
│       ├── company-security.md -> ~/shared-claude-rules/security.md
│       ├── company-style.md -> ~/shared-claude-rules/code-style.md
│       └── project-specific.md  # Project-only rules
```

**When to use:** Multiple projects share common company standards

## Pattern 5: User-Level + Project Rules

```
~/.claude/
├── CLAUDE.md              # Personal preferences all projects
└── rules/
    ├── preferences.md     # Your coding style
    └── workflows.md       # Your preferred workflows

project/
├── .claude/
│   ├── CLAUDE.md          # Project conventions
│   └── rules/             # Project-specific rules
```

**When to use:** Want personal preferences across all projects + project-specific rules

## "One Topic Per File" Principle

Each rule file should focus on a single cohesive topic.

**Good examples:**

- ✅ `testing.md` - All testing conventions (unit, integration, mocking)
- ✅ `api-design.md` - REST API standards (endpoints, errors, versioning)
- ✅ `security.md` - Security practices (auth, secrets, validation)

**Bad examples:**

- ❌ `backend.md` - Too broad (testing, API design, database, etc.)
- ❌ `style-and-testing.md` - Multiple unrelated topics
- ❌ `miscellaneous.md` - Kitchen sink file

**Test:** Can you describe the file's purpose in one sentence without using "and"?

- ✅ "Testing conventions" (focused)
- ❌ "Testing and security and code style" (unfocused)

**Benefits:**

- Easy to find relevant rules
- Can evolve topics independently
- Clear ownership per domain
- Path-specific rules make more sense
