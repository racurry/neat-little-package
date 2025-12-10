---
description: Load focused context for a specific plugin in this multi-plugin repository
argument-hint: plugin-name
---

Quick orientation to the `$1` plugin in `plugins/$1` - just enough context to start working.

**Efficiency goal:** Minimal token usage. Read only essential docs, list (don't read) components.

**Steps:**

1. **Read essential documentation** (always small, high-value):

   - `plugins/$1/.claude-plugin/plugin.json` - Plugin metadata
   - `plugins/$1/README.md` - Plugin overview
   - `plugins/$1/CLAUDE.md` - Plugin-specific conventions (if exists)

1. **List component files** using a single bash command:

   - Use `find` or `ls` to enumerate files in agents/, commands/, skills/, hooks/
   - DO NOT read individual component files - just list what exists
   - Component details can be read on-demand when actually needed

1. **Provide concise summary** (3-5 bullets):

   - Plugin's core purpose (from README)
   - Available components (counts: X agents, Y commands, Z skills, N hooks)
   - Notable conventions from CLAUDE.md (if present)
   - Any cross-plugin references mentioned in README

**Important:**

- This is orientation, not deep analysis - keep it light
- Don't read component contents unless README references something specific
- Don't offer to make changes - this is context loading only

**If no argument provided:** List available plugins and prompt for selection.
