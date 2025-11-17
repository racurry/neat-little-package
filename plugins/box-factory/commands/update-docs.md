---
description: Update or regenerate README and CLAUDE.md documentation for a plugin
argument-hint: plugin-path
---

Update or regenerate comprehensive documentation for the plugin at $1 (or current directory if not specified).

## Process

1. **Read all plugin components:**
   - plugin.json (metadata)
   - All files in agents/, commands/, skills/, hooks/
   - Existing README.md and CLAUDE.md (if present)

2. **Analyze the plugin:**
   - Core purpose and value proposition
   - Features and capabilities
   - Component architecture and relationships
   - Usage patterns and workflows
   - Development conventions and patterns

3. **Generate/update README.md:**
   - Plugin overview and description
   - Features section (organize by component type)
   - Installation instructions
   - Quick start guide
   - Usage examples for each component
   - File structure reference
   - Troubleshooting section
   - Resources and links
   - Follow existing Box Factory README patterns as reference

4. **Generate/update CLAUDE.md:**
   - Development philosophy and principles
   - Component-specific patterns and conventions
   - Decision frameworks (when to use what)
   - Quality standards and checklists
   - Anti-patterns (forbidden approaches)
   - Architecture diagrams or patterns
   - Follow existing Box Factory CLAUDE.md patterns as reference

5. **Ensure quality:**
   - Documentation matches actual implementation
   - All components are documented
   - Examples are accurate and tested
   - Consistent tone and formatting
   - No outdated or incorrect information
