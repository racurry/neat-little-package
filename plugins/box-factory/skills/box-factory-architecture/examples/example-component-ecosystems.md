# Examples: Complete Component Ecosystems

## Example 1: Testing Ecosystem

**Architecture:**

```markdown
Commands (user-triggered):
├── /run-tests → Delegates to test-runner agent
└── /generate-tests → Delegates to test-generator agent

Agents (autonomous work):
├── test-runner
│   ├── Tools: Read, Bash, Grep
│   ├── Loads: testing-strategy skill
│   └── Purpose: Execute tests, analyze failures
│
└── test-generator
    ├── Tools: Read, Write, Glob
    ├── Loads: testing-strategy skill
    └── Purpose: Create test files from code

Skills (shared knowledge):
└── testing-strategy
    ├── Testing pyramid philosophy
    ├── When to mock patterns
    └── Test design principles

Hooks (enforcement):
└── PostToolUse:Write (*.test.*)
    └── Auto-format test files
```

**Interaction flow:**

```markdown
User: /run-tests
    ↓
Command executes → test-runner agent
    ├── Loads testing-strategy skill
    ├── Detects test framework (pytest/jest)
    ├── Runs tests via Bash tool
    ├── Analyzes failures
    └── Returns detailed report

Main Claude:
    ├── Receives report
    ├── Suggests fixes
    └── May delegate to test-generator for missing tests
```

## Example 2: Documentation Ecosystem

**Architecture:**

```markdown
Commands:
├── /document-api → Delegates to api-doc-generator
└── /review-docs → Delegates to doc-reviewer

Agents:
├── api-doc-generator
│   ├── Tools: Read, Write, WebFetch
│   ├── Loads: api-documentation-standards skill
│   └── Creates API documentation
│
└── doc-reviewer
    ├── Tools: Read, Grep
    ├── Loads: api-documentation-standards skill
    └── Reviews existing docs for compliance

Skills:
└── api-documentation-standards
    ├── OpenAPI specification patterns
    ├── Example formats
    └── Common pitfalls

Hooks:
└── PostToolUse:Write (*.md in docs/)
    └── Validates markdown syntax
```

## Example 3: Code Quality Enforcement Ecosystem

**Architecture:**

```markdown
Memory (always loaded):
└── CLAUDE.md
    └── "Use mr-sparkle plugin for linting"

Commands:
└── /lint <file> → Runs linting skill workflow

Skills:
└── linting
    ├── Tool selection per file type
    ├── Fallback patterns (biome → eslint+prettier)
    └── scripts/lint.py (executable helper)

Hooks (enforcement):
├── PostToolUse:Write → lint-on-write.py
│   └── Auto-lint after every file write
└── PostToolUse:Edit → lint-on-write.py
    └── Auto-lint after every file edit
```

**Interaction flow:**

```markdown
Claude writes file via Write tool
    ↓
PostToolUse hook triggers lint-on-write.py
    ├── Detects file type
    ├── Selects appropriate linter (ruff, biome, prettier, etc.)
    ├── Runs linter with auto-fix
    └── Returns success/failure

If formatting changes:
    └── File is already fixed (hook ran formatter)

No agent needed - enforcement is deterministic
```

**Why this works:**

- Hooks handle deterministic enforcement (no judgment)
- Skill provides guidance when user asks "how does linting work?"
- Command gives explicit control when user wants manual lint
- No agent needed - the task doesn't require reasoning
