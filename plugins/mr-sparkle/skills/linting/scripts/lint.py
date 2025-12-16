#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Universal polyglot linting CLI for Claude Code.

Detects file type by extension, finds project configuration,
and runs appropriate linters with smart tool selection.

Usage:
    lint.py <file_path>                    # Lint file (text output)
    lint.py <file_path> --format json      # JSON output
    lint.py <file_path> --format text      # Text output (default)
    lint.py --stdin-hook                   # Read hook JSON from stdin

Exit codes:
    0: Success (clean or fixed)
    1: Lint errors found (non-blocking)
    2: Tool execution error
"""

import argparse
import configparser
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

# tomllib is built-in Python 3.11+
try:
    import tomllib
except ImportError:
    tomllib = None  # type: ignore[assignment]


# =============================================================================
# Data Structures
# =============================================================================

EXTENSION_TO_TOOLSET = {
    ".py": "python",
    ".md": "markdown",
    ".markdown": "markdown",
    ".js": "js_ts",
    ".jsx": "js_ts",
    ".ts": "js_ts",
    ".tsx": "js_ts",
    ".mjs": "js_ts",
    ".cjs": "js_ts",
    ".mts": "js_ts",
    ".cts": "js_ts",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".rb": "ruby",
    ".rake": "ruby",
    ".gemspec": "ruby",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".json5": "json",
    ".jsonc": "json",
}

# Groups are in PRIORITY ORDER (first group with project config wins)
# Tools WITHIN a group run in LIST ORDER (e.g., isort before black)
# Fallback is always the first tool in the first group
TOOLSETS = {
    "python": [["ruff"], ["pylint", "isort", "black"]],
    "js_ts": [["biome"], ["eslint", "prettier"]],
    "markdown": [["mdformat", "markdownlint"]],
    "shell": [["shfmt", "shellcheck"]],
    "ruby": [["standard"], ["rubocop"]],
    "yaml": [["prettier"]],
    "json": [["prettier"]],
}

TOOLS = {
    "ruff": {
        "binary": "ruff",
        "commands": [
            ["ruff", "check", "--fix"],
            ["ruff", "format"],
        ],
        "config_indicators": ["ruff.toml", ".ruff.toml"],
        "pyproject_keys": ["tool.ruff"],
    },
    "black": {
        "binary": "black",
        "commands": [["black"]],
        "pyproject_keys": ["tool.black"],
    },
    "isort": {
        "binary": "isort",
        "commands": [["isort"]],
        "config_indicators": [".isort.cfg"],
        "pyproject_keys": ["tool.isort"],
        "ini_sections": [{"file": "setup.cfg", "section": "isort"}],
    },
    "pylint": {
        "binary": "pylint",
        "commands": [["pylint"]],
        "config_indicators": [".pylintrc", "pylintrc"],
        "pyproject_keys": ["tool.pylint"],
        "ini_sections": [{"file": "setup.cfg", "section": "pylint"}],
    },
    "biome": {
        "binary": "biome",
        "commands": [["biome", "check", "--fix"]],
        "config_indicators": ["biome.json", "biome.jsonc"],
        "packages": ["@biomejs/biome", "biome"],
    },
    "eslint": {
        "binary": "eslint",
        "commands": [["eslint", "--fix"]],
        "config_indicators": [
            "eslint.config.js",
            "eslint.config.mjs",
            "eslint.config.cjs",
            ".eslintrc",
            ".eslintrc.js",
            ".eslintrc.cjs",
            ".eslintrc.json",
            ".eslintrc.yaml",
            ".eslintrc.yml",
        ],
        "packages": ["eslint"],
        "needs_project_cwd": True,
    },
    "prettier": {
        "binary": "prettier",
        "commands": [["prettier", "--write"]],
        "config_indicators": [
            ".prettierrc",
            ".prettierrc.js",
            ".prettierrc.cjs",
            ".prettierrc.json",
            ".prettierrc.json5",
            ".prettierrc.yaml",
            ".prettierrc.yml",
            ".prettierrc.toml",
            "prettier.config.js",
            "prettier.config.cjs",
            "prettier.config.mjs",
        ],
        "packages": ["prettier"],
        "config_flag": "--config",
        "global_config_location": "~/.prettierrc.json5",
        "ignore_flag": "--ignore-path",
    },
    "markdownlint": {
        "binary": "markdownlint-cli2",
        "commands": [["markdownlint-cli2", "--fix"]],
        "config_indicators": [
            ".markdownlint-cli2.jsonc",
            ".markdownlint-cli2.yaml",
            ".markdownlint-cli2.cjs",
            ".markdownlint-cli2.mjs",
        ],
        "config_flag": "--config",
        "global_config_location": "~/.markdownlint-cli2.jsonc",
    },
    "mdformat": {
        "binary": "mdformat",
        "commands": [["mdformat"]],
        "pyproject_keys": ["tool.mdformat"],
    },
    "shfmt": {
        "binary": "shfmt",
        "commands": [["shfmt", "-w"]],
        "config_indicators": [".editorconfig"],
    },
    "shellcheck": {
        "binary": "shellcheck",
        "commands": [["shellcheck"]],
        "config_indicators": [".shellcheckrc"],
    },
    "standard": {
        "binary": "standardrb",
        "commands": [["standardrb", "--fix"]],
        "config_indicators": [".standard.yml"],
        "gemfile_gems": ["standard", "standardrb"],
    },
    "rubocop": {
        "binary": "rubocop",
        "commands": [["rubocop", "-a"]],
        "config_indicators": [".rubocop.yml", ".rubocop_todo.yml"],
        "gemfile_gems": ["rubocop"],
    },
}


class Status(Enum):
    """Status of a tool run."""

    OK = "ok"
    WARNING = "warning"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class ToolResult:
    """Result from running a tool."""

    name: str
    status: Status
    output: str = ""


# =============================================================================
# File Content Checks
# =============================================================================

# Git conflict marker patterns - must match at line start
CONFLICT_MARKERS = (b"<<<<<<<", b"=======", b">>>>>>>")


def has_conflict_markers(file_path: str) -> bool:
    """Check if file contains git conflict markers.

    Files mid-merge should not be formatted as formatters may corrupt
    the conflict markers, making resolution difficult.
    """
    try:
        with open(file_path, "rb") as f:
            for line in f:
                stripped = line.lstrip()
                for marker in CONFLICT_MARKERS:
                    if stripped.startswith(marker):
                        return True
        return False
    except (OSError, IOError):
        return False


# =============================================================================
# Config Detection Functions
# =============================================================================


def find_project_root(file_path: str) -> Optional[Path]:
    """Walk up directory tree to find project root."""
    path = Path(file_path).resolve().parent
    for parent in [path] + list(path.parents):
        if (parent / "package.json").is_file():
            return parent
        if (parent / "pyproject.toml").is_file():
            return parent
        if (parent / "Gemfile").is_file():
            return parent
        if (parent / ".git").exists():
            return parent
    return None


def check_pyproject_key(project_root: Path, key: str) -> bool:
    """Check if a dotted key exists in pyproject.toml."""
    if tomllib is None:
        return False

    pyproject = project_root / "pyproject.toml"
    if not pyproject.is_file():
        return False

    try:
        with open(pyproject, "rb") as f:
            data = tomllib.load(f)

        parts = key.split(".")
        current = data
        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return False
            current = current[part]
        return True
    except Exception:
        return False


def has_config_file(tool_def: dict, project_root: Path) -> bool:
    """Check if any config indicator files exist."""
    for cfg in tool_def.get("config_indicators", []):
        if (project_root / cfg).is_file():
            return True
    return False


def has_npm_package(tool_def: dict, project_root: Path) -> bool:
    """Check if tool is in package.json dependencies."""
    packages = tool_def.get("packages", [])
    if not packages:
        return False

    pkg_json = project_root / "package.json"
    if not pkg_json.is_file():
        return False

    try:
        data = json.loads(pkg_json.read_text())
        all_deps = {
            **data.get("dependencies", {}),
            **data.get("devDependencies", {}),
        }
        return any(pkg in all_deps for pkg in packages)
    except (json.JSONDecodeError, KeyError):
        return False


def has_gemfile_gem(tool_def: dict, project_root: Path) -> bool:
    """Check if tool is declared as a gem in Gemfile."""
    gems = tool_def.get("gemfile_gems", [])
    if not gems:
        return False

    gemfile = project_root / "Gemfile"
    if not gemfile.is_file():
        return False

    try:
        content = gemfile.read_text()
        # Match gem declarations: gem "name" or gem 'name'
        for gem_name in gems:
            # Pattern matches: gem "name" or gem 'name' with optional version specs
            if f'gem "{gem_name}"' in content or f"gem '{gem_name}'" in content:
                return True
        return False
    except Exception:
        return False


def has_pyproject_config(tool_def: dict, project_root: Path) -> bool:
    """Check if tool has config in pyproject.toml."""
    for key in tool_def.get("pyproject_keys", []):
        if check_pyproject_key(project_root, key):
            return True
    return False


def has_ini_section(tool_def: dict, project_root: Path) -> bool:
    """Check if tool has config section in an INI file (setup.cfg, etc.)."""
    ini_sections = tool_def.get("ini_sections", [])
    if not ini_sections:
        return False

    for entry in ini_sections:
        ini_file = project_root / entry["file"]
        section = entry["section"]

        if not ini_file.is_file():
            continue

        try:
            parser = configparser.ConfigParser()
            parser.read(ini_file)
            if parser.has_section(section):
                return True
        except configparser.Error:
            continue

    return False


def has_project_config(tool_name: str, project_root: Optional[Path]) -> bool:
    """Check if tool has project-level configuration."""
    if not project_root:
        return False

    tool_def = TOOLS[tool_name]

    if has_config_file(tool_def, project_root):
        return True
    if has_npm_package(tool_def, project_root):
        return True
    if has_gemfile_gem(tool_def, project_root):
        return True
    if has_pyproject_config(tool_def, project_root):
        return True
    if has_ini_section(tool_def, project_root):
        return True

    return False


def select_tools(toolset: str, project_root: Optional[Path]) -> list[str]:
    """Select tools to run based on project config."""
    groups = TOOLSETS[toolset]

    for group in groups:
        configured = [t for t in group if has_project_config(t, project_root)]
        if configured:
            return configured

    # No project config - fall back to entire first group
    return groups[0]


def get_skill_default_config(tool_name: str) -> Optional[Path]:
    """Get default config from skill directory if available."""
    # Self-locate: this script is at <plugin>/skills/linting/scripts/lint.py
    plugin_dir = Path(__file__).resolve().parent.parent.parent.parent

    config_map = {
        "markdownlint": plugin_dir / "skills" / "markdown-quality" / "default-config.jsonc",
        "prettier": plugin_dir / "skills" / "prettier-quality" / "default-config.json5",
    }

    skill_config = config_map.get(tool_name)
    if skill_config and skill_config.is_file():
        return skill_config
    return None


# =============================================================================
# Tool Execution
# =============================================================================


def run_tool(
    file_path: str,
    tool_name: str,
    project_root: Optional[Path],
) -> Optional[ToolResult]:
    """Run tool. Returns None if not installed (skip silently)."""
    tool_def = TOOLS[tool_name]
    binary = shutil.which(tool_def["binary"])
    if not binary:
        return None

    # Check if explicit global config is required
    has_config = has_project_config(tool_name, project_root)
    has_global_config = "global_config_location" in tool_def
    needs_explicit_config = not has_config and has_global_config

    # Resolve global config path
    global_cfg_path = tool_def.get("global_config_location", "")
    global_cfg = Path(global_cfg_path).expanduser() if global_cfg_path else None
    global_cfg_exists = global_cfg.is_file() if global_cfg else False

    # Try skill default config as fallback
    skill_default = get_skill_default_config(tool_name)

    # Determine which config to use
    config_to_use: Optional[Path] = None
    if needs_explicit_config:
        if global_cfg_exists:
            config_to_use = global_cfg
        elif skill_default:
            config_to_use = skill_default
        else:
            # No config available - skip
            return None

    # Build config args
    config_args: list[str] = []
    if config_to_use:
        config_flag = tool_def.get("config_flag", "--config")
        config_args = [config_flag, str(config_to_use)]

    # When using fallback config, disable ignore file to avoid picking up
    # unrelated ignore patterns from parent directories
    if needs_explicit_config and "ignore_flag" in tool_def:
        config_args.extend([tool_def["ignore_flag"], "/dev/null"])

    cwd = str(project_root) if project_root and tool_def.get("needs_project_cwd") else None

    all_output: list[str] = []
    worst_status = Status.OK

    for cmd_template in tool_def["commands"]:
        cmd = cmd_template.copy()
        cmd[0] = binary
        cmd.extend(config_args)
        cmd.append(file_path)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=60,
            )

            output = (result.stdout + result.stderr).strip()
            if output:
                all_output.append(output)

            if result.returncode != 0:
                # Non-zero exit typically means lint errors found
                if worst_status == Status.OK:
                    worst_status = Status.WARNING

        except subprocess.TimeoutExpired:
            all_output.append(f"{tool_def['binary']} timed out after 60s")
            worst_status = Status.ERROR
        except Exception as e:
            all_output.append(f"{tool_def['binary']} error: {e}")
            worst_status = Status.ERROR

    return ToolResult(
        name=tool_def["binary"],
        status=worst_status,
        output="\n".join(all_output),
    )


# =============================================================================
# Output Formatting
# =============================================================================


def format_text_output(file_path: str, results: list[ToolResult]) -> tuple[str, int]:
    """Format results as human-readable text. Returns (output, exit_code)."""
    filename = Path(file_path).name
    ran = [r for r in results if r.status != Status.SKIPPED]

    if not ran:
        return "", 0

    tools_str = ", ".join(r.name for r in ran)
    has_error = any(r.status == Status.ERROR for r in ran)
    has_warning = any(r.status == Status.WARNING for r in ran)

    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"

    lines = []

    if has_error:
        error_output = next((r.output for r in ran if r.status == Status.ERROR and r.output), "")
        if error_output:
            first_line = error_output.split("\n")[0]
            if ": " in first_line:
                first_line = first_line.split(": ", 1)[-1]
            short_error = first_line[:50] + "..." if len(first_line) > 50 else first_line
        else:
            short_error = "execution failed"
        lines.append(f"{RED}✗ {tools_str} {filename}: {short_error}{RESET}")
        exit_code = 2
    elif has_warning:
        lines.append(f"{YELLOW}⚠ {tools_str} {filename}: Lint errors!{RESET}")
        exit_code = 1
    else:
        lines.append(f"{GREEN}✓ {tools_str} {filename}: OK{RESET}")
        exit_code = 0

    # Add detailed output for warnings/errors
    for r in results:
        if r.output and r.status in (Status.WARNING, Status.ERROR):
            lines.append(r.output)

    return "\n".join(lines), exit_code


def format_json_output(file_path: str, toolset: str, results: list[ToolResult]) -> tuple[str, int]:
    """Format results as JSON. Returns (output, exit_code)."""
    ran = [r for r in results if r.status != Status.SKIPPED]

    has_error = any(r.status == Status.ERROR for r in ran)
    has_warning = any(r.status == Status.WARNING for r in ran)

    if has_error:
        overall_status = "error"
        exit_code = 2
    elif has_warning:
        overall_status = "warning"
        exit_code = 1
    else:
        overall_status = "ok"
        exit_code = 0

    output = {
        "file": file_path,
        "toolset": toolset,
        "tools_run": [r.name for r in ran],
        "status": overall_status,
        "results": [{"tool": r.name, "status": r.status.value, "output": r.output} for r in ran],
    }

    return json.dumps(output, indent=2), exit_code


def format_hook_output(file_path: str, results: list[ToolResult], verbose: bool = False) -> tuple[str, int]:
    """Format results as hook-compatible JSON. Returns (output, exit_code)."""
    filename = Path(file_path).name
    ran = [r for r in results if r.status != Status.SKIPPED]

    if not ran:
        return "", 0

    tools_str = ", ".join(r.name for r in ran)
    has_error = any(r.status == Status.ERROR for r in ran)
    has_warning = any(r.status == Status.WARNING for r in ran)

    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"

    if has_error:
        error_output = next((r.output for r in ran if r.status == Status.ERROR and r.output), "")
        if error_output:
            first_line = error_output.split("\n")[0]
            if ": " in first_line:
                first_line = first_line.split(": ", 1)[-1]
            short_error = first_line[:50] + "..." if len(first_line) > 50 else first_line
        else:
            short_error = "execution failed"
        summary = f"{RED}✗ {tools_str} {filename}: {short_error}{RESET}"
        exit_code = 2
    elif has_warning:
        summary = f"{YELLOW}⚠ {tools_str} {filename}: Lint errors!{RESET}"
        exit_code = 1
    else:
        summary = f"{GREEN}✓ {tools_str} {filename}: OK{RESET}"
        exit_code = 0

    response: dict = {"systemMessage": summary}

    # Only include additionalContext when verbose
    if verbose:
        context_parts = [r.output for r in results if r.output]
        if context_parts:
            additional_context = "\n".join(context_parts)
        else:
            additional_context = f"{tools_str} {filename}: OK"

        response["hookSpecificOutput"] = {
            "hookEventName": "PostToolUse",
            "additionalContext": additional_context,
        }

    return json.dumps(response), exit_code


# =============================================================================
# Main Entry Points
# =============================================================================


def lint_file(
    file_path: str,
    output_format: str = "text",
    verbose: bool = False,
) -> tuple[str, int]:
    """
    Lint a file and return formatted output.

    Args:
        file_path: Path to file to lint
        output_format: One of "text", "json", "hook"
        verbose: Include detailed output in hook mode

    Returns:
        Tuple of (formatted_output, exit_code)
    """
    if not Path(file_path).is_file():
        return "", 0

    # Skip files with git conflict markers - formatters may corrupt them
    if has_conflict_markers(file_path):
        return "", 0

    ext = Path(file_path).suffix.lower()
    toolset = EXTENSION_TO_TOOLSET.get(ext)
    if not toolset:
        return "", 0

    project_root = find_project_root(file_path)
    tools_to_run = select_tools(toolset, project_root)

    if not tools_to_run:
        return "", 0

    results: list[ToolResult] = []
    for tool_name in tools_to_run:
        result = run_tool(file_path, tool_name, project_root)
        if result:
            results.append(result)

    if not results:
        return "", 0

    if output_format == "json":
        return format_json_output(file_path, toolset, results)
    elif output_format == "hook":
        return format_hook_output(file_path, results, verbose=verbose)
    else:
        return format_text_output(file_path, results)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Universal polyglot linting CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s file.py                    Lint Python file
  %(prog)s file.md --format json      Lint markdown, JSON output
  %(prog)s --stdin-hook               Read hook JSON from stdin
        """,
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="File to lint",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "hook"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--stdin-hook",
        action="store_true",
        help="Read hook JSON from stdin (for hooks.json integration)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include detailed output in hook mode (default: summary only)",
    )

    args = parser.parse_args()

    # Handle stdin-hook mode
    if args.stdin_hook:
        try:
            hook_input = json.load(sys.stdin)
        except json.JSONDecodeError:
            sys.exit(0)

        tool_input = hook_input.get("tool_input", {})
        file_path = tool_input.get("file_path")
        if not file_path or not isinstance(file_path, str):
            sys.exit(0)

        output, exit_code = lint_file(file_path, output_format="hook", verbose=args.verbose)
        if output:
            print(output, flush=True)
        sys.exit(0)  # Hooks should not block

    # Normal CLI mode
    if not args.file:
        parser.error("file is required unless using --stdin-hook")

    output, exit_code = lint_file(args.file, output_format=args.format)

    if output:
        print(output)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
