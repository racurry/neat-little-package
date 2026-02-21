#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
PreToolUse hook to block git -C commands.

Claude repeatedly uses `git -C <path>` despite prompting telling it not to.
This hook deterministically blocks execution and guides Claude to use
standard git commands from the working directory instead.
"""

import json
import os
import re
import sys
import tomllib
from pathlib import Path


def _get_config(cwd: str) -> dict:
    """Read dmv config with directory-specific overrides."""
    config_dir = Path(
        os.environ.get("NLP_CONFIG_DIR", "~/.config/neat-little-package")
    ).expanduser()
    config_file = config_dir / "dmv.toml"

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


def block(reason: str) -> None:
    """Output blocking decision and exit."""
    output = {"decision": "block", "reason": reason}
    print(json.dumps(output), flush=True)
    sys.exit(0)


def main():
    """Main hook entry point."""
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Check per-project config
    cwd = hook_input.get("cwd", "")
    if cwd:
        config = _get_config(cwd)
        if not config.get("block_git_dash_c", True):
            sys.exit(0)

    # Only process Bash tool calls
    if hook_input.get("tool_name") != "Bash":
        sys.exit(0)

    command = hook_input.get("tool_input", {}).get("command", "")

    # Check for git -C pattern (case insensitive, various spacing)
    # Matches: git -C, git  -C, git -C/path, etc.
    if re.search(r"\bgit\s+-C\b", command, re.IGNORECASE):
        block(
            "BLOCKED: git -C is not allowed. "
            "Run git commands from the working directory instead. "
            "Use relative paths or absolute paths without -C flag."
        )

    # Allow command to proceed
    sys.exit(0)


if __name__ == "__main__":
    main()
