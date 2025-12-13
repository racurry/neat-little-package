# Mr. Sparkle

![Mr. Sparkle](./assets/mr-sparkle.png)

Lints your code on write.

## Overview

- Auto-lints files when you save them (hook)
- Tells Claude how to use linting tools for each language

## Supported Languages

| Language              | Tools                      |
| --------------------- | -------------------------- |
| Markdown              | markdownlint-cli2          |
| Python                | ruff, pylint, isort, black |
| JavaScript/TypeScript | biome, eslint, prettier    |
| Shell                 | shfmt, shellcheck          |
| Ruby                  | standardrb, rubocop        |
| YAML                  | prettier                   |
| JSON/JSON5/JSONC      | prettier                   |

## Commands

```
/mr-sparkle:lint <file>    # lint a specific file
```
