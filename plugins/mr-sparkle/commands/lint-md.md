---
description: Lint markdown files and report issues with line numbers
argument-hint: [path] [--config CONFIG_FILE]
allowed-tools: Bash(markdownlint-cli2:*), Bash($HOME/.claude/plugins/mr-sparkle@neat-little-package/skills/markdown-quality/scripts/lint-helper.py)
---

Run `markdownlint-cli2` to check markdown files for formatting issues.

## Usage examples

- `/lint-md` - Lint all markdown files in current directory
- `/lint-md docs/` - Lint files in the docs directory
- `/lint-md guides/getting-started.md` - Lint a specific file
- `/lint-md README.md --config .my-custom-config.jsonc` - Lint with custom config

## Configuration File Hierarchy

The command uses the following config file resolution order:

1. **Explicit config** - If `--config CONFIG_FILE` is passed, use that file
2. **Project config** - Look for `.markdownlint-cli2.*` files in current directory (`.jsonc`, `.yaml`, `.cjs`, `.mjs`)
3. **User config** - Check `~/.markdownlint-cli2.jsonc` for user-level defaults
4. **Skill default** - Use `~/.claude/plugins/mr-sparkle@neat-little-package/skills/markdown-quality/default-config.jsonc` as fallback

## Implementation

1. Parse the arguments to check if `--config` flag was passed with a config file path
2. If no explicit config provided, call `$HOME/.claude/plugins/mr-sparkle@neat-little-package/skills/markdown-quality/scripts/lint-helper.py` to resolve the config file
3. If the helper returns a config path, run `markdownlint-cli2 --config <path> <target>`
4. If the helper returns empty string, run `markdownlint-cli2 <target>` (uses project config or defaults)

The command reports:

- Which files have issues
- Line numbers where issues occur
- Rule violations and descriptions

For guidance on rule interpretations and fixes, refer to the markdown-quality skill.

Do NOT automatically fix issues - this command is for inspection only. Use `/mr-sparkle:fix-md` to apply automatic fixes.
