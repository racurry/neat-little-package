---
description: Create a new Claude Code skill
---

Use the skill-writer agent to create a new skill.

**Context Detection:**

1. If `marketplace.json` exists at project root → List plugins to choose from
2. If `.claude-plugin/plugin.json` exists in current directory → Use current plugin's `skills/` directory
3. Otherwise → Use `.claude/skills/` (standalone project)

The skill-writer will:

- Detect context automatically using the rules above
- Gather skill requirements and specifications
- Create properly formatted SKILL.md file in the appropriate directory
- Follow skill-design patterns for progressive knowledge disclosure
