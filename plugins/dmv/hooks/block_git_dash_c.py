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
from pathlib import Path


def _is_enabled(cwd: str) -> bool:
    """Check if block_git_dash_c is enabled via .claude/dmv.local.md."""
    settings_file = Path(cwd) / ".claude" / "dmv.local.md"
    if not settings_file.is_file():
        return True  # enabled by default

    try:
        text = settings_file.read_text()
        # Extract frontmatter
        parts = text.split("---", 2)
        if len(parts) < 3:
            return True
        frontmatter = parts[1]
        for line in frontmatter.strip().splitlines():
            if line.strip().startswith("block_git_dash_c:"):
                value = line.split(":", 1)[1].strip().lower()
                return value not in ("false", "no", "0")
    except Exception:
        pass
    return True


def block(reason: str) -> None:
    """Output PreToolUse denial and exit."""
    print(reason, file=sys.stderr, flush=True)
    sys.exit(2)


def main():
    """Main hook entry point."""
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Check per-project config
    cwd = hook_input.get("cwd", "")
    if cwd and not _is_enabled(cwd):
        sys.exit(0)

    # Only process Bash tool calls
    if hook_input.get("tool_name") != "Bash":
        sys.exit(0)

    command = hook_input.get("tool_input", {}).get("command", "")

    # Check for git -C pattern (case insensitive, various spacing)
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
