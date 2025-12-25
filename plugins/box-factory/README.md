# Box Factory

![My boy is a box!](./assets/box-factory.png)

Toolkit for creating Claude Code components. Specialized agents, slash commands, and design skills for building plugins, agents, commands, skills, and hooks.

## Overview

Box Factory creates Claude Code components for **both plugins and standalone projects**. It automatically detects your context:

- **Marketplace context** (`marketplace.json` exists): Lists plugins to choose from
- **Plugin context** (`.claude-plugin/plugin.json` exists): Uses current plugin's directories
- **Standalone project**: Uses `.claude/` directories

Every component in Box Factory follows the patterns it teaches.

## Commands

| Command                                | Description                                   |
| -------------------------------------- | --------------------------------------------- |
| `/box-factory:add-plugin`              | Create a new plugin with complete scaffolding |
| `/box-factory:add-sub-agent`           | Create a new agent                            |
| `/box-factory:add-command`             | Create a new slash command                    |
| `/box-factory:add-skill`               | Create a new skill                            |
| `/box-factory:add-hook`                | Create a new hook                             |
| `/box-factory:add-rule`                | Create a modular rule file                    |
| `/box-factory:validate-plugin [path]`  | Validate plugin structure and components      |
| `/box-factory:review-component <path>` | Review a component for quality                |
| `/box-factory:update-docs [path]`      | Regenerate README and CLAUDE.md               |

## Agents

### Writers

| Agent                              | Purpose                                                  |
| ---------------------------------- | -------------------------------------------------------- |
| `box-factory:plugin-writer`        | Creates complete plugins, delegates to component writers |
| `box-factory:sub-agent-writer`     | Creates agents following sub-agent-design patterns       |
| `box-factory:slash-command-writer` | Creates commands following thin wrapper pattern          |
| `box-factory:skill-writer`         | Creates skills with fetch-first, two-layer structure     |
| `box-factory:hooks-writer`         | Creates hooks with security and performance validation   |
| `box-factory:rules-writer`         | Creates modular rule files with proper frontmatter       |

### Quality

| Agent                            | Purpose                                      |
| -------------------------------- | -------------------------------------------- |
| `box-factory:validation-agent`   | Validates plugins and components (read-only) |
| `box-factory:component-reviewer` | Reviews components for quality (read-only)   |

## Skills

| Skill                                  | When to Use                                                |
| -------------------------------------- | ---------------------------------------------------------- |
| `box-factory:sub-agent-design`         | Creating or reviewing agents                               |
| `box-factory:slash-command-design`     | Creating or reviewing commands                             |
| `box-factory:plugin-design`            | Creating or reviewing plugins                              |
| `box-factory:hook-design`              | Creating or reviewing hooks                                |
| `box-factory:skill-design`             | Creating or reviewing skills                               |
| `box-factory:box-factory-architecture` | Choosing between component types, understanding delegation |
| `box-factory:memory-design`            | Organizing CLAUDE.md and .claude/rules/                    |
| `box-factory:mcp-config`               | Configuring MCP servers                                    |
| `box-factory:uv-scripts`               | Creating Python scripts with inline dependencies           |
| `box-factory:output-styles`            | Understanding agent output customization                   |
| `box-factory:status-line`              | Configuring status line display                            |

## Installation

```bash
# Add marketplace (if needed)
/plugin marketplace add /path/to/neat-little-package

# Install
/plugin install box-factory@neat-little-package
```

## Quick Start

```bash
# Create a new plugin
/box-factory:add-plugin

# Add components to existing plugin
/box-factory:add-command
/box-factory:add-skill
/box-factory:add-sub-agent

# Validate before publishing
/box-factory:validate-plugin
```

## Design Philosophy

Box Factory components follow these principles:

- **Low-maintenance**: Defer to official docs via WebFetch; avoid hardcoding version-specific details
- **Knowledge delta**: Only document what Claude doesn't already know
- **Two-layer approach**: Distinguish official specs from opinionated best practices
- **Delegation pattern**: Commands → Agents → Skills

Load `box-factory:box-factory-architecture` for component selection guidance.

## Examples

Every component in this plugin demonstrates the patterns it teaches:

- `agents/sub-agent-writer.md` - Agent following sub-agent-design
- `commands/add-sub-agent.md` - Command using thin wrapper delegation
- `skills/skill-design/SKILL.md` - Skill with fetch-first structure
