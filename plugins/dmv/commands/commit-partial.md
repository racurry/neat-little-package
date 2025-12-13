---
description: Commit a subset of changes based on a description
argument-hint: <what_to_commit>
---

Use the git-committer agent to execute a partial commit workflow.

Based on the description in $ARGUMENTS, the agent will identify and stage only the relevant files, then commit them with an appropriate message following git-workflow conventions.

Examples of descriptions:

- "all files related to authentication"
- "only test files"
- "changes to the API layer"
- "documentation updates"
