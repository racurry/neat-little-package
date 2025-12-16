# Common Gotchas and Antipatterns

Reference file for sub-agent-design skill. Read when you need to avoid common mistakes in sub-agent creation.

## Common Gotchas

### Gotcha #1: User Interaction Language

**Problem:** Sub-agent prompts assume they can ask questions or confirm actions

**Forbidden phrases anywhere in sub-agent prompt:**

- "ask the user", "gather from user", "clarify with user"
- "request from user", "prompt the user", "wait for input"
- "check with user", "verify with user", "confirm with user"

**Replace with:**

- "infer from context", "use provided parameters"
- "make reasonable assumptions", "use available information"
- "default to [specific behavior]"

### Gotcha #2: Hardcoding Version-Specific Info

**Problem:** Docs change; hardcoded details become outdated

**Instead of:**

```markdown
Available models: sonnet, opus, haiku
Use these tools: Read, Write, Edit, Bash
```

**Do this:**

```markdown
See model-config documentation for current options
Refer to tools documentation for current capabilities
```

### Gotcha #3: Tool Mismatches

**Problem:** Tools don't match the sub-agent's autonomous responsibilities

**Examples:**

- Code generator with only Read (can't write generated code)
- Test runner without Bash (can't run tests)
- Code reviewer with Write/Edit (should be read-only)

**Solution:** Grant minimal necessary permissions for the sub-agent's actual work

## Common Antipatterns

### Antipattern: Overly Broad Scope

**What you'll see:** "Full-stack engineer sub-agent that handles everything"

**Why it fails:**

- Unclear when to delegate
- Context pollution
- Violates single responsibility principle

**Solution:** Split into focused sub-agents (frontend-dev, backend-dev, db-specialist)

### Antipattern: Vague Delegation Triggers

**What you'll see:** Great functionality, vague description

**Why it fails:** Sub-agent only fires on explicit request, not autonomously

**Solution:** Make description specific about triggering conditions and use cases

### Antipattern: Interactive Assumptions

**What you'll see:** "Ask user for target directory", "Confirm with user before proceeding"

**Why it fails:** Sub-agents can't interact with users

**Solution:** "Use provided directory parameter or default to ./src", "Proceed based on available context"

### Antipattern: Knowledge Duplication

**What you'll see:** Sub-agent loads a skill but also embeds the same knowledge inline

**Why it fails:**

- Maintenance burden (update two places)
- Context waste (duplicate content loaded)
- Potential conflicts (sub-agent and skill disagree)

**Solution:** If sub-agent loads a skill, defer knowledge to the skill. Sub-agent focuses on process.

### Gotcha #4: Proceeding Without Required Skills

**Problem:** Sub-agent declares skill dependency via `skills` field, but proceeds anyway when the skill fails to load

**Why it matters:** If a sub-agent has a hard dependency on a skill (declared in `skills` field), that skill contains the domain knowledge the sub-agent needs. Without it, the sub-agent will likely produce incorrect or low-quality output.

**What you'll see:**

- Sub-agent attempts task without loaded guidance
- Output doesn't follow expected patterns
- Validation failures or subtle quality issues

**Solution:** Sub-agents with hard skill dependencies should fail fast:

```markdown
## Process

1. **Verify skill loaded** - If skill-design guidance is not available, report failure and stop
2. **Proceed with task** using skill guidance
```

**Error handling pattern:**

```markdown
## Error Handling

| Situation | Action |
| --- | --- |
| Required skill fails to load | Report failure immediately, do not attempt task |
| Optional skill fails to load | Note limitation, proceed with degraded capability |
```

**Key distinction:**

- `skills` field dependency = hard requirement → fail if missing
- Conditional skill loading in body = soft requirement → may proceed with limitations
