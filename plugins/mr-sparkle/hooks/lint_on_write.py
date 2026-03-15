#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
PostToolUse linting hook for Claude Code.

Thin wrapper that delegates to skills/lint/scripts/lint.py --stdin-hook.
Respects per-project config from .claude/mr-sparkle.local.md.
"""

import json
import subprocess
import sys
from pathlib import Path


def _is_enabled(cwd: str) -> bool:
    """Check if lint_on_write is enabled via .claude/mr-sparkle.local.md."""
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
            if line.strip().startswith("lint_on_write:"):
                value = line.split(":", 1)[1].strip().lower()
                return value not in ("false", "no", "0")
    except Exception:
        pass
    return True


def main():
    """Delegate to lint.py --stdin-hook."""
    # Locate lint.py relative to this hook
    hook_dir = Path(__file__).resolve().parent
    lint_script = hook_dir.parent / "skills" / "lint" / "scripts" / "lint.py"

    if not lint_script.is_file():
        sys.exit(0)

    # Read stdin (needed for both config check and delegation)
    stdin_data = sys.stdin.read()

    # Check per-project config
    try:
        hook_input = json.loads(stdin_data)
        cwd = hook_input.get("cwd", "")
    except (json.JSONDecodeError, AttributeError):
        cwd = ""

    if cwd and not _is_enabled(cwd):
        sys.exit(0)

    result = subprocess.run(
        [sys.executable, str(lint_script), "--stdin-hook"],
        input=stdin_data,
        capture_output=True,
        text=True,
    )

    # Print any output from lint.py
    if result.stdout:
        print(result.stdout, end="", flush=True)

    # Hooks should not block - always exit 0
    sys.exit(0)


if __name__ == "__main__":
    main()
