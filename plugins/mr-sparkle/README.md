# Mr. Sparkle

![Mr. Sparkle](./assets/mr-sparkle.png)

All the things about how to do code.

## Overview

- Auto-lints files after every Write/Edit (hook)
- Detects file type and runs appropriate tools automatically
- Prefers modern unified tools (ruff, biome) over traditional chains
- Terse commits and Problem/Solution PRs via `gh`, no type prefixes or attribution
- Warns when a commit message breaks those conventions (hook)
- Blocks dangerous Bash patterns as a safety net for broad permissions

## Skills

Linting

```
/mr-sparkle:lint <file>                              # lint a specific file
/mr-sparkle:lint config                              # show per-project settings
/mr-sparkle:lint config init                         # generate config from autodetection
/mr-sparkle:lint config set tools none               # disable auto-linting
/mr-sparkle:lint config set validate_commit_message false   # disable commit-message checks here
```

Git & GitHub

```
/mr-sparkle:github                                   # set up gh cli
/mr-sparkle:commit                                   # commits everything with terse message
/mr-sparkle:commit just the auth stuff               # commits only files matching description
/mr-sparkle:pr                                        # creates PR with Problem/Solution format
/mr-sparkle:pr users seeing 500 errors on login      # creates PR using provided context
```

Also: `merge-conflicts` and `code-history` skills activate automatically when relevant.

## Supported Languages

| Language              | Tools                      |
| --------------------- | -------------------------- |
| Python                | ruff, pylint, isort, black |
| JavaScript/TypeScript | biome, eslint, prettier    |
| Markdown              | markdownlint-cli2          |
| Shell                 | shfmt, shellcheck          |
| Ruby                  | standardrb, rubocop        |
| YAML/JSON             | prettier                   |
