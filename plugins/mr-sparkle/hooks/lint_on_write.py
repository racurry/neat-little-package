#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
PostToolUse linting hook for Claude Code.

Thin wrapper that delegates to skills/linting/scripts/lint.py --stdin-hook.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Delegate to lint.py --stdin-hook."""
    # Locate lint.py relative to this hook
    hook_dir = Path(__file__).resolve().parent
    lint_script = hook_dir.parent / "skills" / "linting" / "scripts" / "lint.py"

    if not lint_script.is_file():
        sys.exit(0)

    # Read stdin and pass through to lint.py
    stdin_data = sys.stdin.read()

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
