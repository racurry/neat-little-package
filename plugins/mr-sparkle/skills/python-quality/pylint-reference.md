# Pylint Reference

This document provides a quick reference for pylint configuration. For comprehensive documentation, fetch <https://pylint.readthedocs.io/>.

## Purpose

Pylint is a comprehensive Python linter that checks for:

- **Errors** - Likely bugs and logic problems
- **Warnings** - Stylistic problems or minor issues
- **Refactoring** - Code that could be simplified
- **Conventions** - Coding standard violations
- **Code quality** - Maintainability metrics

## Message Categories

Pylint organizes messages into categories:

| Category | Prefix | Examples |
|----------|--------|----------|
| **Convention** | C | C0103 (invalid-name), C0114 (missing-module-docstring) |
| **Refactor** | R | R0913 (too-many-arguments), R1705 (no-else-return) |
| **Warning** | W | W0612 (unused-variable), W0621 (redefined-outer-name) |
| **Error** | E | E0401 (import-error), E1101 (no-member) |
| **Fatal** | F | F0001 (syntax-error) |

## Common Configuration

### Basic Configuration

```toml
[tool.pylint.main]
jobs = 0  # Use all CPU cores

[tool.pylint.messages_control]
disable = [
    "C0103",  # invalid-name (too strict for some projects)
    "C0114",  # missing-module-docstring
    "C0115",  # missing-class-docstring
    "C0116",  # missing-function-docstring
]

[tool.pylint.format]
max-line-length = 88  # Match Black/ruff
```

### Message Control

```toml
[tool.pylint.messages_control]
disable = [
    "missing-docstring",  # Can specify by name or code
    "too-many-arguments",
    "too-many-locals",
]

enable = [
    "useless-suppression",  # Warn about unnecessary disables
]
```

### Code Quality Limits

```toml
[tool.pylint.design]
max-args = 5              # Maximum function arguments
max-locals = 15           # Maximum local variables
max-returns = 6           # Maximum return statements
max-branches = 12         # Maximum branches in function
max-statements = 50       # Maximum statements in function
max-attributes = 7        # Maximum class attributes

[tool.pylint.format]
max-line-length = 88
max-module-lines = 1000   # Maximum lines per module
```

### Naming Conventions

```toml
[tool.pylint.basic]
good-names = ["i", "j", "k", "x", "y", "z", "ex", "Run", "_"]
```

**Default patterns:** Pylint expects PEP 8 naming by default:

- `snake_case` for functions, variables, modules
- `PascalCase` for classes
- `UPPER_CASE` for constants

## Common Commands

### Check Files

```bash
pylint .                   # Check all Python files
pylint file.py             # Check single file
pylint mypackage/          # Check specific package
```

### Output Formats

```bash
pylint --output-format=colorized .     # Colored output
pylint --output-format=json .          # JSON output
pylint --output-format=parseable .     # Machine-readable
```

### Score Display

```bash
pylint --score=no .        # Hide score
pylint --score=yes .       # Show score (default)
```

### Generate Config

```bash
pylint --generate-rcfile > .pylintrc   # Generate full config
```

## Inline Disables

### Disable for Line

```python
import sys  # pylint: disable=unused-import
```

### Disable for Block

```python
# pylint: disable=too-many-arguments
def complex_function(a, b, c, d, e, f):
    pass
# pylint: enable=too-many-arguments
```

### Disable for File

```python
# pylint: disable=missing-docstring,invalid-name
"""Module without detailed configuration."""
```

### Disable by Category

```python
# pylint: disable=C  # Disable all convention messages
```

## Configuration File Locations

Pylint looks for configuration in this order:

1. `pyproject.toml` (`[tool.pylint.X]`)
2. `.pylintrc` or `pylintrc` in project directory
3. `setup.cfg` (`[pylint.X]`)
4. `~/.pylintrc` (user-level)

**Recommendation:** Use `pyproject.toml` for consistency.

## Common Pitfalls

### Pitfall 1: Too Strict Naming Conventions

**Problem:** Pylint complains about common variable names.

```python
# Pylint error: C0103 (invalid-name)
df = pd.read_csv("data.csv")  # Common in data science
```

**Solution:**

```toml
[tool.pylint.basic]
good-names = ["i", "j", "k", "df", "x", "y", "z", "_"]
```

### Pitfall 2: Unrealistic Complexity Limits

**Problem:** Legitimate complex functions trigger refactoring warnings.

**Solution:** Adjust limits or disable for specific cases:

```toml
[tool.pylint.design]
max-args = 7              # More realistic for real projects
max-branches = 15
```

### Pitfall 3: False Positive Import Errors

**Problem:** Pylint can't find imports that exist (virtual environments, dynamic imports).

```python
import third_party  # E0401: Unable to import 'third_party'
```

**Solution:**

```toml
[tool.pylint.messages_control]
disable = ["import-error"]
```

Or use inline disable:

```python
import third_party  # pylint: disable=import-error
```

### Pitfall 4: Docstring Requirements Too Strict

**Problem:** Requiring docstrings for every function is often excessive.

**Solution:**

```toml
[tool.pylint.messages_control]
disable = [
    "missing-module-docstring",
    "missing-class-docstring",
    "missing-function-docstring",
]
```

Enable only for public APIs.

### Pitfall 5: Line Length Conflicts

**Problem:** Pylint's default 100-char limit conflicts with Black's 88.

**Solution:**

```toml
[tool.pylint.format]
max-line-length = 88  # Match Black
```

Or disable entirely (let formatter handle):

```toml
[tool.pylint.messages_control]
disable = ["line-too-long"]
```

## Integration Patterns

### With Black/isort

Pylint checks logic; Black/isort handle formatting:

```bash
isort . && black . && pylint .
```

**Configuration alignment:**

```toml
[tool.black]
line-length = 88

[tool.isort]
profile = "black"
line_length = 88

[tool.pylint.format]
max-line-length = 88
```

### With Ruff

Ruff's `PLR/PLE/PLC/PLW` rules replicate many pylint checks. Consider:

- Use ruff for speed and auto-fixes
- Use pylint for thorough analysis and complex checks ruff doesn't cover

**Hybrid approach:**

```bash
ruff check --fix . && ruff format . && pylint .
```

### Exit Codes

- `0` - No issues
- `1` - Fatal message issued
- `2` - Error message issued
- `4` - Warning message issued
- `8` - Refactor message issued
- `16` - Convention message issued
- `32` - Usage error

**Note:** Exit codes are bitwise OR'd (e.g., 6 = 2 + 4 means errors and warnings).

## Typical Complete Configuration

A balanced pylint configuration for modern projects:

```toml
[tool.pylint.main]
jobs = 0  # Use all CPU cores

[tool.pylint.messages_control]
disable = [
    "missing-docstring",      # Let type hints serve as documentation
    "too-few-public-methods", # Sometimes classes are simple
    "invalid-name",           # Sometimes short names are fine
    "line-too-long",          # Let formatter handle
]

[tool.pylint.format]
max-line-length = 88

[tool.pylint.design]
max-args = 7
max-locals = 20
max-branches = 15
max-statements = 60
```

## Official Documentation

For complete reference:

- <https://pylint.readthedocs.io/> - Main documentation
- <https://pylint.readthedocs.io/en/latest/user_guide/messages/> - All messages
- <https://pylint.readthedocs.io/en/latest/user_guide/configuration/> - Configuration reference
