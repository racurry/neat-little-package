# isort Reference

This document provides a quick reference for isort configuration. For comprehensive documentation, fetch <https://pycqa.github.io/isort/>.

## Purpose

isort automatically sorts and organizes Python imports into standardized sections with consistent ordering.

## Default Behavior

**Import sections (in order):**

1. **FUTURE** - `from __future__ import ...`
2. **STDLIB** - Standard library imports
3. **THIRDPARTY** - Third-party library imports
4. **FIRSTPARTY** - Project's own modules
5. **LOCALFOLDER** - Relative imports (`.module`)

**Within each section:**

- Alphabetical sorting
- `import` statements before `from ... import ...`
- Line wrapping for long import lists

## Common Configuration

### Black-Compatible (Recommended)

```toml
[tool.isort]
profile = "black"  # Ensures isort doesn't conflict with Black
```

**This is the most important setting** when using Black or ruff formatting.

### Basic Configuration

```toml
[tool.isort]
line_length = 88              # Match your formatter's line length
multi_line_output = 3         # Vertical hanging indent
include_trailing_comma = true # Add trailing comma on multiline
force_grid_wrap = 0          # Don't force grid wrapping
use_parentheses = true       # Use parentheses for line continuation
ensure_newline_before_comments = true
```

**Note:** `profile = "black"` sets all of these automatically.

### Custom First-Party

```toml
[tool.isort]
profile = "black"
known_first_party = ["myproject", "mypackage"]
```

**Effect:** Tells isort which packages are part of your project (for proper section placement).

### Custom Sections

```toml
[tool.isort]
profile = "black"
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
known_first_party = ["myproject"]
```

**Custom section example:**

```toml
[tool.isort]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "DJANGO", "FIRSTPARTY", "LOCALFOLDER"]
known_django = ["django"]
```

### Multi-Line Output Styles

```toml
[tool.isort]
multi_line_output = 3  # Vertical hanging indent (Black compatible)
```

**Common styles:**

- `0` - Grid
- `1` - Vertical
- `2` - Hanging indent
- `3` - Vertical hanging indent (Black default)
- `4` - Hanging grid
- `5` - Hanging grid grouped

**Example of style 3 (Vertical hanging indent):**

```python
from mypackage import (
    function_one,
    function_two,
    function_three,
)
```

### Skip Files

```toml
[tool.isort]
skip = ["migrations", ".venv", "build"]
skip_glob = ["**/migrations/*"]
```

## Common Commands

### Sort Imports

```bash
isort .                    # Sort all Python files
isort file.py              # Sort single file
isort --check .            # Check only (CI)
isort --diff .             # Show what would change
```

### Recursive vs Single Directory

```bash
isort .                    # Recursive (default)
isort --recursive .        # Explicit recursive
isort src/                 # Specific directory
```

### Settings Discovery

```bash
isort --show-settings      # Display current settings
```

## Integration Patterns

### With Black

**CRITICAL:** Always use `profile = "black"` to avoid conflicts.

```toml
[tool.black]
line-length = 88

[tool.isort]
profile = "black"
line_length = 88
```

**Run order:** isort BEFORE Black:

```bash
isort . && black .
```

**Why:** Black may reformat what isort just organized, but won't break isort's section separation.

### With Ruff

Ruff's `I` rules replace isort entirely:

```toml
[tool.ruff.lint]
select = ["I"]  # Enable import sorting

[tool.ruff.lint.isort]
known-first-party = ["myproject"]
```

**Migration:** If using ruff for imports, remove isort from your workflow.

### With Pre-commit

```yaml
repos:
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2  # Use latest version
    hooks:
      - id: isort
        args: ["--profile", "black"]
```

## Skip Directives

### Skip Entire File

```python
# isort: skip_file
```

**Place at top of file.**

### Skip Specific Imports

```python
import module  # isort: skip
```

### Skip Block

```python
# isort: off
import z
import a
# isort: on
```

## Configuration File Locations

isort looks for configuration in this order:

1. `pyproject.toml` (`[tool.isort]`)
2. `setup.cfg` (`[isort]`)
3. `.isort.cfg`
4. `tox.ini` (`[isort]`)

**Recommendation:** Use `pyproject.toml` for consistency with other tools.

## Common Pitfalls

### Pitfall 1: Conflicting with Black

**Problem:** isort and Black disagree on import formatting.

```toml
# ❌ No profile specified
[tool.isort]
line_length = 79

[tool.black]
line-length = 88
```

**Solution:**

```toml
# ✅ Black profile
[tool.isort]
profile = "black"
line_length = 88
```

### Pitfall 2: Wrong Section Classification

**Problem:** Project imports classified as third-party.

```python
# Imports from your project incorrectly grouped with third-party
from thirdparty import foo
from myproject import bar  # Should be in separate section
```

**Solution:**

```toml
[tool.isort]
known_first_party = ["myproject"]
```

### Pitfall 3: Import Ordering in `__init__.py`

**Problem:** isort reorders imports that need specific ordering for re-exports.

**Solution:**

```python
# isort: skip_file
# Specific ordering required for re-exports
from .base import Base
from .child import Child  # Must import after Base
```

### Pitfall 4: Running After Black

**Problem:** Black reformats what isort just organized.

**Solution:** Always run isort BEFORE Black:

```bash
isort . && black .  # Correct order
```

### Pitfall 5: Not Skipping Generated Files

**Problem:** isort reformats generated or vendored code.

**Solution:**

```toml
[tool.isort]
skip = ["migrations", "vendor", ".venv", "build"]
skip_glob = ["**/migrations/*", "**/vendor/**/*.py"]
```

## Typical Complete Configuration

Most projects using Black need minimal isort configuration:

```toml
[tool.isort]
profile = "black"
known_first_party = ["myproject"]
```

That's it for Black-compatible projects.

## Official Documentation

For complete reference:

- <https://pycqa.github.io/isort/> - Main documentation
- <https://pycqa.github.io/isort/docs/configuration/options/> - Configuration reference
- <https://pycqa.github.io/isort/docs/configuration/profiles/> - Profile documentation
