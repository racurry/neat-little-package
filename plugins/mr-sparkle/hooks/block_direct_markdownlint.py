#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
PreToolUse hook that blocks direct markdownlint-cli2 invocations.

Forces use of /mr-sparkle:lint-md command which handles config resolution
properly (project config -> user config -> plugin default).

Exit codes:
- 0: Allow (not a markdownlint command)
- 2: Block (direct markdownlint invocation detected)
"""

import json
import os
import sys
import tomllib
from pathlib import Path


def _get_config(cwd: str) -> dict:
    """Read mr-sparkle config with directory-specific overrides."""
    config_dir = Path(
        os.environ.get("NLP_CONFIG_DIR", "~/.config/neat-little-package")
    ).expanduser()
    config_file = config_dir / "mr-sparkle.toml"

    if not config_file.is_file():
        return {}

    try:
        with open(config_file, "rb") as f:
            data = tomllib.load(f)
    except Exception:
        return {}

    resolved = {k: v for k, v in data.items() if k != "overrides"}
    for override in data.get("overrides", []):
        pattern = override.get("match", "")
        if not pattern:
            continue
        prefix = str(Path(pattern).expanduser()).rstrip("/")
        for suffix in ("/**", "/*"):
            if prefix.endswith(suffix):
                prefix = prefix[: -len(suffix)]
                break
        if cwd == prefix or cwd.startswith(prefix + "/"):
            for k, v in override.items():
                if k != "match":
                    resolved[k] = v

    return resolved


def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Check per-project config
    cwd = hook_input.get("cwd", "")
    if cwd:
        config = _get_config(cwd)
        if not config.get("block_direct_markdownlint", True):
            sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Only check Bash commands
    if tool_name != "Bash":
        sys.exit(0)

    command = tool_input.get("command", "")

    # Block direct markdownlint-cli2 invocations
    if command.startswith("markdownlint-cli2 "):
        # Allow if --config is specified (proper usage via slash command)
        if "--config" in command:
            sys.exit(0)
        # Block direct invocation without config
        print(
            "markdownlint-cli2 requires a --config argument. Specify a config or use /mr-sparkle:lint-md [path]",
            file=sys.stderr,
        )
        sys.exit(2)

    # Allow other commands
    sys.exit(0)


if __name__ == "__main__":
    main()
