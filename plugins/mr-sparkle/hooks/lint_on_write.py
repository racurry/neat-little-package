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
import os
import subprocess
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
        config = _get_config(cwd)
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
