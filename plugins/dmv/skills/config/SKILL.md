---
name: config
description: Manage dmv per-project hook settings
argument-hint: show | enable <key> | disable <key>
---

Read and manage dmv's per-project settings at `.claude/dmv.local.md` in the current project root.

**Available config keys:**

| Key                       | Default | Description                    |
| ------------------------- | ------- | ------------------------------ |
| `validate_commit_message` | `true`  | Validate commit message format |

**If no arguments or "show":** Read `.claude/dmv.local.md` (it may not exist — all defaults apply) and display the resolved values from YAML frontmatter.

**If "enable" or "disable":** Parse the key name, read or create `.claude/dmv.local.md`, update the YAML frontmatter, and show the resolved config after.

**File format:**

```markdown
---
validate_commit_message: false
---

Optional notes about why settings were changed.
```

- Create `.claude/` directory if it doesn't exist
- Add `.claude/*.local.md` to `.gitignore` if not already there
- Always show resolved state after any change

Now execute this based on what the user requested.
