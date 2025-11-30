---
description: Automatically fix markdown linting issues
argument-hint: [path] [--config CONFIG_FILE]
allowed-tools: Bash(markdownlint-cli2:*), Bash($HOME/.claude/plugins/mr-sparkle@neat-little-package/skills/markdown-quality/scripts/lint-helper.py)
---

Run `markdownlint-cli2 --fix` to automatically correct markdown formatting issues.

## Usage examples

- `/fix-md` - Fix all markdown files in current directory
- `/fix-md docs/` - Fix markdown files in the docs folder
- `/fix-md README.md` - Fix a specific markdown file
- `/fix-md README.md --config .my-custom-config.jsonc` - Fix with custom config

## Configuration File Hierarchy

The command uses the following config file resolution order:

1. **Explicit config** - If `--config CONFIG_FILE` is passed, use that file
2. **Project config** - Look for `.markdownlint-cli2.*` files in current directory (`.jsonc`, `.yaml`, `.cjs`, `.mjs`)
3. **User config** - Check `~/.markdownlint-cli2.jsonc` for user-level defaults
4. **Skill default** - Use `~/.claude/plugins/mr-sparkle@neat-little-package/skills/markdown-quality/default-config.jsonc` as fallback

## Implementation

1. Parse the arguments to check if `--config` flag was passed with a config file path
2. If no explicit config provided, call `$HOME/.claude/plugins/mr-sparkle@neat-little-package/skills/markdown-quality/scripts/lint-helper.py` to resolve the config file
3. If the helper returns a config path, run `markdownlint-cli2 --fix --config <path> <target>`
4. If the helper returns empty string, run `markdownlint-cli2 --fix <target>` (uses project config or defaults)

After fixing, the tool will report which files were processed and any issues that couldn't be auto-fixed.

For details on the linting rules and configuration, see the markdown-quality skill.
