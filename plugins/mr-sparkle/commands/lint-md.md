---
description: Lint markdown files and report issues with line numbers
argument-hint: [path] [--config CONFIG_FILE]
allowed-tools: Bash(markdownlint-cli2:*), Bash(*/lint-helper.py)
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
2. **Project config** - If `.markdownlint-cli2.*` exists in cwd, let markdownlint auto-discover it
3. **User config** - If `~/.markdownlint-cli2.jsonc` exists, use `--config` with it
4. **Skill default** - Use the plugin's default-config.jsonc as fallback

## Implementation

1. Parse arguments: extract target path and check for `--config CONFIG_FILE`
2. If explicit `--config` provided: run `markdownlint-cli2 --config <CONFIG_FILE> <target>`
3. Otherwise, use the lint-helper.py script to resolve config:
   - The script is at: `MR_SPARKLE_ROOT/skills/markdown-quality/scripts/lint-helper.py`
   - MR_SPARKLE_ROOT is provided via SessionStart hook context (check your session context)
   - Run the helper: `<MR_SPARKLE_ROOT>/skills/markdown-quality/scripts/lint-helper.py`
   - If it returns a config path, run `markdownlint-cli2 --config <path> <target>`
   - If it returns empty string, run `markdownlint-cli2 <target>` (auto-discovers or uses defaults)

The command reports which files have issues, line numbers, and rule violations.

For guidance on rule interpretations and fixes, refer to the markdown-quality skill.

Do NOT automatically fix issues - this command is for inspection only. Use `/mr-sparkle:fix-md` to apply automatic fixes.
