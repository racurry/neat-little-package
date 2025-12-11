# DMV

![Some Days, We Don't Let The Line Move At All](assets/dmv.png)

## Overview

Doing git stuff in the way I prefer. Git commits, talking to Github.

## Commands

Setup

```
/dmv:setup     # Walks through `gh` and github mcp config
```

Committing

```
/dmv:commit                                          # commits everything with terse language
/dmv:commit refactor authentication flow             # commits everything with message 'refactor authentication flow'
/dmv:commit-partial just the stuff related to auth   # commits just the stuff related to auth with a terse message
```

Pull Requests

```
/dmv:pr                                              # creates PR with Problem/Solution format
/dmv:pr users seeing 500 errors on login             # creates PR using provided context for Problem statement
```
