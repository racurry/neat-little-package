---
description: Add a new hook to an existing plugin
---

Use the hooks-writer agent to create a new hook for a plugin.

The hooks-writer will:
- List available plugins to choose from
- Gather hook requirements (event type, matcher, command/prompt)
- Create or update hooks.json in the plugin's hooks/ directory
- Update plugin.json if needed
- Follow hook-design skill patterns for deterministic lifecycle integration
