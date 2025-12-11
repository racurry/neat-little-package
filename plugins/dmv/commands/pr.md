---
description: Create a pull request with Problem/Solution format
argument-hint: [optional context about the problem being solved]
---

Use the pr-opener agent to create a pull request for the current branch.

If $ARGUMENTS is provided, use it as context for the Problem statement. This could be:

- A description of the bug or issue being fixed
- A link to relevant logs or documentation
- Error output or symptoms that motivated the change
- A feature request or requirement being addressed

If $ARGUMENTS is NOT provided, the agent will analyze the branch commits and diff to infer the Problem and Solution.

The PR will follow the Problem/Solution format with terse, concise language.
