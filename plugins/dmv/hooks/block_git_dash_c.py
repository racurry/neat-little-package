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
import re
import sys


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
