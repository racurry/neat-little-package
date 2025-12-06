---
description: Add a new Claude Code hook
---

Use the hooks-writer agent to create a new hook.

**Context Detection:**

1. If `marketplace.json` exists at project root → List plugins to choose from
2. If `.claude-plugin/plugin.json` exists in current directory → Use current plugin's `hooks/` directory
3. Otherwise → Use `.claude/settings.json` hooks section (standalone project)

The hooks-writer will:

- Detect context automatically using the rules above
- Gather hook requirements (event type, matcher, command/prompt)
- Create or update hooks configuration in the appropriate location
- Follow hook-design skill patterns for deterministic lifecycle integration
