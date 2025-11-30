---
description: Automatically fix markdown linting issues
argument-hint: [path] [--config CONFIG_FILE]
allowed-tools: Bash(markdownlint-cli2:*), Bash(*/lint-helper.py)
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
2. **Project config** - If `.markdownlint-cli2.*` exists in cwd, let markdownlint auto-discover it
3. **User config** - If `~/.markdownlint-cli2.jsonc` exists, use `--config` with it
4. **Skill default** - Use the plugin's default-config.jsonc as fallback

## Implementation

1. Parse arguments: extract target path and check for `--config CONFIG_FILE`
2. If explicit `--config` provided: run `markdownlint-cli2 --fix --config <CONFIG_FILE> <target>`
3. Otherwise, use the lint-helper.py script to resolve config:
   - The script is at: `MR_SPARKLE_ROOT/skills/markdown-quality/scripts/lint-helper.py`
   - MR_SPARKLE_ROOT is provided via SessionStart hook context (check your session context)
   - Run the helper: `<MR_SPARKLE_ROOT>/skills/markdown-quality/scripts/lint-helper.py`
   - If it returns a config path, run `markdownlint-cli2 --fix --config <path> <target>`
   - If it returns empty string, run `markdownlint-cli2 --fix <target>` (auto-discovers or uses defaults)

After fixing, report which files were processed and any issues that couldn't be auto-fixed.

For details on the linting rules and configuration, see the markdown-quality skill.
