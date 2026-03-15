#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
PreToolUse hook that blocks direct markdownlint-cli2 invocations.

Forces use of /mr-sparkle:lint which handles config resolution
properly (project config -> user config -> plugin default).

Exit codes:
- 0: Allow (not a markdownlint command)
- 2: Block (direct markdownlint invocation detected)
"""

import json
import sys
from pathlib import Path


def _is_enabled(cwd: str) -> bool:
    """Check if block_direct_markdownlint is enabled via .claude/mr-sparkle.local.md."""
    settings_file = Path(cwd) / ".claude" / "mr-sparkle.local.md"
    if not settings_file.is_file():
        return True  # enabled by default

    try:
        text = settings_file.read_text()
        parts = text.split("---", 2)
        if len(parts) < 3:
            return True
        frontmatter = parts[1]
        for line in frontmatter.strip().splitlines():
            if line.strip().startswith("block_direct_markdownlint:"):
                value = line.split(":", 1)[1].strip().lower()
                return value not in ("false", "no", "0")
    except Exception:
        pass
    return True


def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Check per-project config
    cwd = hook_input.get("cwd", "")
    if cwd and not _is_enabled(cwd):
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
