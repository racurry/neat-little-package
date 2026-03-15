#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
PostToolUse hook to validate git commit messages against user preferences.

Triggers on Bash tool usage, checks if the command was a git commit,
and validates the message format. Warns (non-blocking) if violations found.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def _is_enabled(cwd: str) -> bool:
    """Check if validate_commit_message is enabled via .claude/dmv.local.md."""
    settings_file = Path(cwd) / ".claude" / "dmv.local.md"
    if not settings_file.is_file():
        return True  # enabled by default

    try:
        text = settings_file.read_text()
        parts = text.split("---", 2)
        if len(parts) < 3:
            return True
        frontmatter = parts[1]
        for line in frontmatter.strip().splitlines():
            if line.strip().startswith("validate_commit_message:"):
                value = line.split(":", 1)[1].strip().lower()
                return value not in ("false", "no", "0")
    except Exception:
        pass
    return True


def output_warning(message: str) -> None:
    """Output non-blocking warning visible directly to user."""
    output = {"systemMessage": message}
    print(json.dumps(output), flush=True)


def get_commit_message_from_command(command: str) -> Optional[str]:
    """Extract commit message from git commit command."""
    match = re.search(r'git\s+commit.*-m\s+["\']([^"\']+)["\']', command)
    if match:
        return match.group(1)

    match = re.search(r"git\s+commit.*-m\s+(\S+)", command)
    if match:
        return match.group(1)

    return None


def get_latest_commit_message() -> Optional[str]:
    """Get the most recent commit message from git log."""
    try:
        result = subprocess.run(["git", "log", "-1", "--format=%s"], capture_output=True, text=True, timeout=2)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def validate_commit_message(message: str) -> List[str]:
    """Validate commit message against user conventions."""
    violations = []

    # Check for emojis
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"
        "\U0001f300-\U0001f5ff"
        "\U0001f680-\U0001f6ff"
        "\U0001f1e0-\U0001f1ff"
        "\U00002702-\U000027b0"
        "\U000024c2-\U0001f251"
        "]+",
        flags=re.UNICODE,
    )
    if emoji_pattern.search(message):
        violations.append("contains emojis (user prefers none)")

    # Check for attribution text
    attribution_patterns = [
        r"Generated with.*Claude",
        r"Co-Authored-By:",
        r"🤖.*Claude Code",
    ]
    for pattern in attribution_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            violations.append("contains attribution text (user prefers none)")
            break

    # Check for period at end
    if message.rstrip().endswith("."):
        violations.append("ends with period (user prefers no period)")

    # Check for capitalized type prefix
    if message and message[0].isupper():
        first_word = message.split()[0] if message.split() else ""
        common_types = ["Add", "Fix", "Update", "Remove", "Refactor", "Improve", "Prevent"]
        if first_word.rstrip(":") in common_types:
            violations.append(f"starts with capitalized type '{first_word}' (user prefers lowercase)")

    # Check for vague messages
    vague_patterns = [
        r"^(fix|update|change|modify)s?$",
        r"^bug\s*fix$",
        r"^(minor|small)\s+(change|fix|update)s?$",
    ]
    for pattern in vague_patterns:
        if re.match(pattern, message.strip(), re.IGNORECASE):
            violations.append("too vague (user prefers specific descriptions)")
            break

    # Check message length
    if len(message) > 200:
        violations.append(f"length {len(message)} chars (user prefers max ~200)")

    return violations


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

    if "git commit" not in command.lower():
        sys.exit(0)

    commit_message = get_commit_message_from_command(command)

    if not commit_message:
        commit_message = get_latest_commit_message()

    if not commit_message:
        sys.exit(0)

    violations = validate_commit_message(commit_message)

    if violations:
        issues = ", ".join(violations)
        warning = f"\033[33m⚠ commit message:\033[0m {issues}"
        output_warning(warning)

    sys.exit(0)


if __name__ == "__main__":
    main()
