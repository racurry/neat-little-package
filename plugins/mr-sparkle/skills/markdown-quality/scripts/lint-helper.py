#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Markdown linting config resolver for mr-sparkle plugin.

Resolves markdownlint-cli2 config file using hierarchy:
1. Project config - .markdownlint-cli2.* in cwd
2. User config - ~/.markdownlint-cli2.jsonc
3. Skill default - plugin's default-config.jsonc

Outputs:
- Empty string if project config exists (let markdownlint auto-discover)
- Config file path if user or skill config should be used
- Empty string if no config found (use markdownlint defaults)

Usage:
  CONFIG=$(./lint-helper.py)
  if [ -n "$CONFIG" ]; then
    markdownlint-cli2 --config "$CONFIG" file.md
  else
    markdownlint-cli2 file.md
  fi
"""

import sys
from pathlib import Path


def resolve_config() -> str:
    """
    Resolve markdownlint config file using hierarchy.

    Returns:
        Config file path, or empty string for auto-discovery/defaults
    """
    # 1. Check for project config in current directory
    project_configs = [
        ".markdownlint-cli2.jsonc",
        ".markdownlint-cli2.yaml",
        ".markdownlint-cli2.cjs",
        ".markdownlint-cli2.mjs"
    ]

    for config in project_configs:
        if Path(config).is_file():
            # Found project config - return empty to let markdownlint auto-discover
            return ""

    # 2. Check for user config
    user_config = Path.home() / ".markdownlint-cli2.jsonc"
    if user_config.is_file():
        return str(user_config)

    # 3. Fall back to skill default config
    # Self-locate: this script is at <plugin_root>/skills/markdown-quality/scripts/lint-helper.py
    plugin_dir = Path(__file__).resolve().parent.parent.parent.parent
    skill_config = plugin_dir / "skills" / "markdown-quality" / "default-config.jsonc"
    if skill_config.is_file():
        return str(skill_config)

    # No config found - return empty for markdownlint defaults
    return ""


def main():
    """Main entry point."""
    config_path = resolve_config()
    print(config_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
