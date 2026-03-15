# DMV

![Some Days, We Don't Let The Line Move At All](assets/dmv.png)

Doing git stuff in the way I prefer.

## Overview

- Terse commits with no type prefixes, no emojis, no attribution
- PRs in Problem/Solution format, ignoring repo templates
- Prefers gh CLI over GitHub MCP server
- Auto-retries pre-commit hook formatting failures once

## Skills

Setup

```
/dmv:github                                          # set up gh cli and github mcp
/dmv:config                                          # show per-project hook settings
/dmv:config disable validate_commit_message          # disable a hook for this directory
```

Committing

```
/dmv:commit                                          # commits everything with terse message
/dmv:commit refactor authentication flow             # commits with provided message
/dmv:commit just the auth stuff                      # commits only files matching description
```

Pull Requests

```
/dmv:pr                                              # creates PR with Problem/Solution format
/dmv:pr users seeing 500 errors on login             # creates PR using provided context
```
