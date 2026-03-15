---
name: config
description: Manage mr-sparkle per-project hook settings
argument-hint: show | enable <key> | disable <key>
---

Read and manage mr-sparkle's per-project settings at `.claude/mr-sparkle.local.md` in the current project root.

**Available config keys:**

| Key                         | Default | Description                                 |
| --------------------------- | ------- | ------------------------------------------- |
| `lint_on_write`             | `true`  | Auto-lint files after Write/Edit operations |
| `block_direct_markdownlint` | `true`  | Block markdownlint-cli2 without --config    |

**If no arguments or "show":** Read `.claude/mr-sparkle.local.md` (it may not exist — all defaults apply) and display the resolved values from YAML frontmatter.

**If "enable" or "disable":** Parse the key name, read or create `.claude/mr-sparkle.local.md`, update the YAML frontmatter, and show the resolved config after.

**File format:**

```markdown
---
lint_on_write: true
block_direct_markdownlint: false
---

Optional notes about why settings were changed.
```

- Create `.claude/` directory if it doesn't exist
- Add `.claude/*.local.md` to `.gitignore` if not already there
- Always show resolved state after any change

Now execute this based on what the user requested.
