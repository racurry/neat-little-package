---
description: Validate a plugin's structure and components against official specs and best practices
argument-hint: [plugin-path]
---

Use the validation-agent to perform comprehensive validation of the plugin at `$1`.

The agent will validate:

- plugin.json structure and required fields
- Directory structure (components at plugin root, not in .claude-plugin/)
- Component frontmatter and formatting
- Forbidden patterns and anti-patterns
- Best practices compliance

If no path is provided, validate the current plugin context.
