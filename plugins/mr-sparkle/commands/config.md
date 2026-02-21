---
description: Manage mr-sparkle per-project hook settings
argument-hint: [show | enable <key> | disable <key>]
allowed-tools: Read, Write, Edit
---

Manage mr-sparkle's per-project configuration file at `~/.config/neat-little-package/mr-sparkle.toml`.

## Config Keys

| Key                         | Default | Description                                 |
| --------------------------- | ------- | ------------------------------------------- |
| `lint_on_write`             | `true`  | Auto-lint files after Write/Edit operations |
| `block_direct_markdownlint` | `true`  | Block markdownlint-cli2 without --config    |

## Behavior

**If $ARGUMENTS is empty or "show":**

1. Read `~/.config/neat-little-package/mr-sparkle.toml` (it may not exist yet — that's fine, all defaults apply)
2. Resolve overrides against the current working directory
3. Display: which keys are active for this directory, their resolved values, and any matching overrides

**If $ARGUMENTS starts with "enable" or "disable":**

1. Parse the key name from arguments (e.g., "disable lint_on_write")
2. Read the config file (create it if it doesn't exist)
3. Add or update an `[[overrides]]` block for the current working directory:
   - "disable lint_on_write" → adds override with `lint_on_write = false` matching the current directory
   - "enable lint_on_write" → removes the override for this directory that disables it, or adds `lint_on_write = true` if a parent override disabled it
4. Write the updated TOML back
5. Show the resolved config after the change

## TOML Format

```toml
# Top-level: defaults for all directories
lint_on_write = true

# Directory-specific overrides (last match wins)
[[overrides]]
match = "~/workspace/some-project"
lint_on_write = false
```

The `match` field uses `~` for home directory. It matches the directory and all subdirectories. Trailing `/**` is optional and equivalent.

## Important

- If the config file doesn't exist and the user wants to disable something, create `~/.config/neat-little-package/mr-sparkle.toml` with the appropriate override
- Create the `~/.config/neat-little-package/` directory if it doesn't exist
- Always show the resolved state after any change
