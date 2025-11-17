---
description: Lint markdown files and report issues with line numbers
argument-hint: [path]
allowed-tools: Bash(markdownlint-cli2:*)
model: haiku
---

Run `markdownlint-cli2` to check markdown files for formatting issues.

Usage examples:
- `/lint-md` - Lint all markdown files in current directory
- `/lint-md docs/` - Lint files in the docs directory
- `/lint-md guides/getting-started.md` - Lint a specific file

The command reports:
- Which files have issues
- Line numbers where issues occur
- Rule violations and descriptions

For guidance on rule interpretations and fixes, refer to the markdown-quality skill.

Do NOT automatically fix issues - this command is for inspection only. Use `/mr-sparkle:fix-md` to apply automatic fixes.
