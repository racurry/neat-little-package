---
description: Review a Claude Code component for quality and best practices
argument-hint: [component-path]
---

Use the component-reviewer agent to perform a comprehensive quality review of the specified Claude Code component.

The component-reviewer agent will analyze the component against:
- Relevant design skills (slash-command-design, agent-design, hook-design, plugin-design)
- Official Claude Code documentation
- Common anti-patterns and best practices

Component to review: $1

If no component path is provided, the agent will prompt for clarification or review the current file if it's a recognized component type.
