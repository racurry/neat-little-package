---
description: Commit all changes with smart message generation or provided message
argument-hint: [commit_message]
---

Use the git-committer agent to execute a full repository commit.

If $ARGUMENTS is provided, use it as the commit message.

If $ARGUMENTS is NOT provided, the agent will analyze all changes and generate an appropriate commit message following git-workflow conventions.
