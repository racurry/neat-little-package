---
description: Automatically fix markdown linting issues
argument-hint: [path]
allowed-tools: Bash(markdownlint-cli2:*)
model: haiku
---

Fix markdown files at path `$1` (defaults to current directory if not provided).

Run `markdownlint-cli2 --fix` to automatically correct markdown formatting issues according to the markdown-quality skill rules.

## Usage examples

- `/fix-md` - Fix all markdown files in current directory
- `/fix-md docs/` - Fix markdown files in the docs folder
- `/fix-md README.md` - Fix a specific markdown file

After fixing, the tool will report which files were processed and any issues that couldn't be auto-fixed.

For details on the linting rules and configuration, see the markdown-quality skill.
