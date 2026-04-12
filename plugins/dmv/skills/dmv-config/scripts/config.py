#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["pyyaml"]
# ///
"""Manage dmv per-project hook settings in .claude/dmv.config.local.yml."""

import sys
from pathlib import Path

import yaml

DEFAULTS = {
    "validate_commit_message": True,
}

config_path = Path(".claude/dmv.config.local.yml")


def load():
    if config_path.exists():
        return yaml.safe_load(config_path.read_text()) or {}
    return {}


def save(config):
    config_path.parent.mkdir(exist_ok=True)
    config_path.write_text(yaml.dump(config, default_flow_style=False))


def resolved(config):
    return {k: config.get(k, v) for k, v in DEFAULTS.items()}


def show():
    config = load()
    r = resolved(config)
    source = "defaults" if not config_path.exists() else str(config_path)
    lines = [f"dmv config ({source}):"]
    for k, v in r.items():
        marker = "" if k not in config else " (overridden)"
        lines.append(f"  {k}: {str(v).lower()}{marker}")
    print("\n".join(lines))


def coerce(value_str, default):
    """Coerce a string value to match the type of the default."""
    if isinstance(default, bool):
        return value_str.lower() in ("true", "yes", "1")
    return value_str


def set_key(key, value_str):
    if key not in DEFAULTS:
        print(f"unknown key: {key}")
        print(f"keys: {', '.join(DEFAULTS.keys())}")
        sys.exit(1)
    config = load()
    config[key] = coerce(value_str, DEFAULTS[key])
    save(config)
    print(f"dmv config: {key} = {config[key]}")


args = sys.argv[1:]

if not args or args[0] == "show":
    show()
elif args[0] == "set" and len(args) > 2:
    set_key(args[1], args[2])
elif len(args) == 2 and args[0] in DEFAULTS:
    set_key(args[0], args[1])
else:
    print("usage: dmv-config show | set <key> <value>")
    print(f"keys: {', '.join(DEFAULTS.keys())}")
