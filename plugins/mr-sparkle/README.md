# Mr. Sparkle

![Mr. Sparkle](./assets/mr-sparkle.png)

Lints your code on write.

## Overview

- Auto-lints files after every Write/Edit (hook)
- Detects file type and runs appropriate tools automatically
- Prefers modern unified tools (ruff, biome) over traditional chains
- Blocks dangerous Bash patterns as a safety net for broad permissions

## Skills

```
/mr-sparkle:lint <file>                              # lint a specific file
/mr-sparkle:config                                   # show per-project hook settings
/mr-sparkle:config disable lint_on_write             # disable auto-linting for this project
```

## Supported Languages

| Language              | Tools                      |
| --------------------- | -------------------------- |
| Python                | ruff, pylint, isort, black |
| JavaScript/TypeScript | biome, eslint, prettier    |
| Markdown              | markdownlint-cli2          |
| Shell                 | shfmt, shellcheck          |
| Ruby                  | standardrb, rubocop        |
| YAML/JSON             | prettier                   |
