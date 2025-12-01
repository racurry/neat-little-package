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
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Tuple

# tomllib is built-in Python 3.11+, used for pyproject.toml parsing
try:
    import tomllib
except ImportError:
    tomllib = None  # type: ignore[assignment]


class Status(Enum):
    """Status of a linter stage or overall result."""
    OK = "ok"           # Ran successfully
    WARNING = "warning" # Found issues needing manual fix
    ERROR = "error"     # Tool failed or unexpected error
    SKIPPED = "skipped" # Tool not installed (optional)


@dataclass
class StageResult:
    """Result from running a single linter stage."""
    name: str
    status: Status
    output: str = ""


# Configuration: Map file extensions to linter pipeline configurations
# Each config has "extensions" and "pipeline" (list of stages to run in sequence)
# Stage options:
#   - name: Display name for the tool
#   - command: Command array to run
#   - check_installed: Binary name to check for availability
#   - unfixable_exit_code: Exit code indicating lint errors needing manual fix
#   - optional: If True, skip silently when tool not installed
#   - config_resolver: Key into CONFIG_RESOLVERS for dynamic config file lookup
LINTER_CONFIG = {
    "markdown": {
        "extensions": [".md", ".markdown"],
        "pipeline": [{
            "name": "markdownlint",
            "command": ["markdownlint-cli2", "--fix"],
            "check_installed": "markdownlint-cli2",
            "unfixable_exit_code": 1,
            "config_resolver": "markdown",
        }],
    },
    "python": {
        "extensions": [".py"],
        "pipeline_resolver": "python",
    },
    "shell": {
        "extensions": [".sh", ".bash", ".zsh"],
        "pipeline": [
            {
                "name": "shfmt",
                "command": ["shfmt", "-w"],
                "check_installed": "shfmt",
                "optional": True,
            },
            {
                "name": "shellcheck",
                "command": ["shellcheck"],
                "check_installed": "shellcheck",
                "unfixable_exit_code": 1,
                "optional": True,
            },
        ],
    },
    "javascript": {
        "extensions": [".js", ".jsx", ".mjs", ".cjs"],
        "pipeline_resolver": "js_ts",
    },
    "typescript": {
        "extensions": [".ts", ".tsx", ".mts", ".cts"],
        "pipeline_resolver": "js_ts",
    },
}

# Tool detection configuration for dynamic pipeline resolution
# JS/TS tools use "packages" (package.json), Python tools use "pyproject_keys" (pyproject.toml)
TOOL_DETECTION = {
    # JS/TS tools
    "biome": {
        "configs": ["biome.json", "biome.jsonc"],
        "packages": ["@biomejs/biome", "biome"],
    },
    "eslint": {
        "configs": [
            ".eslintrc",
            ".eslintrc.js",
            ".eslintrc.cjs",
            ".eslintrc.json",
            ".eslintrc.yaml",
            ".eslintrc.yml",
            "eslint.config.js",
            "eslint.config.mjs",
            "eslint.config.cjs",
        ],
        "packages": ["eslint"],
    },
    "prettier": {
        "configs": [
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
    # Python tools
    "ruff": {
        "configs": ["ruff.toml", ".ruff.toml"],
        "pyproject_keys": ["tool.ruff"],
    },
    "black": {
        "configs": [],  # Black rarely uses standalone config files
        "pyproject_keys": ["tool.black"],
    },
    "isort": {
        "configs": [".isort.cfg"],
        "pyproject_keys": ["tool.isort"],
    },
}

# Map config_resolver keys to resolver functions (populated after function definitions)
CONFIG_RESOLVERS: Dict[str, callable] = {}


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


def resolve_biome_config() -> Optional[str]:
    """
    Resolve biome config for fallback (no project config).

    Hierarchy:
    1. User config: ~/.config/biome/biome.json
    2. Skill default: <plugin>/skills/js-quality/default-biome.json

    Returns:
        Path to config file, or None if not found
    """
    # User config
    user_config = Path.home() / ".config" / "biome" / "biome.json"
    if user_config.is_file():
        return str(user_config)

    # Skill default
    plugin_dir = Path(__file__).resolve().parent.parent
    skill_config = plugin_dir / "skills" / "js-quality" / "default-biome.json"
    if skill_config.is_file():
        return str(skill_config)

    return None


def find_project_root(file_path: str) -> Optional[Path]:
    """Walk up directory tree to find project root (package.json, pyproject.toml, or .git)."""
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
    """
    Check if a key exists in pyproject.toml.

    Args:
        project_root: Path to project root
        key: Dot-notation key like "tool.ruff" or "tool.black"

    Returns:
        True if key exists in pyproject.toml
    """
    if tomllib is None:
        return False

    pyproject = project_root / "pyproject.toml"
    if not pyproject.is_file():
        return False

    try:
        with open(pyproject, "rb") as f:
            data = tomllib.load(f)

        # Navigate dot-notation key (e.g., "tool.ruff" -> data["tool"]["ruff"])
        parts = key.split(".")
        current = data
        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return False
            current = current[part]
        return True
    except Exception:
        return False


def detect_tool(project_root: Path, tool: str) -> bool:
    """Check if a tool is configured in project (JS/TS or Python)."""
    info = TOOL_DETECTION.get(tool)
    if not info:
        return False

    # Check config files
    for config in info.get("configs", []):
        if (project_root / config).is_file():
            return True

    # Check package.json dependencies (JS/TS tools)
    if "packages" in info:
        pkg_json = project_root / "package.json"
        if pkg_json.is_file():
            try:
                data = json.loads(pkg_json.read_text())
                all_deps = {
                    **data.get("dependencies", {}),
                    **data.get("devDependencies", {}),
                }
                if any(pkg in all_deps for pkg in info["packages"]):
                    return True
            except (json.JSONDecodeError, KeyError):
                pass

    # Check pyproject.toml keys (Python tools)
    if "pyproject_keys" in info:
        for key in info["pyproject_keys"]:
            if check_pyproject_key(project_root, key):
                return True

    return False


def make_stage(tool: str, project_root: Optional[Path], base_command: list[str]) -> Dict:
    """Create pipeline stage, preferring local binary if available."""
    command = base_command.copy()

    # Prefer local node_modules binary
    if project_root:
        local_bin = project_root / "node_modules" / ".bin" / tool
        if local_bin.is_file():
            command[0] = str(local_bin)

    stage = {
        "name": tool,
        "command": command,
        "check_installed": command[0],  # Check whatever we're actually running
        "unfixable_exit_code": 1,
    }

    # Set cwd for tools that need it (eslint v9 looks for config from cwd)
    if project_root:
        stage["cwd"] = str(project_root)

    return stage


def resolve_js_ts_pipeline(file_path: str) -> list[Dict]:
    """
    Detect project tooling and return appropriate pipeline.

    Priority:
    1. Biome (if project configured)
    2. ESLint + Prettier (if both configured)
    3. ESLint only
    4. Prettier only
    5. Fallback: Global Biome with user/skill config
    """
    project_root = find_project_root(file_path)

    if project_root:
        has_biome = detect_tool(project_root, "biome")
        has_eslint = detect_tool(project_root, "eslint")
        has_prettier = detect_tool(project_root, "prettier")

        if has_biome:
            return [make_stage("biome", project_root, ["biome", "check", "--fix"])]

        if has_eslint or has_prettier:
            pipeline = []
            if has_eslint:
                pipeline.append(make_stage("eslint", project_root, ["eslint", "--fix"]))
            if has_prettier:
                pipeline.append(make_stage("prettier", project_root, ["prettier", "--write"]))
            return pipeline

    # Fallback: global biome with config
    return [{
        "name": "biome",
        "command": ["biome", "check", "--fix"],
        "check_installed": "biome",
        "unfixable_exit_code": 1,
        "config_resolver": "biome",
    }]


def resolve_ruff_config() -> Optional[str]:
    """
    Resolve ruff config for fallback (no project config).

    Hierarchy:
    1. User config: ~/.config/ruff/ruff.toml
    2. Skill default: <plugin>/skills/python-quality/default-ruff.toml

    Returns:
        Path to config file, or None if not found
    """
    # User config (XDG standard location)
    user_config = Path.home() / ".config" / "ruff" / "ruff.toml"
    if user_config.is_file():
        return str(user_config)

    # Skill default
    plugin_dir = Path(__file__).resolve().parent.parent
    skill_config = plugin_dir / "skills" / "python-quality" / "default-ruff.toml"
    if skill_config.is_file():
        return str(skill_config)

    return None


def resolve_python_pipeline(file_path: str) -> list[Dict]:
    """
    Detect project tooling and return appropriate pipeline for Python.

    Priority:
    1. Ruff (if project configured) - does lint + format
    2. Black + isort (if both configured)
    3. Black only
    4. isort only
    5. Fallback: Global Ruff with user/skill config
    """
    project_root = find_project_root(file_path)

    if project_root:
        has_ruff = detect_tool(project_root, "ruff")
        has_black = detect_tool(project_root, "black")
        has_isort = detect_tool(project_root, "isort")

        if has_ruff:
            # Ruff does both linting and formatting
            return [
                make_stage("ruff", project_root, ["ruff", "check", "--fix"]),
                make_stage("ruff", project_root, ["ruff", "format"]),
            ]

        if has_black or has_isort:
            pipeline = []
            # isort runs first (import sorting before formatting)
            if has_isort:
                pipeline.append(make_stage("isort", project_root, ["isort"]))
            if has_black:
                pipeline.append(make_stage("black", project_root, ["black"]))
            return pipeline

    # Fallback: global ruff with config
    return [
        {
            "name": "ruff",
            "command": ["ruff", "check", "--fix"],
            "check_installed": "ruff",
            "unfixable_exit_code": 1,
            "config_resolver": "ruff",
        },
        {
            "name": "ruff",
            "command": ["ruff", "format"],
            "check_installed": "ruff",
            "unfixable_exit_code": 1,
            "config_resolver": "ruff",
        },
    ]


# Populate CONFIG_RESOLVERS after function definitions
CONFIG_RESOLVERS.update({
    "markdown": resolve_markdown_config,
    "biome": resolve_biome_config,
    "ruff": resolve_ruff_config,
})

# Map pipeline_resolver keys to resolver functions
PIPELINE_RESOLVERS = {
    "js_ts": resolve_js_ts_pipeline,
    "python": resolve_python_pipeline,
}


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

    # Add config flag if explicit config file specified
    if config_file:
        tool_name = config.get("name", "")
        if tool_name == "biome":
            command.extend(["--config-path", config_file])
        else:
            command.extend(["--config", config_file])

    command.append(file_path)

    # Get working directory if specified (needed for eslint v9 config discovery)
    cwd = config.get("cwd")

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=60  # Safety timeout
        )

        # Combine stdout and stderr for complete output
        output = result.stdout + result.stderr
        return (result.returncode, output.strip())

    except subprocess.TimeoutExpired:
        return (1, "Linter timed out after 60 seconds")
    except Exception as e:
        return (1, f"Linter execution error: {str(e)}")


def run_pipeline(file_path: str, stages: list[Dict]) -> list[StageResult]:
    """
    Run a pipeline of linter stages on a file.

    Args:
        file_path: Path to file to lint
        stages: List of stage configurations

    Returns:
        List of StageResult objects
    """
    results: list[StageResult] = []

    for stage in stages:
        tool_name = stage.get("name", stage["check_installed"])

        # Check if tool is installed
        if not check_tool_installed(stage["check_installed"]):
            if stage.get("optional", False):
                results.append(StageResult(name=tool_name, status=Status.SKIPPED))
                continue
            else:
                results.append(StageResult(
                    name=tool_name,
                    status=Status.ERROR,
                    output=f"{tool_name} not installed (required)"
                ))
                break

        # Resolve config file if stage has a config_resolver
        config_file = None
        if "config_resolver" in stage:
            resolver = CONFIG_RESOLVERS.get(stage["config_resolver"])
            if resolver:
                config_file = resolver()

        # Run the linter stage
        exit_code, output = run_linter(file_path, stage, config_file)

        if exit_code == 0:
            results.append(StageResult(name=tool_name, status=Status.OK))
        elif "unfixable_exit_code" in stage and exit_code == stage["unfixable_exit_code"]:
            # Linter found issues needing manual fix (expected behavior)
            results.append(StageResult(name=tool_name, status=Status.WARNING, output=output))
        else:
            # Tool error (parse failure, crash, etc.)
            results.append(StageResult(
                name=tool_name,
                status=Status.ERROR,
                output=output or f"exit code {exit_code}"
            ))

    return results


def format_summary_line(file_path: str, results: list[StageResult]) -> tuple[str, Optional[str]]:
    """
    Format a single-line summary of linting results.

    Format: icon tools filename [: message]
    - ✓ ruff goodfile.py
    - ⚠ markdownlint badfile.md: Lint errors!
    - ✗ shfmt, shellcheck somefile.bash: Error - message

    Args:
        file_path: Path to the file that was linted
        results: List of StageResult objects

    Returns:
        Tuple of (summary_line, additional_context_or_none)
    """
    filename = Path(file_path).name

    # Filter out skipped stages for display
    ran_stages = [r for r in results if r.status != Status.SKIPPED]

    if not ran_stages:
        # No tools ran (all skipped)
        return "", None

    # Build tool list
    tools_str = ", ".join(r.name for r in ran_stages)

    # Determine overall status and build message
    has_error = any(r.status == Status.ERROR for r in ran_stages)
    has_warning = any(r.status == Status.WARNING for r in ran_stages)

    # ANSI colors
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"

    if has_error:
        # Find first error message
        error_output = next((r.output for r in ran_stages if r.status == Status.ERROR and r.output), "")
        if error_output:
            # Take first line, strip file path prefix if present, truncate
            first_line = error_output.split('\n')[0]
            # Strip common path prefixes (full path or relative)
            if ': ' in first_line:
                first_line = first_line.split(': ', 1)[-1]
            short_error = first_line[:50] + "..." if len(first_line) > 50 else first_line
        else:
            short_error = "execution failed"
        summary = f"{RED}✗ {tools_str} {filename}: {short_error}{RESET}"
    elif has_warning:
        summary = f"{YELLOW}⚠ {tools_str} {filename}: Lint errors!{RESET}"
    else:
        summary = f"{GREEN}✓ {tools_str} {filename}: OK{RESET}"

    # Collect additional context (error/warning output) for Claude
    context_parts = [r.output for r in results if r.output and r.status in (Status.WARNING, Status.ERROR)]
    additional_context = "\n".join(context_parts) if context_parts else None

    return summary, additional_context


def get_pipeline(file_path: str, config: Dict) -> list[Dict]:
    """
    Get pipeline stages - static or dynamically resolved.

    Args:
        file_path: Path to the file (needed for dynamic resolution)
        config: Language config from LINTER_CONFIG

    Returns:
        List of pipeline stage configurations
    """
    # Static pipeline
    if "pipeline" in config:
        return config["pipeline"]

    # Dynamic pipeline via resolver
    if "pipeline_resolver" in config:
        resolver = PIPELINE_RESOLVERS.get(config["pipeline_resolver"])
        if resolver:
            return resolver(file_path)

    return []


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

    _, config = linter_info

    # Get pipeline (static or dynamically resolved)
    pipeline = get_pipeline(file_path, config)

    # Exit silently if no pipeline stages
    if not pipeline:
        sys.exit(0)

    # Run pipeline of linter stages
    results = run_pipeline(file_path, pipeline)
    summary, additional_context = format_summary_line(file_path, results)

    if summary:
        output_json_response(system_message=summary, additional_context=additional_context)

    sys.exit(0)


if __name__ == "__main__":
    main()
