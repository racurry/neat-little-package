---
name: component-paths
description: Path resolution for Claude Code components. Provides context detection and file paths for skills, agents, commands, hooks, and rules. Load when creating any Box Factory component.
---

# Component Paths

Shared path resolution logic for all Box Factory writer agents.

## Context Detection

Detect context in this order:

1. **Caller specifies path** → Use exact path
2. **User-level** → Only when explicitly requested (`~/.claude/`)
3. **Marketplace** → `marketplace.json` at project root
4. **Plugin** → `.claude-plugin/plugin.json` in current directory
5. **Standalone** → Default case. Use `.claude/` in cwd.

In marketplace context without specified plugin, infer from caller's prompt or component domain.

## Component Paths by Context

| Component | Marketplace                           | Plugin                    | Standalone                       | User                               |
| --------- | ------------------------------------- | ------------------------- | -------------------------------- | ---------------------------------- |
| Skill     | `plugins/[p]/skills/[name]/SKILL.md`  | `skills/[name]/SKILL.md`  | `.claude/skills/[name]/SKILL.md` | `~/.claude/skills/[name]/SKILL.md` |
| Sub-agent | `plugins/[p]/agents/[name].md`        | `agents/[name].md`        | `.claude/agents/[name].md`       | `~/.claude/agents/[name].md`       |
| Command   | `plugins/[p]/commands/[name].md`      | `commands/[name].md`      | `.claude/commands/[name].md`     | `~/.claude/commands/[name].md`     |
| Hook      | `plugins/[p]/hooks/hooks.json`        | `hooks/hooks.json`        | `.claude/settings.json`          | `~/.claude/settings.json`          |
| Rule      | `plugins/[p]/.claude/rules/[name].md` | `.claude/rules/[name].md` | `.claude/rules/[name].md`        | N/A                                |

## Naming Conventions

- **Kebab-case**: All component names (lowercase, hyphens for spaces)
- **Skills**: Subdirectory with `SKILL.md` (uppercase)
- **Sub-agents/Commands**: Flat `.md` files
- **Hooks**: Config in `hooks.json`, scripts as `.py` or `.sh`
- **Rules**: `.md` files with YAML frontmatter

Transform names: "Sub-agent Design" → `sub-agent-design`, "API_docs" → `api-docs`
