---
name: agent-design
description: Interpretive guidance for designing Claude Code agents. Helps apply official documentation effectively and avoid common pitfalls. Use when creating or reviewing agents.
---

# Agent Design

This skill provides interpretive guidance for creating Claude Code agents. It helps you understand what the docs mean and how to create excellent agents.

## Workflow Selection

| If you need to...                | Go to...                                                                    |
| -------------------------------- | --------------------------------------------------------------------------- |
| Understand agent isolation model | [Critical Architecture Understanding](#critical-architecture-understanding) |
| Decide agent vs command vs skill | [Decision Framework](#decision-framework)                                   |
| Pick tools for an agent          | [Tool Selection Philosophy](#tool-selection-philosophy)                     |
| Write the description field      | [Description Field Design](#description-field-design)                       |
| Avoid common mistakes            | [Common Gotchas](#common-gotchas)                                           |
| Check color for status line      | [Color Selection](#color-selection)                                         |
| Validate before completing       | [Quality Checklist](#quality-checklist)                                     |

## Quick Start

Create an agent at `.claude/agents/my-agent.md`:

```yaml
---
name: my-agent
description: Does X when Y. ALWAYS use when Z.
tools: Read, Grep, Glob
color: green
---
```

```markdown
# My Agent

You are a specialized agent that [purpose].

## Process

1. [Step one]
2. [Step two]

## Constraints

- Never include "ask the user" phrases (agents can't interact with users)
```

**Critical:** Agents operate in isolated context and return results. They cannot ask users questions.

## Official Documentation

**Claude Code changes rapidly and is post-training knowledge.** Fetch these docs when creating agents to ensure current syntax:

- **<https://code.claude.com/docs/en/sub-agents.md>** - Core specification and examples
- **<https://code.claude.com/docs/en/settings#tools-available-to-claude>** - Verify tool names
- **<https://code.claude.com/docs/en/model-config.md>** - Current model options

## Critical Architecture Understanding

Agents operate in **isolated context** with a **return-based model**:

```text
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

## Color Selection

The optional `color` field sets visual distinction for agents in the status line.

**Supported colors (7 total):** `red`, `green`, `blue`, `yellow`, `cyan`, `purple`, `orange`

**Not supported:** `magenta`, `white`, `black`, `gray`, `grey`, `*Bright` variants

**Semantic mapping:**

| Color    | Category   | Use For                                           |
| -------- | ---------- | ------------------------------------------------- |
| `blue`   | Creators   | Agents that create/write files, components, code  |
| `green`  | Quality    | Validators, reviewers, checkers, analyzers        |
| `yellow` | Operations | Git, deployment, CI/CD, system tasks              |
| `purple` | Meta       | Agents that create other agents                   |
| `cyan`   | Research   | Exploration, documentation, research agents       |
| `red`    | Safety     | Security checks, destructive operations, warnings |
| `orange` | Other      | Agents that don't fit other categories (reserved) |

**Example:**

```yaml
---
name: code-reviewer
color: green
---
```

**Guidelines:**

- Match color to primary function, not secondary features
- Be consistent within a plugin (all quality agents green)
- Reserve `orange` for agents that don't fit established categories
- Colors are optional but improve UX for multi-agent workflows

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

## Quality Checklist

Before finalizing an agent:

1. **Fetch official docs** - Verify against current specification
1. **Check structure** - Valid YAML frontmatter, required fields present
1. **Scan for forbidden language** - No user interaction phrases
1. **Validate tools** - Match autonomous responsibilities, no AskUserQuestion
1. **Test description** - Specific triggering conditions, not generic
1. **Review system prompt** - Single H1, clear structure, actionable instructions
1. **Verify no hardcoding** - No version-specific details that will become outdated
1. **Set color** - Choose semantic color matching agent's primary function (creator=blue, quality=green, ops=yellow, meta=purple, research=cyan, safety=red, other=orange)

## Path Resolution

When writing agents:

1. If caller specifies path → use exact path
1. If working in `.claude/agents/` → use that
1. Default → `.claude/agents/` (project-level)
1. User-level (`~/.claude/agents/`) → only when explicitly requested
