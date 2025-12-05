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

2. **Load readme-style skill:**

   ```
   Use Skill tool: skill="box-factory:readme-style"
   ```

3. **Generate/update README.md following readme-style skill:**
   - Target ~20 lines total (not 50-100)
   - One-liner description
   - 2-3 terse bullets in Overview
   - Commands in code blocks with inline `#` comments
   - NO Components/Features/Philosophy/Troubleshooting sections
   - NO prose explanations - action-focused only

4. **Generate/update CLAUDE.md (only if plugin has conventions):**
   - Only create if plugin has specific patterns Claude should follow
   - Focus on knowledge delta (what Claude wouldn't know)
   - Skip if plugin is simple with no special conventions

5. **Ensure accuracy:**
   - Documentation matches actual implementation
   - No speculative or aspirational content
   - Remove outdated sections from existing docs
