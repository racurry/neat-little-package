---
name: python-quality
description: Interpretive guidance for Python code quality using ruff (modern) or pylint+isort+black (traditional). Use when linting Python files, configuring Python tools, troubleshooting lint errors, or understanding tool selection.
---

# Python Quality Skill

This skill teaches how to apply Python linting and formatting tools effectively using mr-sparkle's tool selection system. It provides guidance on what the tools do, when each tool group is used, and how our configuration balances modern tooling with backward compatibility.

## Official Documentation

Claude knows how to use ruff, black, isort, and pylint. Fetch these docs only when you need:

- Specific rule codes or error messages you don't recognize
- Advanced configuration options
- Recent feature changes

**Reference URLs:**

- **<https://docs.astral.sh/ruff/>** - Ruff rules and configuration
- **<https://black.readthedocs.io/en/stable/>** - Black configuration options
- **<https://pycqa.github.io/isort/>** - isort profiles and settings
- **<https://pylint.readthedocs.io/>** - Pylint message codes

## Core Understanding

### Tool Selection Philosophy

**Key principle:** Prefer modern unified tooling (ruff) when project has it configured; fall back to traditional tools (pylint+isort+black) when they're configured; default to ruff if no configuration exists.

**What this means:**

- **Ruff preferred** - Single tool replacing multiple legacy tools, 10-100x faster
- **Project config wins** - Respects existing project tooling choices
- **Smart fallback** - Uses traditional tools if project has them configured
- **Zero-config default** - Falls back to ruff with sensible defaults

**Decision test:** Does the project have explicit tool configuration? Use configured tools. Otherwise use ruff.

### How Tool Selection Works

The linting system uses **group-based priority selection** for Python files:

```text
Priority 1: ruff (if project has ruff config)
    ↓
Priority 2: pylint + isort + black (if project has any of their configs)
    ↓
Fallback: ruff (with default config)
```

**Detection logic:**

1. Find project root (`pyproject.toml`, `package.json`, or `.git`)
2. Check for ruff configuration (first group)
3. Check for pylint/isort/black configuration (second group)
4. If no config found, use ruff with `default-ruff.toml`

**All tools in winning group run sequentially** (e.g., if isort config exists, runs pylint → isort → black).

## Ruff: Modern Unified Tool (Official Specification)

**From official docs:**

- **Purpose:** Extremely fast Python linter and formatter written in Rust
- **Capabilities:** 800+ built-in linting rules + code formatting
- **Replaces:** Flake8, Black, isort, pydocstyle, pyupgrade, autoflake
- **Performance:** 10-100x faster than traditional Python tools
- **Commands:** `ruff check --fix` (linting) then `ruff format` (formatting)

**Configuration locations:**

- `ruff.toml` or `.ruff.toml` (dedicated config)
- `[tool.ruff]` section in `pyproject.toml`

## Ruff: Modern Unified Tool (Best Practices)

**When ruff shines:**

- ✅ New projects (no legacy tooling)
- ✅ Large codebases (speed matters)
- ✅ Want single tool instead of chain
- ✅ Need drop-in Flake8/Black/isort compatibility

**Basic configuration pattern:**

```toml
# pyproject.toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "W", "I"]  # Error, Flake8, Warning, Import
fixable = ["ALL"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

**Rule selection:**

- `E` - pycodestyle errors
- `F` - Pyflakes (basic static analysis)
- `W` - pycodestyle warnings
- `I` - isort import sorting
- Many more: `B` (bugbear), `UP` (pyupgrade), `C4` (comprehensions), etc.

See `ruff-reference.md` for common rule categories and `default-ruff.toml` for our opinionated defaults.

## Traditional Tools: pylint + isort + black (Official Specification)

**From official docs:**

**Pylint:**

- Traditional comprehensive Python linter
- Checks code quality, errors, style conventions
- More thorough but slower than modern tools
- Command: `pylint <file>`

**isort:**

- Dedicated import sorting utility
- Alphabetical sorting with section separation (stdlib, third-party, local)
- Command: `isort <file>`

**black:**

- "Uncompromising" opinionated code formatter
- "Black is opinionated so you don't have to be"
- AST-safe formatting (verifies output produces equivalent code)
- Command: `black <file>`

**Configuration locations:**

- `pyproject.toml` (`[tool.pylint]`, `[tool.isort]`, `[tool.black]`)
- `setup.cfg` (`[pylint]`, `[isort]` sections)
- Dedicated files (`.pylintrc`, `.isort.cfg`)

## Traditional Tools (Best Practices)

**When traditional tools make sense:**

- ✅ Existing projects with established configs
- ✅ Team familiarity with pylint's comprehensive checks
- ✅ Projects that haven't migrated to ruff yet
- ✅ Need pylint's specific error detection capabilities

**Running order matters:**

1. **pylint** - Linting (doesn't modify files)
2. **isort** - Import sorting (modifies files)
3. **black** - Code formatting (modifies files)

**Why this order:** Linting first (non-destructive), then imports, then formatting last to clean up.

## Tool Selection in Practice (Best Practices)

### Scenario 1: New project, no config

```bash
$ lint.py file.py
# Runs: ruff check --fix, ruff format
# Uses: default-ruff.toml from skill directory
```

### Scenario 2: Project with ruff config

```bash
# pyproject.toml has [tool.ruff]
$ lint.py file.py
# Runs: ruff check --fix, ruff format
# Uses: project's pyproject.toml config
```

### Scenario 3: Project with traditional tools

```bash
# pyproject.toml has [tool.black] or setup.cfg has [isort]
$ lint.py file.py
# Runs: pylint, isort, black
# Uses: project's existing config
```

### Scenario 4: Mixed config (ruff wins)

```bash
# pyproject.toml has both [tool.ruff] and [tool.black]
$ lint.py file.py
# Runs: ruff only (first group with config wins)
```

## Common Configuration Patterns

### Ruff Configuration

**Minimal (uses defaults):**

```toml
[tool.ruff]
# That's it - uses built-in defaults
```

**Typical project:**

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP"]
ignore = ["E501"]  # Line too long (let formatter handle)
fixable = ["ALL"]

[tool.ruff.format]
quote-style = "double"
```

**See `default-ruff.toml`** for our opinionated baseline configuration.

### Black Configuration

**Minimal:**

```toml
[tool.black]
line-length = 88
target-version = ['py312']
```

**With exclusions:**

```toml
[tool.black]
line-length = 88
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''
```

### isort Configuration

**Black-compatible:**

```toml
[tool.isort]
profile = "black"  # Ensures isort doesn't conflict with black
```

**Custom sections:**

```toml
[tool.isort]
profile = "black"
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
known_first_party = ["myproject"]
```

## Common Pitfalls

### Pitfall #1: Conflicting Tool Configurations

**Problem:** Black and isort fight over import formatting.

```toml
# ❌ Conflicting configs
[tool.isort]
line_length = 79

[tool.black]
line-length = 88
```

**Why it fails:** Tools produce different output, causing formatting loops.

**Better:**

```toml
# ✅ Aligned configs
[tool.isort]
profile = "black"  # Defers to black's style
line_length = 88

[tool.black]
line-length = 88
```

### Pitfall #2: Ignoring Auto-Fixable Issues

**Problem:** Manually fixing issues that tools can fix automatically.

**Why it fails:** Wastes time, may introduce inconsistencies.

**Better:** Let `ruff check --fix` or `black` + `isort` handle formatting. Focus on logic errors and design issues.

### Pitfall #3: Over-Configuring Ruff

**Problem:** Trying to replicate entire pylint configuration in ruff.

**Why it fails:** Ruff has different rule categories and defaults. Start with basics, add rules incrementally.

**Better:**

```toml
# ✅ Start simple
[tool.ruff.lint]
select = ["E", "F"]  # Just errors and pyflakes
fixable = ["ALL"]

# Then add more as needed:
# select = ["E", "F", "W", "I", "B"]
```

### Pitfall #4: Not Running Tools in Order

**Problem:** Running black before isort.

**Why it fails:** Black may reformat what isort just organized, or vice versa.

**Better:** Always: `isort` → `black` (imports first, then formatting). The linting system handles this automatically.

### Pitfall #5: Disabling Too Many Rules

**Problem:** Ignoring rules because "they're annoying."

```toml
# ❌ Over-ignoring
[tool.ruff.lint]
ignore = ["E501", "F401", "F841", "E402", ...]  # Too many
```

**Why it fails:** Defeats the purpose of linting. Rules exist for good reasons.

**Better:** Understand why rules trigger, fix the code, or selectively ignore with inline comments:

```python
# Selective ignore when truly needed
import unused_but_required  # noqa: F401
```

## Automatic Hook Behavior

The mr-sparkle plugin's linting hook:

1. Triggers after Write and Edit operations
2. Detects Python files (`.py`)
3. Runs selected tools automatically (ruff OR pylint+isort+black)
4. Applies auto-fixes where possible
5. Reports unfixable issues (non-blocking)
6. Silently skips if tools not installed

**What this means:** Most formatting issues auto-fix on save. Pay attention to reported unfixable issues.

## Quality Checklist

**Before finalizing Python code:**

**Auto-fixable (tools handle):**

- ✓ Import sorting and organization
- ✓ Line length and wrapping
- ✓ Quote style consistency
- ✓ Trailing whitespace
- ✓ Blank line conventions
- ✓ Unused imports (ruff only)

**Manual attention required:**

- ✓ Undefined variables
- ✓ Logic errors
- ✓ Type inconsistencies
- ✓ Complexity warnings
- ✓ Naming conventions
- ✓ Documentation completeness

## CLI Tool Usage

The universal linting script handles Python files automatically:

```bash
# Lint Python file (applies fixes)
./plugins/mr-sparkle/skills/linting/scripts/lint.py file.py

# JSON output for programmatic use
./plugins/mr-sparkle/skills/linting/scripts/lint.py file.py --format json
```

**Exit codes:**

- `0` - Clean or successfully fixed
- `1` - Lint errors found (non-blocking)
- `2` - Tool execution error

See `linting` skill for complete CLI documentation.

## Reference Documentation

**Detailed guides** (loaded on-demand for progressive disclosure):

- `ruff-reference.md` - Ruff rule categories and common configurations
- `black-reference.md` - Black philosophy and configuration patterns
- `isort-reference.md` - Import organization strategies
- `pylint-reference.md` - Pylint configuration and rule categories
- `default-ruff.toml` - Our opinionated ruff defaults

**Official documentation to fetch:**

- <https://docs.astral.sh/ruff/> - Ruff documentation and rule reference
- <https://black.readthedocs.io/> - Black formatter documentation
- <https://pycqa.github.io/isort/> - isort import sorting
- <https://pylint.readthedocs.io/> - Pylint linter documentation
- <https://peps.python.org/pep-0008/> - PEP 8 style guide

**Remember:** This skill documents mr-sparkle's tool selection logic. Fetch official docs when you need specific rule definitions or configuration syntax you're unsure about.
