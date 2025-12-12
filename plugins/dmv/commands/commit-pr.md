---
description: Commit all changes and open a pull request
argument-hint: [commit_message | problem context]
---

Use the git-committer agent to execute a full repository commit, then use the pr-opener agent to create a pull request.

If $ARGUMENTS is provided, use it as the commit message for the commit step, and as problem context for the PR.

If $ARGUMENTS is NOT provided:

- The git-committer agent will analyze all changes and generate an appropriate commit message
- The pr-opener agent will analyze branch commits and diff to infer the Problem and Solution

The PR will follow the Problem/Solution format with terse, concise language.
