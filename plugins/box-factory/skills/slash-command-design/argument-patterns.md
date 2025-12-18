# Argument Patterns

This document covers how to use arguments in slash commands.

## Official Specification

All arguments as single string:

```markdown
$ARGUMENTS
```

Example: `/fix-issue 123 high-priority` → `$ARGUMENTS = "123 high-priority"`

Individual positional arguments:

```markdown
$1, $2, $3, etc.
```

Example: `/review-pr 456 high alice` → `$1="456"`, `$2="high"`, `$3="alice"`

**Official guidance:** "Use individual arguments (`$1`, `$2`) for complex commands with multiple parameters"

## Best Practices

### When to Use $1, $2 vs $ARGUMENTS

**Use `$1, $2` when:**

- Need arguments in different parts of the prompt
- Want to provide defaults or conditional logic
- Arguments have distinct semantic meanings

**Use `$ARGUMENTS` when:**

- Passing all arguments directly to agent
- Single compound argument (like a description or message)
- Don't need to reference specific positions

### Keep Argument Parsing Simple

If you need validation or complex logic, delegate to an agent:

```markdown
---
description: Deploy to specified environment
argument-hint: environment
---

Deploy to $1 environment. The deployer agent will handle validation, rollback strategy, and confirmation.
```

**Agent handles:**

- Argument validation
- Type checking
- Complex parsing
- Error messages

### Anti-Pattern: Overly Complex Arguments

**Problem:** Arguments that need extensive parsing or validation

**Example of questionable pattern:**

```markdown
/deploy env=staging branch=main force=true rollback=false
```

**Why it's questionable:** No argument validation, no type checking, brittle parsing.

**Better approach:** Keep arguments simple, let agent handle complexity:

```markdown
---
description: Deploy to specified environment
argument-hint: environment
---

Deploy to $1 environment. The deployer agent will handle validation, rollback strategy, and confirmation.
```
