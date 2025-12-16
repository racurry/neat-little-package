# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is **neat-little-package**, a Claude Code plugin marketplace containing 5 specialized plugins:

- **box-factory**: Meta-plugin for creating Claude Code components (plugins, agents, commands, skills, hooks)
- **dmv**: Git and GitHub workflow automation with user-specific preferences
- **mr-sparkle**: Code quality enforcement (linting, formatting)
- **spirograph**: 3D-printed home organization (Gridfinity, OpenGrid, etc.)
- **ultrahouse3000**: Home Assistant smart home integration

## Design Intent

Personal toolkit encoding one user's specific preferences. Narrow, opinionated choices are features, not bugs. Never suggest generalizing for hypothetical other users or adding configurability for flexibility's sake.

## Plugin Structure

Each plugin follows this structure:

```text
plugins/<name>/
├── .claude-plugin/plugin.json  # Plugin metadata
├── agents/                     # Autonomous workers (.md files)
├── commands/                   # Slash commands (.md files)
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md            # Main skill guidance
│       └── scripts/            # Optional executable scripts
├── hooks/
│   ├── hooks.json              # Hook configuration
│   └── *.py, *.sh              # Hook implementations
├── CLAUDE.md                   # Developer guidelines
└── README.md                   # User documentation
```

## Script Conventions

All Python scripts use UV inline metadata (PEP 723):

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
```

## Testing

Run tests with uv and pytest:

```bash
uv run --with pytest pytest ./path/to/tests/
```

## Documentation Philosophy

**Low-Maintenance First**: Defer to official docs via WebFetch rather than hardcoding version-specific details. Documentation changes; principles don't.

**Knowledge Delta Filter**: Only document what Claude doesn't already know - user-specific preferences, edge cases, things Claude gets wrong. Skip standard commands and common workflows.

**Two-Layer Approach**: Distinguish official specs (what docs say) from best practices (interpretive guidance). Mark which layer you're in.

**Component Independence**: When referencing content in another component (especially another skill), use indirect references ("the X skill's guidance on Y") rather than direct file paths. Internal structure is an implementation detail; a component's name and purpose are its public interface.

## Plugin-Specific Guidelines

Each plugin has its own CLAUDE.md with detailed conventions. Refer to the plugin-specific file when working within that plugin.
