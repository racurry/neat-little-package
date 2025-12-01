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


def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Only check Bash commands
    if tool_name != "Bash":
        sys.exit(0)

    command = tool_input.get("command", "")

    # Check if this is a markdownlint invocation without explicit config
    if "markdownlint" in command.lower():
        # Allow if --config is specified (proper usage via slash command)
        if "--config" in command:
            sys.exit(0)
        # Block direct invocation without config
        print(
            "markdownlint-cli2 requires a --config argument.  Specify a config or use /mr-sparkle:lint-md [path]",
            file=sys.stderr,
        )
        sys.exit(2)

    # Allow other commands
    sys.exit(0)


if __name__ == "__main__":
    main()
