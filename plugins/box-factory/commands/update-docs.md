---
description: Update or regenerate README and CLAUDE.md documentation for a plugin
argument-hint: plugin-path
---

Update documentation for the plugin at $1 (or current directory if not specified).

## Process

1. **Read all plugin components:**
   - plugin.json (metadata)
   - All files in agents/, commands/, skills/, hooks/
   - Existing README.md and CLAUDE.md (if present)

2. **Generate/update README.md (minimal by default):**
   - Brief description (1-2 sentences)
   - Components list with one-line descriptions
   - Installation only if external tools required
   - Basic usage example if non-obvious

   **Only add if actually needed:**
   - Troubleshooting: Only for known issues
   - Configuration: Only if plugin has settings

   **Never include:**
   - Future roadmap or planned features
   - Extensibility sections (unless explicitly requested)
   - Verbose error handling documentation
   - Sections that duplicate what Claude already knows

3. **Generate/update CLAUDE.md (only if plugin has conventions):**
   - Only create if plugin has specific patterns Claude should follow
   - Focus on knowledge delta (what Claude wouldn't know)
   - Skip if plugin is simple with no special conventions

4. **Ensure accuracy:**
   - Documentation matches actual implementation
   - No speculative or aspirational content
   - Remove outdated sections from existing docs
