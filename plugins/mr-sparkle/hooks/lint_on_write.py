#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Generic PostToolUse linting hook for Claude Code.

Reads stdin JSON to extract file paths, detects file type by extension,
and runs appropriate linter commands.

Exit codes:
- 0: Success or silently skipped (file formatted or no issues)
- 1: Non-blocking error (unfixable linting issues, linter errors)
"""

import configparser
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

# tomllib is built-in Python 3.11+, used for pyproject.toml parsing
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
}

# Groups are in PRIORITY ORDER (first group with project config wins)
# Tools WITHIN a group run in LIST ORDER (e.g., isort before black)
# Fallback is always the first tool in the first group
TOOLSETS = {
    "python": [["ruff"], ["pylint", "isort", "black"]],
    "js_ts": [["biome"], ["eslint", "prettier"]],
    "markdown": [["markdownlint"]],
    "shell": [["shfmt", "shellcheck"]],
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
            ".prettierrc.yaml",
            ".prettierrc.yml",
            ".prettierrc.toml",
            "prettier.config.js",
            "prettier.config.cjs",
            "prettier.config.mjs",
        ],
        "packages": ["prettier"],
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
# Core Functions
# =============================================================================


def find_project_root(file_path: str) -> Optional[Path]:
    """Walk up directory tree to find project root."""
    path = Path(file_path).resolve().parent
    for parent in [path] + list(path.parents):
        if (parent / "package.json").is_file():
            return parent
        if (parent / "pyproject.toml").is_file():
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

    # Skip if explicit config needed but missing
    missing_required_config = needs_explicit_config and not global_cfg_exists
    if missing_required_config:
        return None

    # Build config args
    config_args: list[str] = []
    if needs_explicit_config:
        config_flag = tool_def.get("config_flag", "--config")
        config_args = [config_flag, str(global_cfg)]

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


def format_results(file_path: str, results: list[ToolResult]) -> tuple[str, Optional[str]]:
    """Format results into summary line and optional context."""
    filename = Path(file_path).name
    ran = [r for r in results if r.status != Status.SKIPPED]

    if not ran:
        return "", None

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
    elif has_warning:
        summary = f"{YELLOW}⚠ {tools_str} {filename}: Lint errors!{RESET}"
    else:
        summary = f"{GREEN}✓ {tools_str} {filename}: OK{RESET}"

    # Include detailed output for warnings/errors, or summary for OK status
    context_parts = [r.output for r in results if r.output and r.status in (Status.WARNING, Status.ERROR)]
    if context_parts:
        additional_context = "\n".join(context_parts)
    elif ran:
        # Surface OK status to Claude so it knows linting ran successfully
        additional_context = f"{tools_str} {filename}: OK"
    else:
        additional_context = None

    return summary, additional_context


def output_response(
    system_message: Optional[str] = None,
    additional_context: Optional[str] = None,
) -> None:
    """Output JSON response to stdout."""
    response: dict = {}

    if system_message:
        response["systemMessage"] = system_message

    if additional_context:
        response["hookSpecificOutput"] = {
            "hookEventName": "PostToolUse",
            "additionalContext": additional_context,
        }

    if response:
        print(json.dumps(response), flush=True)


def read_hook_input() -> dict:
    """Read and parse JSON from stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)


def extract_file_path(hook_input: dict) -> Optional[str]:
    """Extract file_path from tool_input."""
    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path")
    if not file_path or not isinstance(file_path, str):
        return None
    return file_path


def main():
    """Main hook execution."""
    hook_input = read_hook_input()
    file_path = extract_file_path(hook_input)

    if not file_path or not Path(file_path).is_file():
        sys.exit(0)

    ext = Path(file_path).suffix.lower()
    toolset = EXTENSION_TO_TOOLSET.get(ext)
    if not toolset:
        sys.exit(0)

    project_root = find_project_root(file_path)
    tools_to_run = select_tools(toolset, project_root)

    if not tools_to_run:
        sys.exit(0)

    results: list[ToolResult] = []
    for tool_name in tools_to_run:
        result = run_tool(file_path, tool_name, project_root)
        if result:
            results.append(result)

    if results:
        summary, context = format_results(file_path, results)
        if summary:
            output_response(system_message=summary, additional_context=context)

    sys.exit(0)


if __name__ == "__main__":
    main()
