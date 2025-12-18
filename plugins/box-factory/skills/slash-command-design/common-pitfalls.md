# Common Pitfalls (Best Practices)

Anti-patterns catalog for slash command design.

## Pitfall #1: Knowledge Storage in Commands

**Problem:** Using commands to store documentation instead of actions

**Example of wrong pattern:**

```markdown
---
description: Show API documentation standards
---

Our API documentation standards:
[50 lines of guidelines...]
```

**Why it's wrong:** This is knowledge, not an action. Commands should DO things.

**Better approach:** Create a skill for standards, command for action:

```markdown
---
description: Generate API documentation for current file
---

Use the api-documentation skill to generate comprehensive API docs for the current file.
```

## Pitfall #2: Reimplementing Agent Logic

**Problem:** Commands with complex logic that agents handle better

**Example of wrong pattern:**

```markdown
---
description: Run tests
---

First, scan for test files in src/, tests/, and __tests__.
Then determine the test framework by checking package.json.
If Jest, run `npm test`. If pytest, run `pytest -v`.
Parse the output for failures and categorize by severity...
```

**Why it's wrong:** Too much logic, too many decisions, better in isolated context.

**Better approach:**

```markdown
---
description: Run full test suite
---

Use the test-runner agent to execute the full test suite and analyze failures.
```

**Delegate to an agent when you need:**

- File reading/parsing (requires Read, Grep, or complex text processing)
- Complex decision trees (framework detection, config file parsing, multi-path logic)
- Error recovery logic (retries, fallbacks, multiple failure modes)
- State management (tracking across multiple steps, rollback capability)
- Multiple tool orchestration (coordinating Read + Grep + Write + Bash)

## Pitfall #3: Scope Creep

**Problem:** Single command tries to do too much

**Example:**

```markdown
description: Test, lint, format, commit, and deploy
```

**Why it fails:** Multiple distinct operations with different failure modes.

**Better:** Separate commands or orchestrator agent that coordinates multiple specialized agents.

## Symptoms and Fixes

| Symptom                                   | Likely Issue               | Fix                                      |
| ----------------------------------------- | -------------------------- | ---------------------------------------- |
| Command prompt > 30 lines                 | Too much logic             | Delegate to agent                        |
| Multiple Read/Grep calls needed           | Wrong component type       | Use agent instead                        |
| Complex argument parsing                  | Over-engineering           | Simplify args, let agent handle          |
| Documentation blocks in prompt            | Knowledge storage          | Move to skill, keep command action-only  |
| Conditional logic based on file contents  | Needs isolated context     | Delegate to agent                        |
| "Ask user", "confirm with user" in prompt | Misunderstanding isolation | Commands can't interact - rethink design |
