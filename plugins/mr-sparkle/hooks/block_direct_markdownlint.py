#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
PreToolUse hook that blocks direct markdownlint-cli2 invocations.

Forces use of /mr-sparkle:lint-md command which handles config resolution
properly (project config → user config → plugin default).

Exit codes:
- 0: Allow (not a markdownlint command)
- 2: Block (direct markdownlint invocation detected)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "_lib"))
from plugin_config import get_plugin_config


def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Check per-project config
    cwd = hook_input.get("cwd", "")
    if cwd:
        config = get_plugin_config("mr-sparkle", cwd)
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
