---
description: Commit all changes and push to remote with git pub
argument-hint: [commit_message]
---

Use the git-committer agent to execute a full repository commit, then push with `git pub`.

If $ARGUMENTS is provided, use it as the commit message.

If $ARGUMENTS is NOT provided, the agent will analyze all changes and generate an appropriate commit message following git-workflow conventions.

After the commit succeeds, run `git pub` to push to the remote.
