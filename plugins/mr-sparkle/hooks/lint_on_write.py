#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
PostToolUse linting hook for Claude Code.

Thin wrapper that delegates to skills/linting/scripts/lint.py --stdin-hook.
Respects per-project config from ~/.config/neat-little-package/mr-sparkle.toml.
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "_lib"))
from plugin_config import get_plugin_config


def main():
    """Delegate to lint.py --stdin-hook."""
    # Locate lint.py relative to this hook
    hook_dir = Path(__file__).resolve().parent
    lint_script = hook_dir.parent / "skills" / "linting" / "scripts" / "lint.py"

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

    if cwd:
        config = get_plugin_config("mr-sparkle", cwd)
        if not config.get("lint_on_write", True):
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
