"""
Shared configuration reader for neat-little-package plugin hooks.

Reads per-plugin TOML config from ~/.config/neat-little-package/{plugin}.toml
with directory-pattern overrides (like git includeIf).

Usage from a hook script:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "_lib"))
    from plugin_config import get_plugin_config

    config = get_plugin_config("mr-sparkle", cwd="/path/to/project")
    if not config.get("lint_on_write", True):
        sys.exit(0)
"""

import os
import tomllib
from pathlib import Path
from typing import Any

CONFIG_DIR = Path(os.environ.get("NLP_CONFIG_DIR", "~/.config/neat-little-package")).expanduser()


def _normalize_match(pattern: str) -> str:
    """Expand ~ and strip trailing glob suffixes to get a directory prefix."""
    expanded = str(Path(pattern).expanduser())
    for suffix in ("/**", "/*"):
        if expanded.endswith(suffix):
            expanded = expanded[: -len(suffix)]
            break
    # Remove trailing slash
    return expanded.rstrip("/")


def _path_matches(cwd: str, pattern: str) -> bool:
    """Check if cwd is inside the directory specified by pattern.

    Uses simple prefix matching after ~ expansion. Patterns like
    ~/workspace/foo and ~/workspace/foo/** both match any cwd
    at or below that directory.
    """
    prefix = _normalize_match(pattern)
    return cwd == prefix or cwd.startswith(prefix + "/")


def get_plugin_config(plugin_name: str, cwd: str) -> dict[str, Any]:
    """Read plugin config with directory-specific overrides.

    Args:
        plugin_name: Plugin name (e.g., "mr-sparkle", "dmv")
        cwd: Current working directory from hook stdin JSON

    Returns:
        Dict of resolved config values. Returns empty dict if no config
        file exists or on any error. Callers should use .get(key, True)
        to default features to enabled.
    """
    config_file = CONFIG_DIR / f"{plugin_name}.toml"

    if not config_file.is_file():
        return {}

    try:
        with open(config_file, "rb") as f:
            data = tomllib.load(f)
    except Exception:
        return {}

    # Start with top-level config (excluding 'overrides' key)
    resolved = {k: v for k, v in data.items() if k != "overrides"}

    # Apply matching overrides in order (last match wins)
    for override in data.get("overrides", []):
        match_pattern = override.get("match", "")
        if match_pattern and _path_matches(cwd, match_pattern):
            for k, v in override.items():
                if k != "match":
                    resolved[k] = v

    return resolved
