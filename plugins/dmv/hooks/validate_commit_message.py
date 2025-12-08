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
import sys
import re
import subprocess
from typing import Optional, List


def output_warning(message: str) -> None:
    """Output non-blocking warning visible directly to user."""
    output = {"systemMessage": message}
    print(json.dumps(output), flush=True)


def get_commit_message_from_command(command: str) -> Optional[str]:
    """Extract commit message from git commit command."""
    # Match: git commit -m "message"
    match = re.search(r'git\s+commit.*-m\s+["\']([^"\']+)["\']', command)
    if match:
        return match.group(1)

    # Match: git commit -m message (no quotes, single word)
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
    """
    Validate commit message against user conventions.

    Returns list of violation messages (empty if clean).
    """
    violations = []

    # Check for emojis (any Unicode emoji characters)
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # emoticons
        "\U0001f300-\U0001f5ff"  # symbols & pictographs
        "\U0001f680-\U0001f6ff"  # transport & map
        "\U0001f1e0-\U0001f1ff"  # flags
        "\U00002702-\U000027b0"  # dingbats
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

    # Check for capitalized start (unless proper noun heuristic)
    # Allow: "GitHub", "API", etc. but flag "Fix:", "Add:", etc.
    if message and message[0].isupper():
        # Simple heuristic: if first word is common type prefix, flag it
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

    # Check message length (soft limit ~200 chars)
    if len(message) > 200:
        violations.append(f"length {len(message)} chars (user prefers max ~200)")

    return violations


def main():
    """Main hook entry point."""
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Invalid input, silently exit
        sys.exit(0)

    # Only process Bash tool calls
    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    # Get the bash command
    tool_input = hook_input.get("tool_input", {})
    command = tool_input.get("command", "")

    # Check if this was a git commit command
    if "git commit" not in command.lower():
        sys.exit(0)

    # Extract commit message from command or get from git log
    commit_message = get_commit_message_from_command(command)

    # If message not in command (e.g., git commit --amend), try git log
    if not commit_message:
        commit_message = get_latest_commit_message()

    # If still no message, nothing to validate
    if not commit_message:
        sys.exit(0)

    # Validate the commit message
    violations = validate_commit_message(commit_message)

    # If violations found, warn user (non-blocking)
    if violations:
        warning = "Commit message issues:\n"
        for violation in violations:
            warning += f"  - {violation}\n"
        warning += f'\nMessage: "{commit_message}"'

        output_warning(warning)

    # Always exit 0 (non-blocking, preference enforcement only)
    sys.exit(0)


if __name__ == "__main__":
    main()
