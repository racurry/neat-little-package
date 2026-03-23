---
name: lint
description: Universal polyglot linting and per-project config management. Use when you need to lint files, understand tool selection logic, invoke linting from commands/agents, or manage mr-sparkle config.
---

# Linting Skill

This skill provides universal polyglot linting through a CLI script that detects file types, finds project configuration, and runs appropriate linters.

## Supported Languages and Tools

| Language              | Tool Groups (priority order)       | Config Detection                                  |
| --------------------- | ---------------------------------- | ------------------------------------------------- |
| Python                | `ruff` OR `pylint`+`isort`+`black` | pyproject.toml, ruff.toml, setup.cfg              |
| JavaScript/TypeScript | `biome` OR `eslint`+`prettier`     | biome.json, eslint.config.\*, package.json        |
| Markdown              | `markdownlint-cli2`                | .markdownlint-cli2.\*, ~/.markdownlint-cli2.jsonc |
| Shell                 | `shfmt`+`shellcheck`               | .editorconfig, .shellcheckrc                      |
| Ruby                  | `standard` OR `rubocop`            | .standard.yml, .rubocop.yml, Gemfile              |
| YAML                  | `prettier`                         | .prettierrc\*, ~/.prettierrc.json5                |
| JSON/JSON5/JSONC      | `prettier`                         | .prettierrc\*, ~/.prettierrc.json5                |

## Tool Selection Logic

The script uses **group-based priority selection**:

1. Tools are organized into groups (e.g., `[ruff]` vs `[pylint, isort, black]`)
2. First group with any project-level configuration wins
3. All tools in the winning group run (in order)
4. If no config found, falls back to first group's tools

**Example for Python:**

- If `pyproject.toml` has `[tool.ruff]` → runs `ruff check --fix` then `ruff format`
- If `setup.cfg` has `[isort]` section → runs `pylint`, `isort`, `black`
- If no config → runs `ruff` (first group default)

## CLI Script Usage

The universal linting script is at `scripts/lint.py`.

### Basic Usage

```bash
# Lint a file (auto-detects type, applies fixes)
${CLAUDE_SKILL_DIR}/scripts/lint.py /path/to/file.py

# JSON output for programmatic use
${CLAUDE_SKILL_DIR}/scripts/lint.py /path/to/file.py --format json

# Text output (default, human-readable)
${CLAUDE_SKILL_DIR}/scripts/lint.py /path/to/file.py --format text
```

### Output Formats

**`--format text`** (default):

```text
✓ ruff file.py: OK
```

or

```text
⚠ ruff file.py: Lint errors!
<detailed output>
```

**`--format json`**:

```json
{
  "file": "/path/to/file.py",
  "toolset": "python",
  "tools_run": ["ruff"],
  "status": "ok",
  "results": [
    {"tool": "ruff", "status": "ok", "output": ""}
  ]
}
```

### Exit Codes

- `0`: Success (file clean or fixed)
- `1`: Lint errors found (non-blocking)
- `2`: Tool execution error

## Project Root Detection

The script finds project root by walking up from the file looking for:

1. `package.json`
2. `pyproject.toml`
3. `Gemfile`
4. `.git` directory

Config detection happens relative to project root.

## Config Detection Details

### Python Tools

| Tool   | Config Files              | pyproject.toml  | INI Files            |
| ------ | ------------------------- | --------------- | -------------------- |
| ruff   | `ruff.toml`, `.ruff.toml` | `[tool.ruff]`   | -                    |
| black  | -                         | `[tool.black]`  | -                    |
| isort  | `.isort.cfg`              | `[tool.isort]`  | `setup.cfg [isort]`  |
| pylint | `.pylintrc`, `pylintrc`   | `[tool.pylint]` | `setup.cfg [pylint]` |

### JavaScript/TypeScript Tools

| Tool     | Config Files                        | package.json             |
| -------- | ----------------------------------- | ------------------------ |
| biome    | `biome.json`, `biome.jsonc`         | `@biomejs/biome` in deps |
| eslint   | `eslint.config.*`, `.eslintrc.*`    | `eslint` in deps         |
| prettier | `.prettierrc*`, `prettier.config.*` | `prettier` in deps       |

### Markdown Tools

| Tool              | Config Files           | Global Fallback              |
| ----------------- | ---------------------- | ---------------------------- |
| markdownlint-cli2 | `.markdownlint-cli2.*` | `~/.markdownlint-cli2.jsonc` |

If no config found, uses `defaults/default-markdownlint.jsonc`.

### Shell Tools

| Tool       | Config Files    |
| ---------- | --------------- |
| shfmt      | `.editorconfig` |
| shellcheck | `.shellcheckrc` |

### Ruby Tools

| Tool     | Config Files                        | Gemfile                                |
| -------- | ----------------------------------- | -------------------------------------- |
| standard | `.standard.yml`                     | `gem "standard"` or `gem "standardrb"` |
| rubocop  | `.rubocop.yml`, `.rubocop_todo.yml` | `gem "rubocop"`                        |

**Tool selection:**

- Standard (zero-config, opinionated) runs `standardrb --fix`
- RuboCop (configurable) runs `rubocop -a` (safe auto-correct only)

### YAML/JSON Tools

| Tool     | Config Files                        | Global Fallback       |
| -------- | ----------------------------------- | --------------------- |
| prettier | `.prettierrc*`, `prettier.config.*` | `~/.prettierrc.json5` |

If no config found, uses `defaults/default-prettier.json5`.

**Supported extensions:**

- YAML: `.yaml`, `.yml`
- JSON: `.json`, `.json5`, `.jsonc`

## Integration Patterns

### From Commands

```markdown
Run the linting script:
`${CLAUDE_SKILL_DIR}/scripts/lint.py <file_path>`
```

### From Agents

```markdown
For linting results, run:
`${CLAUDE_SKILL_DIR}/scripts/lint.py <file> --format json`

Parse the JSON output to understand lint status.
```

### From Hooks

The script supports `--stdin-hook` mode for hook integration:

```bash
# Reads hook JSON from stdin, outputs hook-compatible JSON
echo '{"tool_input":{"file_path":"/path/to/file.py"}}' | ${CLAUDE_SKILL_DIR}/scripts/lint.py --stdin-hook
```

Output visibility (systemMessage vs additionalContext) is controlled by the `output` section in `.claude/mr-sparkle.config.yml`.

## Per-Project Config

All mr-sparkle settings live in `.claude/mr-sparkle.config.yml` in the project root.

```yaml
# Use autodetection (default behavior when no config file exists)
lint_on_write:
  tools:
    - default
  output:
    user: true
    claude: false
```

```yaml
# Explicit tools per extension — bypasses autodetection entirely
lint_on_write:
  tools:
    - file_ext: [.py]
      commands:
        - ruff check --fix
        - ruff format
    - file_ext: [.js, .ts, .tsx]
      commands:
        - eslint --fix
  output:
    user: false
    claude: true
```

```yaml
# Disable linting entirely
lint_on_write:
  tools: []
```

```yaml
# Disable direct invocation blocking (markdownlint without --config, etc.)
block_direct: []
```

**Key behaviors:**

- No config file = autodetection (same as `tools: [default]`)
- `tools: [default]` is all-or-nothing — cannot mix with explicit entries
- Explicit tools: file path appended as last arg, run from project root
- Extensions not covered by any entry are silently skipped
- `output.user` controls the systemMessage (shown to user)
- `output.claude` controls additionalContext (fed to Claude)

### Config Management

**If invoked as `config` or `config show`:** Read `.claude/mr-sparkle.config.yml` and display resolved settings.

**If `config init`:** Run `--detect` on representative files to generate `.claude/mr-sparkle.config.yml` with explicit tool commands based on what autodetection found.

**If `config set`:** Update a config value. Examples:

- `config set output.user false`
- `config set output.claude true`
- `config set tools default`
- `config set tools none`

When creating or modifying the config file:

- Create `.claude/` directory if it doesn't exist
- Add `.claude/*.config.yml` to `.gitignore` if not already there
- Always show resolved state after any change

### Detection Mode

```bash
${CLAUDE_SKILL_DIR}/scripts/lint.py --detect /path/to/file.py
```

Shows what autodetection finds: project root, toolset, selected tools, installed binaries, and config status. Useful for debugging why the wrong tools are running.

## Silent Skip Conditions

The script silently exits (code 0, no output) when:

- File doesn't exist
- File extension not recognized
- No tools installed for the detected toolset
- Tool requires config but none found (e.g., markdownlint without config)
- Config has `tools: []` (linting disabled)
- Custom config doesn't cover the file's extension
