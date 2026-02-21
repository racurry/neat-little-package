---
description: Manage dmv per-project hook settings
argument-hint: [show | enable <key> | disable <key>]
allowed-tools: Read, Write, Edit
---

Manage dmv's per-project configuration file at `~/.config/neat-little-package/dmv.toml`.

## Config Keys

| Key                       | Default | Description                    |
| ------------------------- | ------- | ------------------------------ |
| `block_git_dash_c`        | `true`  | Block `git -C` commands        |
| `validate_commit_message` | `true`  | Validate commit message format |

## Behavior

**If $ARGUMENTS is empty or "show":**

1. Read `~/.config/neat-little-package/dmv.toml` (it may not exist yet — that's fine, all defaults apply)
2. Resolve overrides against the current working directory
3. Display: which keys are active for this directory, their resolved values, and any matching overrides

**If $ARGUMENTS starts with "enable" or "disable":**

1. Parse the key name from arguments (e.g., "disable validate_commit_message")
2. Read the config file (create it if it doesn't exist)
3. Add or update an `[[overrides]]` block for the current working directory:
   - "disable block_git_dash_c" → adds override with `block_git_dash_c = false` matching the current directory
   - "enable block_git_dash_c" → removes the override for this directory that disables it, or adds `block_git_dash_c = true` if a parent override disabled it
4. Write the updated TOML back
5. Show the resolved config after the change

## TOML Format

```toml
# Top-level: defaults for all directories
block_git_dash_c = true

# Directory-specific overrides (last match wins)
[[overrides]]
match = "~/workspace/some-project"
validate_commit_message = false
```

The `match` field uses `~` for home directory. It matches the directory and all subdirectories. Trailing `/**` is optional and equivalent.

## Important

- If the config file doesn't exist and the user wants to disable something, create `~/.config/neat-little-package/dmv.toml` with the appropriate override
- Create the `~/.config/neat-little-package/` directory if it doesn't exist
- Always show the resolved state after any change
