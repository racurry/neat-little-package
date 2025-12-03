# Black Reference

This document provides a quick reference for Black configuration. For comprehensive documentation, fetch <https://black.readthedocs.io/>.

## Philosophy

Black is opinionated so you don't have to be.

Black makes almost all formatting decisions for you. Configuration options are deliberately minimal to enforce consistency across the Python ecosystem.

## Core Behavior

**What Black does:**

- Reformats entire files to a consistent style
- Validates output produces equivalent AST (ensures no behavior changes)
- Makes code review faster (fewer style debates, minimal diffs)
- Deterministic output (same input always produces same output)

**What Black doesn't do:**

- Fix linting errors (use ruff/pylint for that)
- Organize imports (use isort or ruff's `I` rules)
- Remove unused code
- Change code logic

## Configuration Options

Black has few configuration options by design. Most projects need minimal config.

### Line Length

```toml
[tool.black]
line-length = 88  # Default
```

**Common alternatives:**

- `79` - PEP 8 traditional
- `100` - Wider for modern displays
- `120` - Very wide (less common)

### Target Version

```toml
[tool.black]
target-version = ["py312"]  # Or your minimum Python version
```

**Effect:** Determines which syntax features Black uses when formatting.

### String Normalization

```toml
[tool.black]
skip-string-normalization = false  # Default: normalize to "
```

**Default behavior:** Converts `'single'` quotes to `"double"` quotes.

**Set to `true`** if you prefer single quotes or have legacy code.

### Magic Trailing Comma

```toml
[tool.black]
skip-magic-trailing-comma = false  # Default: respect trailing commas
```

**Default behavior:** Trailing comma signals "keep this on multiple lines."

```python
# With trailing comma - stays multiline even if short
my_list = [
    1,
    2,
]

# Without trailing comma - may collapse to single line
my_list = [1, 2]
```

### Exclude Patterns

```toml
[tool.black]
exclude = '''
/(
    \.git
  | \.venv
  | \.mypy_cache
  | \.tox
  | build
  | dist
  | migrations
)/
'''
```

### Include Patterns

```toml
[tool.black]
include = '\.pyi?$'  # .py and .pyi files
```

### Preview Mode

```toml
[tool.black]
preview = true  # Enable unstable style changes
```

**Use when:** Want to try upcoming style changes before they're stable.

## Common Commands

### Format Files

```bash
black .                    # Format all files in directory
black file.py              # Format single file
black src/ tests/          # Format specific directories
```

### Check Only (CI)

```bash
black --check .            # Exit 1 if formatting needed
black --diff .             # Show what would change
black --check --diff .     # Both
```

### Verbose Output

```bash
black --verbose .          # Show files being processed
```

### Fast Mode

```bash
black --fast .             # Skip AST safety check
```

**Warning:** Only use `--fast` if you're confident in Black's safety.

## Integration Patterns

### With isort

Black and isort can conflict on import formatting. Use isort's `black` profile:

```toml
[tool.black]
line-length = 88

[tool.isort]
profile = "black"  # Ensures compatibility
line_length = 88   # Match Black's line length
```

**Run order:** `isort` first, then `black`:

```bash
isort . && black .
```

### With Ruff

Ruff's formatter is designed to be Black-compatible. If migrating from Black to ruff:

```toml
[tool.ruff]
line-length = 88

[tool.ruff.format]
quote-style = "double"        # Match Black's default
indent-style = "space"
skip-magic-trailing-comma = false  # Match Black's behavior
```

### With Pre-commit

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1  # Use latest version
    hooks:
      - id: black
```

## Exit Codes

- `0` - Files are formatted correctly (or were formatted successfully)
- `1` - Files need formatting (when using `--check`)
- `123` - Internal error

## Common Pitfalls

### Pitfall 1: Fighting Black's Decisions

**Problem:** Trying to manually format code that Black reformats differently.

**Solution:** Trust Black's decisions. Focus on code logic, not formatting.

### Pitfall 2: Per-File Style Variations

**Problem:** Wanting different formatting in different files.

**Solution:** Black intentionally doesn't support this. Consistency is the goal.

### Pitfall 3: Over-Long Lines Black Can't Fix

**Problem:** Black respects string literals and comments that exceed line length.

```python
# Black can't break this:
x = "This is an extremely long string literal that exceeds the line length limit"
```

**Solution:** Manually break long strings:

```python
x = (
    "This is an extremely long string literal "
    "that exceeds the line length limit"
)
```

### Pitfall 4: Conflicting with isort

**Problem:** Black and isort disagree on import formatting.

**Solution:** Use isort's `profile = "black"` configuration.

### Pitfall 5: Expecting Black to Fix Linting Errors

**Problem:** Black doesn't remove unused imports, fix undefined variables, etc.

**Solution:** Use Black for formatting, ruff/pylint for linting.

## Disabling Black for Specific Code

### Single Line

```python
# fmt: off
weird_formatting = [1,2,3,4,5,6,7,8,9]
# fmt: on
```

### Block

```python
# fmt: off
matrix = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
]
# fmt: on
```

**Use sparingly:** Only when specific formatting is truly necessary (e.g., matrices, tables).

## Typical Complete Configuration

Most projects need very little configuration:

```toml
[tool.black]
line-length = 88
target-version = ["py312"]
```

That's it. Black handles the rest.

## Official Documentation

For complete reference:

- <https://black.readthedocs.io/> - Main documentation
- <https://black.readthedocs.io/en/stable/usage_and_configuration/> - Configuration reference
- <https://black.readthedocs.io/en/stable/the_black_code_style/> - Style guide
