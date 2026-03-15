---
name: uv-scripts
description: Gotchas and conventions for writing Python scripts with UV inline metadata (PEP 723). Use when creating or editing Python scripts that use uv run.
---

# UV Scripts

Corrections and conventions for writing Python scripts with UV inline metadata (PEP 723). Claude knows UV basics but consistently gets these details wrong.

## Shebang Requires -S Flag

```python
#!/usr/bin/env -S uv run --script
```

**Not** `#!/usr/bin/env uv run --script` — without `-S`, env treats `uv run --script` as a single argument and fails.

For scripts that should suppress UV's own output, use `--quiet`:

```python
#!/usr/bin/env -S uv run --quiet --script
```

## Empty Dependencies Must Be Explicit

The `dependencies` field is required even when empty:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

Omitting `dependencies` causes UV to fail, even if you only need `requires-python`.

## Complete Template

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```
