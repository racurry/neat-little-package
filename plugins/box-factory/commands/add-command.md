---
description: Create a new Claude Code slash command
---

Use the slash-command-writer agent to create a new slash command.

**Context Detection:**

1. If `marketplace.json` exists at project root → List plugins to choose from
2. If `.claude-plugin/plugin.json` exists in current directory → Use current plugin's `commands/` directory
3. Otherwise → Use `.claude/commands/` (standalone project)

The agent will:

- Detect context automatically using the rules above
- Gather command requirements (name, purpose, arguments, tool restrictions)
- Create the command markdown file in the appropriate directory
- Validate the command follows best practices

Provide the command name and purpose when ready.
