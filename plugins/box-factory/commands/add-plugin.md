---
description: Create a new Claude Code plugin with complete scaffolding
---

Delegate to the plugin-writer agent to create a new Claude Code plugin.

The plugin-writer will:

- Create proper directory structure with components at root (not in .claude-plugin/)
- Generate plugin.json with comprehensive metadata
- Write detailed README with installation and usage instructions
- **MUST delegate** component creation to specialized writer agents (never create components directly)
- Self-validate for Box Factory compliance before completing
- Follow plugin-design skill patterns for production-ready plugins
- Optionally register plugin in marketplace.json
