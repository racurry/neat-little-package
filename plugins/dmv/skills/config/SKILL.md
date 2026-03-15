---
name: config
description: Manage dmv per-project hook settings
argument-hint: show | enable <key> | disable <key>
---

Read and manage the dmv per-project configuration file at `~/.config/neat-little-package/dmv.toml`.

**Available config keys:**

| Key                       | Default | Description                    |
| ------------------------- | ------- | ------------------------------ |
| `block_git_dash_c`        | `true`  | Block `git -C` commands        |
| `validate_commit_message` | `true`  | Validate commit message format |

**If no arguments or "show":** Read the config file (it may not exist — all defaults apply), resolve overrides against the current working directory, and display the resolved values.

**If "enable" or "disable":** Parse the key name, read or create the config file, add/update an `[[overrides]]` block for the current working directory, write the TOML back, and show the resolved config after.

**TOML format:**

```toml
block_git_dash_c = true

[[overrides]]
match = "~/workspace/some-project"
validate_commit_message = false
```

The `match` field uses `~` for home directory, matches the directory and all subdirectories.

Create `~/.config/neat-little-package/` directory if it doesn't exist. Always show resolved state after any change.

Now execute this based on what the user requested.
