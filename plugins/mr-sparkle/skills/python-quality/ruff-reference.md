# Ruff Reference

This document provides a quick reference for ruff rule categories and common configuration patterns. For comprehensive documentation, fetch <https://docs.astral.sh/ruff/>.

## Rule Categories

Ruff organizes 800+ rules into categories based on the original tools they replace:

| Category | Tool Replaced | What It Checks |
|----------|---------------|----------------|
| **E/W** | pycodestyle | PEP 8 style (spacing, indentation, line length) |
| **F** | Pyflakes | Undefined names, unused imports, invalid syntax |
| **I** | isort | Import sorting and organization |
| **B** | flake8-bugbear | Likely bugs and design problems |
| **UP** | pyupgrade | Modernizations for newer Python syntax |
| **C4** | flake8-comprehensions | List/dict/set comprehension optimization |
| **SIM** | flake8-simplify | Code simplifications |
| **N** | pep8-naming | Naming conventions (PEP 8 compliance) |
| **D** | pydocstyle | Docstring format and completeness |
| **S** | flake8-bandit | Security vulnerabilities |
| **RET** | flake8-return | Return statement patterns |
| **PTH** | flake8-use-pathlib | Prefer pathlib over os.path |
| **DTZ** | flake8-datetimez | Timezone-related datetime issues |
| **LOG** | flake8-logging | Logging best practices |
| **PLR/PLE/PLC/PLW** | Pylint | Refactoring, errors, conventions, warnings |
| **RUF** | Ruff-specific | Custom rules unique to Ruff |

## Common Rule Selections

### Minimal (Errors Only)

```toml
[tool.ruff.lint]
select = ["E", "F"]  # pycodestyle errors + Pyflakes
```

**Use when:** Starting out, conservative linting

### Recommended (Default++)

```toml
[tool.ruff.lint]
select = ["E", "F", "W", "I"]  # Errors + warnings + imports
```

**Use when:** Standard Python projects

### Comprehensive

```toml
[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP", "C4", "SIM"]
```

**Use when:** High-quality codebase, want thorough checking

### Security-Focused

```toml
[tool.ruff.lint]
select = ["E", "F", "S", "B"]  # Errors + security + bugbear
```

**Use when:** Security-critical applications

### All Rules (Kitchen Sink)

```toml
[tool.ruff.lint]
select = ["ALL"]
ignore = [
    "D",     # Skip docstring checks (too noisy)
    "COM",   # Skip trailing commas (formatter handles)
]
```

**Use when:** Exploring all available checks, then whittle down

## Common Ignore Patterns

```toml
[tool.ruff.lint]
ignore = [
    "E501",   # Line too long (let formatter handle)
    "D100",   # Missing docstring in public module
    "D104",   # Missing docstring in public package
    "S101",   # Use of assert (OK in tests)
    "PLR0913", # Too many arguments
]
```

## Per-File Ignores

```toml
[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]  # Allow assert in tests
"__init__.py" = ["F401"]    # Allow unused imports (re-exports)
"scripts/*.py" = ["T201"]   # Allow print() in scripts
```

## Formatting Configuration

```toml
[tool.ruff.format]
quote-style = "double"           # "" instead of ''
indent-style = "space"           # Spaces, not tabs
skip-magic-trailing-comma = false # Respect trailing commas
line-ending = "auto"             # Platform-appropriate
```

## Target Version

```toml
[tool.ruff]
target-version = "py312"  # Adjust to your minimum Python version
```

**Effect:** Determines which UP (pyupgrade) rules apply.

## Line Length

```toml
[tool.ruff]
line-length = 88  # Black default

# Or more conservative:
line-length = 79  # PEP 8 default
```

## Fixable Rules

```toml
[tool.ruff.lint]
fixable = ["ALL"]     # Auto-fix everything possible
unfixable = []        # Don't auto-fix anything specific

# Or more conservative:
fixable = ["I", "UP", "C4"]  # Only fix safe categories
unfixable = ["B", "SIM"]     # Don't touch logic changes
```

## Common Commands

### Linting

```bash
ruff check .                    # Check all files
ruff check --fix .              # Check and auto-fix
ruff check --fix --unsafe-fixes . # Include unsafe fixes
ruff check file.py              # Check single file
```

### Formatting

```bash
ruff format .                   # Format all files
ruff format --check .           # Check formatting (CI)
ruff format file.py             # Format single file
```

### Combined Workflow

```bash
ruff check --fix . && ruff format .
```

## Exit Codes

- `0` - No issues (or all fixed)
- `1` - Issues found
- `2` - Invalid configuration

## Cache Behavior

Ruff caches results in `.ruff_cache/` by default.

**Clear cache:**

```bash
ruff clean
```

## Integration with Other Tools

### With Black

If migrating from Black, ruff's formatter is designed to be compatible:

```toml
[tool.ruff]
line-length = 88  # Match Black default

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### With isort

Ruff's `I` rules replace isort:

```toml
[tool.ruff.lint]
select = ["I"]

[tool.ruff.lint.isort]
known-first-party = ["myproject"]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]
```

### With mypy

Ruff and mypy are complementary (ruff doesn't do type checking):

```bash
ruff check --fix . && ruff format . && mypy .
```

## Official Documentation

For complete rule reference and configuration options:

- <https://docs.astral.sh/ruff/> - Main documentation
- <https://docs.astral.sh/ruff/rules/> - All 800+ rules
- <https://docs.astral.sh/ruff/configuration/> - Configuration reference
- <https://docs.astral.sh/ruff/formatter/> - Formatter documentation
