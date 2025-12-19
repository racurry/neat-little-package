# Common Pitfalls (Best Practices)

Anti-patterns catalog for slash command design.

## Anti-Pattern Catalog

| Pitfall                   | Symptom                                             | Impact                                                                | Fix                                                                   |
| ------------------------- | --------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Knowledge Storage         | Command prompt > 20 lines of documentation          | Wastes tokens, wrong component type, poor discoverability             | Move to skill, keep command action-only                               |
| Scope Creep               | Single command tries to do multiple distinct things | Multiple failure modes, unclear purpose, hard to maintain             | Split into separate commands or use orchestrator agent                |
| User Interaction Language | "Ask user", "confirm with user" in prompt           | Commands can't interact mid-execution, breaks isolation model         | Remove interaction or rethink as interactive Main Claude conversation |
| Missing Tool Restrictions | Security-sensitive command with full tool access    | Accidental modifications, security risk                               | Add `allowed-tools` field with specific restrictions                  |
| Over-Restrictive Tools    | Command needs multiple tools but restricted to one  | Command fails or incomplete execution                                 | Remove tool restrictions or widen scope                               |
| Wrong Component Type      | Command contains substantial guidance or knowledge  | Should be skill; command is for actions not documentation             | Convert to skill, create action-only command if needed                |
| Vague Description         | Generic or missing description field                | Poor discoverability, Claude won't use SlashCommand tool autonomously | Always include specific, action-oriented description                  |
| Unnecessary Delegation    | Delegates to agent when command could handle it     | Extra complexity, no benefit from isolation                           | Handle directly unless you need context isolation or reusability      |

## Detailed Examples

### Pitfall #1: Knowledge Storage in Commands

**Symptom:** Command prompt contains extensive documentation (>20 lines) instead of triggering action.

**Example of wrong pattern:**

```markdown
---
description: Show API documentation standards
---

Our API documentation standards:
- Use OpenAPI 3.0 specification
- Include examples for all endpoints
- Document error codes comprehensively
- [40+ more lines of guidelines...]
```

**Impact:** Wastes tokens, wrong component type, poor progressive disclosure, should be skill not command.

**Fix:** Create a skill for standards, command for action:

```markdown
---
description: Generate API documentation for current file
---

Use the api-documentation skill to generate comprehensive API docs for the current file.
```

______________________________________________________________________

### Pitfall #2: Unnecessary Delegation

**Symptom:** Command delegates to agent when it could handle the task directly.

**Example of over-delegation:**

```markdown
---
description: Show git status
---

Use the git-status agent to display the current git status.
```

**Impact:** Adds complexity without benefit. No context isolation needed, no reusability gain, task is straightforward.

**Fix:** Handle directly:

```markdown
---
description: Show git status
allowed-tools: Bash(git:*)
---

!git status

Summarize the current state of the working directory.
```

**When delegation IS appropriate:**

- **Context isolation** — Test output, logs, or large file contents shouldn't clutter main conversation
- **Parallelization** — Multiple independent tasks to run simultaneously
- **Reusable workflows** — Same logic invoked from multiple commands or contexts

**When to handle directly:**

- Output is reasonably sized and useful in conversation
- Straightforward task even if multi-step
- No need for the workflow elsewhere

______________________________________________________________________

### Pitfall #3: Scope Creep

**Symptom:** Single command tries to do multiple distinct operations.

**Example of wrong pattern:**

```markdown
---
description: Test, lint, format, commit, and deploy
---

Run tests, fix any linting issues, format code, commit changes, and deploy to staging.
```

**Impact:** Multiple failure modes, unclear purpose, complex error handling, hard to maintain, violates single-responsibility principle.

**Fix Option 1 - Separate commands:**

```markdown
/test      → Run test suite
/lint      → Lint and fix
/commit    → Commit changes
/deploy    → Deploy to staging
```

**Fix Option 2 - Orchestrator agent:**

```markdown
---
description: Run complete CI workflow (test, lint, format, commit)
---

Use the ci-orchestrator agent to run the complete CI workflow with proper error handling and rollback.
```

______________________________________________________________________

### Pitfall #4: Overly Complex Argument Syntax

**Symptom:** Command uses key=value parsing or complex argument structures.

**Example of questionable pattern:**

```markdown
/deploy env=staging branch=main force=true rollback=false
```

**Impact:** Brittle parsing, error-prone, hard for users to remember syntax.

**Fix:** Use simple positional arguments:

```markdown
---
description: Deploy to specified environment
argument-hint: environment [branch]
---

Deploy to $1 environment using branch $2 (defaults to main). Validate the environment, check prerequisites, and proceed with appropriate rollback strategy.
```

Claude handles the interpretation and validation as part of processing the prompt—no special parsing needed.

______________________________________________________________________

### Pitfall #5: User Interaction Language

**Symptom:** Command prompt contains "ask the user", "confirm with user", "wait for response".

**Example of wrong pattern:**

```markdown
---
description: Deploy to production
---

Ask the user to confirm production deployment.
If confirmed, run deployment script.
Show results and ask if rollback is needed.
```

**Impact:** Commands can't interact mid-execution, breaks isolation model, impossible to implement.

**Fix Option 1 - Remove interaction (assume confirmation via command invocation):**

```markdown
---
description: Deploy to production (confirmation required)
---

!echo "Deploying to production..."
!./deploy.sh production

Deployment complete. Monitor logs at https://logs.example.com
```

**Fix Option 2 - Rethink as Main Claude conversation:**

Don't use a command. User asks "deploy to production", Main Claude confirms details, then either runs deployment directly or delegates to agent.

______________________________________________________________________

## Quick Reference: Symptoms and Fixes

| Symptom                                   | Likely Issue               | Fix                                       |
| ----------------------------------------- | -------------------------- | ----------------------------------------- |
| Documentation blocks in prompt            | Knowledge storage          | Move to skill, keep command action-only   |
| "Ask user", "confirm with user" in prompt | Misunderstanding isolation | Remove interaction or rethink design      |
| Security-sensitive op with full tools     | Missing tool restrictions  | Add `allowed-tools` field                 |
| Command fails due to tool restrictions    | Over-restrictive tools     | Widen scope or remove restrictions        |
| Vague or missing description              | Poor discoverability       | Add specific, action-oriented description |
| Substantial guidance in command           | Wrong component type       | Convert to skill, create action command   |
| Delegates simple task to agent            | Unnecessary delegation     | Handle directly in command                |
| Command does many unrelated things        | Scope creep                | Split into separate focused commands      |
