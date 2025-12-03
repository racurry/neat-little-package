---
name: box-factory-agent-design
description: Interpretive guidance for designing Claude Code agents. Helps apply official documentation effectively and avoid common pitfalls. Use when creating or reviewing agents.
---

# Agent Design Skill

This skill provides interpretive guidance for creating Claude Code agents. It helps you understand what the docs mean and how to create excellent agents.

## Official Documentation

Fetch these docs when you need to verify syntax or check current options:

- **<https://code.claude.com/docs/en/sub-agents.md>** - Core specification and examples
- **<https://code.claude.com/docs/en/settings#tools-available-to-claude>** - Verify tool names
- **<https://code.claude.com/docs/en/model-config.md>** - Current model options

## Critical Architecture Understanding

Agents operate in **isolated context** with a **return-based model**:

```
User ↔ Main Claude → Agent (isolated, returns results)
```

**Critical implications:**

- Agents CAN'T ask users questions
- Agents CAN'T interact with users directly
- Agents SHOULD do actual work (run code, write files, analyze code) when appropriate
- Main agent handles ALL user communication

**The key distinction:** No user interaction (no asking questions, no confirming), but full ability to do autonomous work within scope.

**Common misconception:** If your agent prompt includes phrases like "ask the user", "gather from user", "clarify with user" - you've misunderstood the architecture.

## Decision Framework

### Agent vs Command vs Skill

**Use Agent when:**

- Need isolated context (won't pollute main conversation)
- Want autonomous delegation (triggered by context)
- Require specific tool restrictions
- Task runs as part of larger workflows

**Use Command when:**

- User explicitly triggers it
- Simple, straightforward task
- No need for context isolation

**Use Skill when:**

- Knowledge needed by multiple contexts
- Procedural expertise that's substantial
- Progressive disclosure would save tokens

### Tool Selection Philosophy

**Match tools to autonomous responsibilities:**

- If agent's job is to write files → include Write/Edit
- If agent only analyzes → Read, Grep, Glob only
- Never include AskUserQuestion (agents can't use it)

**Common mistake:** Over-restricting tools because you're thinking "safety"

**Reality:** An agent whose job is generating code but only has Read tool can't do its job

**Balance:** Reviewers should be read-only; builders need write access

## Description Field Design

The `description` field determines when Claude delegates to your agent. This is critical for autonomous invocation.

**Official requirement:** "Natural language explanation of when to invoke the subagent"

**Quality test:** Would Claude invoke this agent based on context alone, or only when explicitly asked?

**Guidelines:**

- State WHEN to use (triggering conditions), not just WHAT it does
- Be specific about context and use cases
- Test empirically - if your agent isn't being invoked automatically, revise the description
- Avoid overly generic descriptions that match too many scenarios

## Common Gotchas

### Gotcha #1: User Interaction Language

**Problem:** Agent prompts assume they can ask questions or confirm actions

**Forbidden phrases anywhere in agent prompt:**

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

**Problem:** Tools don't match the agent's autonomous responsibilities

**Examples:**

- ❌ Code generator with only Read (can't write generated code)
- ❌ Test runner without Bash (can't run tests)
- ❌ Code reviewer with Write/Edit (should be read-only)

**Solution:** Grant minimal necessary permissions for the agent's actual work

## Common Antipatterns

### Antipattern: Overly Broad Scope

**What you'll see:** "Full-stack engineer agent that handles everything"

**Why it fails:**

- Unclear when to delegate
- Context pollution
- Violates single responsibility principle

**Solution:** Split into focused agents (frontend-dev, backend-dev, db-specialist)

### Antipattern: Vague Delegation Triggers

**What you'll see:** Great functionality, vague description

**Why it fails:** Agent only fires on explicit request, not autonomously

**Solution:** Make description specific about triggering conditions and use cases

### Antipattern: Interactive Assumptions

**What you'll see:** "Ask user for target directory", "Confirm with user before proceeding"

**Why it fails:** Agents can't interact with users

**Solution:** "Use provided directory parameter or default to ./src", "Proceed based on available context"

## System Prompt Best Practices

### Structure

Use consistent markdown hierarchy:

```markdown
# Agent Name (H1 - single heading)

## Purpose
[Clear statement of role]

## Process
1. Step one
2. Step two

## Guidelines
- Key principle one
- Key principle two

## Constraints
- What NOT to do
- Boundaries and limitations
```

### Content Quality

**Be specific and actionable:**

- ✅ "Run pytest -v and parse output for failures"
- ❌ "Run tests and check for problems"

**Define scope clearly:**

- ✅ "Only analyze Python files in src/ directory"
- ❌ "Analyze code"

**Include constraints:**

- ✅ "Never modify production configuration files"
- ✅ "Only analyze; never modify code"

## Validation Workflow

Before finalizing an agent:

1. **Fetch official docs** - Verify against current specification
2. **Check structure** - Valid YAML frontmatter, required fields present
3. **Scan for forbidden language** - No user interaction phrases
4. **Validate tools** - Match autonomous responsibilities, no AskUserQuestion
5. **Test description** - Specific triggering conditions, not generic
6. **Review system prompt** - Single H1, clear structure, actionable instructions
7. **Verify no hardcoding** - No version-specific details that will become outdated

## Path Resolution

When writing agents:

1. If caller specifies path → use exact path
2. If working in `.claude/agents/` → use that
3. Default → `.claude/agents/` (project-level)
4. User-level (`~/.claude/agents/`) → only when explicitly requested

## Documentation References

Authoritative sources for agent specifications:

**Core specifications:**

- <https://code.claude.com/docs/en/sub-agents.md> - Agent structure, examples, patterns

**Tool verification:**

- <https://code.claude.com/docs/en/settings#tools-available-to-claude> - Current tool list

**Model selection:**

- <https://code.claude.com/docs/en/model-config.md> - Available models, selection guidance

**Workflow patterns:**

- <https://code.claude.com/docs/en/common-workflows.md> - Real-world delegation patterns

**Remember:** This skill helps you interpret and apply those docs effectively. Always fetch current documentation for specifications and details.
