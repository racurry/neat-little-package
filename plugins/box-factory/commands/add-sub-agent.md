---
description: Create a new Claude Code agent
---

Use the sub-agent-writer agent to create a new agent.

**Context Detection:**

1. If `marketplace.json` exists at project root → List plugins to choose from
1. If `.claude-plugin/plugin.json` exists in current directory → Use current plugin's `agents/` directory
1. Otherwise → Use `.claude/agents/` (standalone project)

The sub-agent-writer will:

- Detect context automatically using the rules above
- Gather agent requirements and specifications
- Create properly formatted agent markdown file in the appropriate directory
- Follow sub-agent-design skill patterns for autonomous delegation
