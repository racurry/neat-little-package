---
name: sub-agent-design
description: Interpretive guidance for designing Claude Code agents. Helps apply official documentation effectively and avoid common pitfalls. Use when creating or reviewing agents.
---

# Agent Design

This skill provides interpretive guidance for creating Claude Code agents. It helps you understand what the docs mean and how to create excellent agents.

## Workflow Selection

| If you need to...                  | Go to...                                                                    |
| ---------------------------------- | --------------------------------------------------------------------------- |
| Understand agent isolation model   | [Critical Architecture Understanding](#critical-architecture-understanding) |
| Decide agent vs command vs skill   | [Decision Framework](#decision-framework)                                   |
| Decide what goes in agent vs skill | [Agent-Skill Relationship](#agent-skill-relationship)                       |
| Pick tools for an agent            | [Tool Selection Philosophy](#tool-selection-philosophy)                     |
| Write the description field        | [Description Field Design](#description-field-design)                       |
| Avoid common mistakes              | Read `gotchas.md`                                                           |
| Write agent system prompts         | Read `system-prompt.md`                                                     |
| Check color for status line        | [Color Selection](#color-selection)                                         |
| Validate before completing         | [Quality Checklist](#quality-checklist)                                     |

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

**The #1 thing to understand:** Claude Code uses **isolated contexts** with **return-based delegation**.

```text
User ↔ Main Claude ──→ Sub-Agent (isolated context)
                        │
                        └──→ Returns final result
                             (no back-and-forth)
```

**Critical implications:**

- Agents **CANNOT** ask users questions
- Agents **CANNOT** see main conversation history
- Agents **CAN** do autonomous work (write files, run tests, analyze code)
- Main Claude handles **ALL** user communication
- Delegation is **one-way** (call → return, not interactive)

**Why this matters:** Every design decision flows from this architecture. The "cannot see history" point is especially important—you must provide all necessary context in the agent prompt. Agents can't "continue from where we left off" or reference "our earlier discussion."

**Common misconception:** "Agents are just like functions"—No, they're isolated AI instances with their own context and tool access. If your agent prompt includes phrases like "ask the user" or "clarify with user", you've misunderstood the architecture.

### The Return-Based Model

**Execution flow:**

1. Main Claude decides to delegate
1. Sub-agent receives context + task
1. Sub-agent works autonomously in isolation
1. Sub-agent returns complete result
1. Main Claude integrates result and continues

**What this means for agent design:**

- **No mid-execution interaction**—agent can't pause and ask for clarification
- **Agent must have everything it needs upfront**—all context in the prompt
- **Results must be complete and actionable**—main Claude shouldn't need to ask follow-ups

**Design test:** If your agent needs to ask questions mid-execution, redesign the delegation pattern. Either provide more context upfront, or split into multiple agents.

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

### Agent-Skill Relationship

**Core principle:** When an agent loads a skill, knowledge lives in the skill; the agent focuses on process.

**Decision logic:**

| Agent has backing skill? | Where knowledge goes            | Agent contains                       |
| ------------------------ | ------------------------------- | ------------------------------------ |
| Yes, loads a skill       | Skill contains domain knowledge | Process, mechanics, validation steps |
| No backing skill         | Agent contains domain knowledge | Both process AND knowledge           |

**Why this matters:**

- Avoids duplication (same knowledge in agent AND skill)
- Single source of truth (update skill, all agents benefit)
- Smaller agent prompts (less context consumed)
- Skills are reusable across multiple agents

**Pattern for skill-backed agents:**

```markdown
## Process

1. **Load design skill (REQUIRED)**
```

Use Skill tool: skill="my-plugin:my-skill"

```

2. **Follow skill guidance** for [specific aspect]:
- See `SKILL.md` for [topic]
- See `subfile.md` for [detailed topic]

3. **Execute task** using skill patterns
```

**Pattern for standalone agents (no skill):**

```markdown
## Process

1. **Understand requirements** [process step]

2. **Apply domain knowledge** [embedded in agent]:
   - Guideline one
   - Guideline two
   - Decision framework here

3. **Execute task** [process step]
```

**Anti-pattern:** Agent loads skill but also embeds same knowledge inline. This causes:

- Maintenance burden (update two places)
- Context waste (duplicate content loaded)
- Potential conflicts (agent and skill disagree)

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
