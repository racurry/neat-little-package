#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Generic PostToolUse linting hook for Claude Code.

Reads stdin JSON to extract file paths, detects file type by extension,
and runs appropriate linter commands. Designed for extensibility to support
multiple languages (markdown, JavaScript, Python, Go, etc.).

Exit codes:
- 0: Success or silently skipped (file formatted or no issues)
- 1: Non-blocking error (unfixable linting issues, linter errors)
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple


# Configuration: Map file extensions to linter configurations
# Each config includes: command, extensions, success messages, error handling
LINTER_CONFIG = {
    "markdown": {
        "extensions": [".md", ".markdown"],
        "command": ["markdownlint-cli2", "--fix"],
        "check_installed": "markdownlint-cli2",
        "success_message": "Markdown formatted: {file_path}",
        "unfixable_message": "Markdown linting found unfixable issues in {file_path}",
        "unfixable_hint": "Run: markdownlint-cli2 {file_path} to see details",
        "unfixable_exit_code": 1,  # markdownlint-cli2 returns 1 for unfixable issues
    },
    # Example: Future JavaScript/TypeScript support
    # "javascript": {
    #     "extensions": [".js", ".jsx", ".ts", ".tsx"],
    #     "command": ["eslint", "--fix"],
    #     "check_installed": "eslint",
    #     "success_message": "JavaScript formatted: {file_path}",
    #     "unfixable_message": "ESLint found unfixable issues in {file_path}",
    #     "unfixable_hint": "Run: eslint {file_path} to see details",
    #     "unfixable_exit_code": 1,
    # },
    # Example: Future Python support
    # "python": {
    #     "extensions": [".py"],
    #     "command": ["ruff", "check", "--fix"],
    #     "check_installed": "ruff",
    #     "success_message": "Python formatted: {file_path}",
    #     "unfixable_message": "Ruff found unfixable issues in {file_path}",
    #     "unfixable_hint": "Run: ruff check {file_path} to see details",
    #     "unfixable_exit_code": 1,
    # },
}


def resolve_markdown_config() -> Optional[str]:
    """
    Resolve markdownlint config file using hierarchy:
    1. Project config - .markdownlint-cli2.* in cwd
    2. User config - ~/.markdownlint-cli2.jsonc
    3. Skill default - plugin's default-config.jsonc

    Returns:
        Path to config file, or None if using project config (let markdownlint auto-discover)
    """
    # Check for project config in current directory
    project_config_patterns = [
        ".markdownlint-cli2.jsonc",
        ".markdownlint-cli2.yaml",
        ".markdownlint-cli2.cjs",
        ".markdownlint-cli2.mjs"
    ]

    for config_file in project_config_patterns:
        if Path(config_file).is_file():
            # Found project config - return None to let markdownlint auto-discover
            return None

    # Check for user config
    home = Path.home()
    user_config = home / ".markdownlint-cli2.jsonc"
    if user_config.is_file():
        return str(user_config)

    # Fall back to skill default config
    # Self-locate: this script is at <plugin_root>/hooks/lint-on-write.py
    plugin_dir = Path(__file__).resolve().parent.parent
    skill_config = plugin_dir / "skills" / "markdown-quality" / "default-config.jsonc"

    if skill_config.is_file():
        return str(skill_config)

    # No config found - let markdownlint use its built-in defaults
    return None


def read_stdin_json() -> Dict:
    """Read and parse JSON from stdin (hook input)."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        # Invalid JSON - exit silently (non-blocking)
        sys.exit(0)


def extract_file_path(hook_input: Dict) -> Optional[str]:
    """Extract file_path from tool_input in hook JSON."""
    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path")

    # Handle both string and null/missing values
    if not file_path or not isinstance(file_path, str):
        return None

    return file_path


def get_linter_config(file_path: str) -> Optional[Tuple[str, Dict]]:
    """
    Determine linter config based on file extension.

    Returns:
        Tuple of (language_name, config_dict) or None if no match
    """
    file_ext = Path(file_path).suffix.lower()

    for language, config in LINTER_CONFIG.items():
        if file_ext in config["extensions"]:
            return (language, config)

    return None


def check_tool_installed(command_name: str) -> bool:
    """Check if a command-line tool is installed and available."""
    try:
        subprocess.run(
            ["command", "-v", command_name],
            check=True,
            capture_output=True,
            shell=False
        )
        return True
    except subprocess.CalledProcessError:
        return False


def run_linter(file_path: str, config: Dict, config_file: Optional[str] = None) -> Tuple[int, str]:
    """
    Run linter command on file.

    Args:
        file_path: Path to file to lint
        config: Linter configuration dict
        config_file: Optional path to config file to use

    Returns:
        Tuple of (exit_code, output)
    """
    command = config["command"].copy()

    # Add --config flag if explicit config file specified
    if config_file:
        command.extend(["--config", config_file])

    command.append(file_path)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60  # Safety timeout
        )

        # Combine stdout and stderr for complete output
        output = result.stdout + result.stderr
        return (result.returncode, output.strip())

    except subprocess.TimeoutExpired:
        return (1, f"Linter timed out after 60 seconds")
    except Exception as e:
        return (1, f"Linter execution error: {str(e)}")


def format_message(template: str, **kwargs) -> str:
    """Format message template with provided variables."""
    return template.format(**kwargs)


def output_json_response(system_message: Optional[str] = None, additional_context: Optional[str] = None, decision: Optional[str] = None, reason: Optional[str] = None):
    """Output JSON response to stdout for Claude to process."""
    response = {}

    if decision:
        response["decision"] = decision

    if reason:
        response["reason"] = reason

    if system_message:
        response["systemMessage"] = system_message

    if additional_context:
        response["hookSpecificOutput"] = {
            "hookEventName": "PostToolUse",
            "additionalContext": additional_context
        }

    print(json.dumps(response), flush=True)


def main():
    """Main hook execution logic."""
    # Debug: log that hook was triggered
    import datetime
    with open("/tmp/hook-test.log", "a") as f:
        f.write(f"{datetime.datetime.now()}: Hook triggered\n")

    # Read hook input from stdin
    hook_input = read_stdin_json()

    # Extract file path from tool_input
    file_path = extract_file_path(hook_input)

    # Exit silently if no file path (not a file write/edit operation)
    if not file_path:
        sys.exit(0)

    # Verify file exists
    if not Path(file_path).is_file():
        sys.exit(0)

    # Get linter configuration for this file type
    linter_info = get_linter_config(file_path)

    # Exit silently if no linter configured for this file type
    if not linter_info:
        sys.exit(0)

    _language, config = linter_info

    # Check if linter tool is installed
    if not check_tool_installed(config["check_installed"]):
        # Not installed - exit silently (non-blocking)
        # User can install the tool if desired
        sys.exit(0)

    # Resolve config file for markdown (other linters can add their own resolvers)
    config_file = None
    if _language == "markdown":
        config_file = resolve_markdown_config()

    # Run the linter
    exit_code, output = run_linter(file_path, config, config_file)

    # Handle linter results
    if exit_code == 0:
        # Success - file was clean or successfully fixed
        success_msg = format_message(
            config["success_message"],
            file_path=file_path
        )
        output_json_response(system_message=success_msg)
        sys.exit(0)

    elif exit_code == config.get("unfixable_exit_code", 1):
        # Linter found issues that couldn't be auto-fixed
        unfixable_msg = format_message(
            config["unfixable_message"],
            file_path=file_path
        )

        # Build complete context message
        context_parts = [unfixable_msg]
        if output:
            context_parts.append(output)
        if "unfixable_hint" in config:
            hint = format_message(
                config["unfixable_hint"],
                file_path=file_path
            )
            context_parts.append(hint)

        full_context = "\n".join(context_parts)
        output_json_response(system_message=full_context, additional_context=output)
        sys.exit(0)

    else:
        # Unexpected exit code - report error
        error_msg = f"Linter error (exit code {exit_code}) in {file_path}:"

        context_parts = [error_msg]
        if output:
            context_parts.append(output)

        full_context = "\n".join(context_parts)
        output_json_response(system_message=full_context)
        sys.exit(0)


if __name__ == "__main__":
    main()
