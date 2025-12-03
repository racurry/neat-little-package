---
description: Lint a file using appropriate tools based on file type
argument-hint: <file_path>
allowed-tools: Bash(*/lint.py:*)
---

Lint a file using the universal linting script.

## Usage

- `/mr-sparkle:lint src/app.py` - Lint a Python file
- `/mr-sparkle:lint README.md` - Lint a markdown file

## Implementation

Run: `${MR_SPARKLE_ROOT}/skills/linting/scripts/lint.py <file_path>`
Note that you MUST replace the env var with the value you were told earlier.

Output shows colored status: `✓ tool file: OK` or `⚠ tool file: Lint errors!`
