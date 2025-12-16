#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Auto-bump plugin versions with Claude analysis.

Detects plugins with staged changes, asks Claude to determine appropriate
semver bump level (major/minor/patch), and stages the version updates.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


def get_staged_plugins() -> dict[str, bool]:
    """
    Find plugins with staged changes.

    Returns {plugin_name: plugin_json_was_staged}
    If plugin.json was staged, user is managing version manually.
    """
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
    )
    files = result.stdout.strip().split("\n") if result.stdout.strip() else []

    plugins = {}
    for f in files:
        if match := re.match(r"plugins/([^/]+)/", f):
            name = match.group(1)
            plugins.setdefault(name, False)
            if ".claude-plugin/plugin.json" in f:
                plugins[name] = True
    return plugins


def get_diff(plugin_name: str) -> str:
    """Get staged diff for a specific plugin."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--", f"plugins/{plugin_name}/"],
        capture_output=True,
        text=True,
    )
    return result.stdout


def prompt_user() -> bool:
    """Ask user if they want to run version analysis.

    Controlled by VERSION_BUMP env var:
      - unset or "prompt": Interactive prompt (default yes if non-interactive)
      - "yes" or "auto": Skip prompt, proceed with analysis
      - "no" or "skip": Skip prompt, don't bump
    """
    mode = os.environ.get("VERSION_BUMP", "prompt").lower()

    if mode in ("yes", "auto"):
        return True
    if mode in ("no", "skip"):
        return False

    # Default: prompt mode
    if not sys.stdin.isatty():
        return True  # Non-interactive (CI, etc.) - proceed

    print(
        "\nPlugin changes detected. Run version analysis? [Y/n] ", end="", flush=True
    )
    response = input().strip().lower()
    return response in ("", "y", "yes")


def analyze_with_claude(plugins_and_diffs: dict[str, str]) -> dict[str, str]:
    """
    Ask Claude to determine bump levels for all plugins at once.

    Returns {plugin_name: "major"|"minor"|"patch"}
    Falls back to "patch" for all if Claude unavailable.
    """
    # Build combined prompt
    plugin_sections = []
    for name, diff in plugins_and_diffs.items():
        truncated = diff[:6000] if len(diff) > 6000 else diff
        plugin_sections.append(f"## Plugin: {name}\n```diff\n{truncated}\n```")

    prompt = f"""Analyze these Claude Code plugin diffs and determine the semantic version bump for each.

Guidelines:
- major: Breaking changes, removed features, incompatible API changes
- minor: New features, new agents, new commands, new skills, new capabilities
- patch: Bug fixes, documentation, refactoring, small improvements

Respond with ONLY a JSON object mapping plugin names to bump levels:
{{"plugin-name": "patch", "other-plugin": "minor"}}

{chr(10).join(plugin_sections)}"""

    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "json", "--max-turns", "1"],
            capture_output=True,
            text=True,
            timeout=120,
        )

        response = json.loads(result.stdout)
        result_text = response.get("result", "{}")

        # Extract JSON from response (Claude might wrap in markdown)
        if match := re.search(r"\{[^{}]+\}", result_text):
            return json.loads(match.group())

    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError, FileNotFoundError):
        print("  (Claude unavailable, defaulting to patch)", flush=True)

    # Fallback: patch for everything
    return {name: "patch" for name in plugins_and_diffs}


def bump_version(version: str, level: str) -> str:
    """Bump version according to semver level."""
    major, minor, patch = map(int, version.split("."))
    if level == "major":
        return f"{major + 1}.0.0"
    elif level == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def main():
    # Find plugins with staged changes (excluding manual plugin.json edits)
    plugins = get_staged_plugins()
    plugins_to_bump = {
        name: get_diff(name)
        for name, was_manual in plugins.items()
        if not was_manual and get_diff(name).strip()
    }

    if not plugins_to_bump:
        print("  No plugins changed; no version bump needed")
        sys.exit(0)

    # Interactive prompt
    if not prompt_user():
        print("  Skipping version bump")
        sys.exit(0)

    # Analyze with Claude
    print(f"  Analyzing {len(plugins_to_bump)} plugin(s)...", flush=True)
    bump_levels = analyze_with_claude(plugins_to_bump)

    # Apply bumps
    for plugin in plugins_to_bump:
        level = bump_levels.get(plugin, "patch")
        plugin_json = Path(f"plugins/{plugin}/.claude-plugin/plugin.json")

        if not plugin_json.exists():
            continue

        data = json.loads(plugin_json.read_text())
        old = data["version"]
        new = bump_version(old, level)
        data["version"] = new
        plugin_json.write_text(json.dumps(data, indent=2) + "\n")

        subprocess.run(["git", "add", str(plugin_json)])
        print(f"  {plugin}: {old} → {new} ({level})")

    sys.exit(0)


if __name__ == "__main__":
    main()
