---
name: sub-agent-design
description: Interpretive guidance for designing Claude Code sub-agents. Helps apply official documentation effectively and avoid common pitfalls. ALWAYS use when creating or reviewing sub-agents (aka agents or subagents).
---

# Sub-agent Design

This skill provides interpretive guidance for creating Claude Code sub-agents (aka Subagents aka Agents). It helps you understand what the docs mean and how to create excellent sub-agents.

## Fundamentals

**Everything in this skill is built on top of the box-factory-architecture skill. Load that first!**

This skill adds sub-agent-specific guidance on top of that foundation.

## Workflow Selection

| If you need to...                      | Go to...                                                      |
| -------------------------------------- | ------------------------------------------------------------- |
| Understand sub-agent isolation model   | `box-factory-architecture` skill (load first)                 |
| Decide sub-agent vs command vs skill   | `box-factory-architecture` skill (component selection)        |
| Decide what goes in sub-agent vs skill | [Sub-agent-Skill Relationship](#sub-agent-skill-relationship) |
| Auto-load skills in a sub-agent        | [The `skills` Field](#the-skills-field-best-practice)         |
| Pick tools for a sub-agent             | [Tool Selection Philosophy](#tool-selection-philosophy)       |
| Write the description field            | [Description Field Design](#description-field-design)         |
| Avoid common mistakes                  | Read `gotchas.md`                                             |
| Check color for status line            | [Color Selection](#color-selection)                           |
| Validate before completing             | [Quality Checklist](#quality-checklist)                       |

## Quick Start

Sub-agent file structure:

```markdown
---
name: my-agent
description: Does X when Y. ALWAYS use when Z.
tools: Read, Grep, Glob, Skill
skills: my-plugin:my-design-skill
color: green
---

# My Agent

You are a specialized sub-agent that [purpose].

## Process

1. [Step one]
2. [Step two]

## Constraints

- Never include "ask the user" phrases (sub-agents can't interact with users)
```

**Critical:** Sub-agents operate in isolated context and return results. They cannot ask users questions.

## The `skills` Field (Best Practice)

The `skills` YAML field auto-loads skills when the sub-agent starts. This is especially valuable for Box Factory sub-agents that need design skills.

```yaml
---
name: agent-writer
description: Creates sub-agents. ALWAYS use when creating sub-agents.
tools: Read, Write, Edit, Glob, Grep, Skill, WebFetch
skills: box-factory:sub-agent-design
---
```

**When to use:**

| Pattern            | Choose When                                     | Avoid When                                    |
| ------------------ | ----------------------------------------------- | --------------------------------------------- |
| `skills` field     | Domain is fixed; always needs same skill        | Different skills needed based on context      |
| Skill tool in body | Domain varies; skill depends on runtime context | Same skill always needed (use `skills` field) |
| No skill           | No relevant skill exists                        | A skill exists with guidance Claude needs     |

**Box Factory pattern:** Writer sub-agents should declare their design skill dependency:

- `agent-writer` → `skills: box-factory:sub-agent-design`
- `skill-writer` → `skills: box-factory:skill-design`
- `command-writer` → `skills: box-factory:slash-command-design`

**Note:** Still include `Skill` in your `tools` list - the sub-agent may need to load additional skills during execution.

**Example of conditional skill loading** (Skill tool in body pattern):

```markdown
---
name: component-validator
description: Validates Claude Code components. MUST BE USED when validating plugins or components.
tools: Read, Grep, Glob, Skill, WebFetch
---

# Component Validator

## Process

1. **Identify component type** from file structure
2. **Load relevant design skill:**
   - Plugin → `Skill box-factory:plugin-design`
   - Sub-agent → `Skill box-factory:sub-agent-design`
   - Skill → `Skill box-factory:skill-design`
   - Command → `Skill box-factory:slash-command-design`
3. **Validate** against loaded skill's patterns
```

This sub-agent can't declare a single skill upfront because which skill it needs depends on what component type it discovers at runtime.

## Official Documentation

**Claude Code changes rapidly and is post-training knowledge.** Fetch these docs when creating sub-agents to ensure current syntax:

- **<https://code.claude.com/docs/en/sub-agents.md>** - Core specification and examples
- **<https://code.claude.com/docs/en/settings#tools-available-to-claude>** - Verify tool names
- **<https://code.claude.com/docs/en/model-config.md>** - Current model options

## Sub-agent-Skill Relationship

**Core principle:** When a sub-agent loads a skill, knowledge lives in the skill; the sub-agent focuses on process.

**Decision logic:**

| Sub-agent has backing skill? | Where knowledge goes            | Sub-agent contains                   |
| ---------------------------- | ------------------------------- | ------------------------------------ |
| Yes, loads a skill           | Skill contains domain knowledge | Process, mechanics, validation steps |
| No backing skill             | Sub-agent contains it           | Both process AND knowledge           |

**Why this matters:**

- Avoids duplication (same knowledge in sub-agent AND skill)
- Single source of truth (update skill, all sub-agents benefit)
- Smaller sub-agent prompts (less context consumed)
- Skills are reusable across multiple sub-agents

**Pattern for skill-backed sub-agents:**

Prefer the `skills` YAML field (see [The `skills` Field](#the-skills-field-best-practice)) to auto-load skills at startup. The sub-agent body then focuses on process:

```markdown
## Process

1. **Follow skill guidance** for [specific aspect]:
   - See `SKILL.md` for [topic]
   - See `subfile.md` for [detailed topic]

2. **Execute task** using skill patterns
```

**Pattern for standalone sub-agents (no skill):**

```markdown
## Process

1. **Understand requirements** [process step]

2. **Apply domain knowledge** [embedded in sub-agent]:
   - Guideline one
   - Guideline two
   - Decision framework here

3. **Execute task** [process step]
```

**Anti-pattern:** Sub-agent loads skill but also embeds same knowledge inline. This causes:

- Maintenance burden (update two places)
- Context waste (duplicate content loaded)
- Potential conflicts (sub-agent and skill disagree)

## Tool Selection Philosophy

**Key constraint:** Never include AskUserQuestion—sub-agents can't interact with users.

**General principle:** Match tools to the sub-agent's job. Reviewers should be read-only; builders need write access.

## Color Selection

The `color` field sets visual distinction for sub-agents in the status line.

- **Official spec:** Optional
- **Box Factory requirement:** Required for all sub-agents

**Note:** Color support is not documented officially. The following was verified through testing—Claude often guesses wrong colors that don't render.

**Supported colors (7 total):** `red`, `green`, `blue`, `yellow`, `cyan`, `purple`, `orange`

**Not supported:** `magenta`, `white`, `black`, `gray`, `grey`, `*Bright` variants

**Semantic mapping:**

| Color    | Category   | Use For                                               |
| -------- | ---------- | ----------------------------------------------------- |
| `blue`   | Creators   | Sub-agents that create/write files, components, code  |
| `green`  | Quality    | Validators, reviewers, checkers, analyzers            |
| `yellow` | Operations | Git, deployment, CI/CD, system tasks                  |
| `purple` | Meta       | Sub-agents that create other sub-agents               |
| `cyan`   | Research   | Exploration, documentation, research sub-agents       |
| `red`    | Safety     | Security checks, destructive operations, warnings     |
| `orange` | Other      | Sub-agents that don't fit other categories (reserved) |

**Example:**

```yaml
---
name: code-reviewer
color: green
---
```

**Guidelines:**

- Match color to primary function, not secondary features
- Be consistent within a plugin (all quality sub-agents green)
- Reserve `orange` for sub-agents that don't fit established categories

## Description Field Design

The `description` field determines when Main Claude delegates to your sub-agent. This is critical for autonomous invocation.

**Official requirement:** "Natural language explanation of when to invoke the subagent"

**Quality test:** Would Main Claude invoke this sub-agent based on context alone, or only when explicitly asked?

**Guidelines:**

- State WHEN to use (triggering conditions), not just WHAT it does
- Be specific about context and use cases
- Test empirically - if your sub-agent isn't being invoked automatically, revise the description
- Avoid overly generic descriptions that match too many scenarios

## Quality Checklist

Before finalizing a sub-agent:

1. **Fetch official docs** - Verify against current specification
2. **Check structure** - Valid YAML frontmatter, required fields present
3. **Scan for forbidden language** - No user interaction phrases
4. **Validate tools** - Match autonomous responsibilities, no AskUserQuestion
5. **Test description** - Specific triggering conditions, not generic
6. **Review system prompt** - Single H1, clear structure, actionable instructions
7. **Verify no hardcoding** - No version-specific details that will become outdated
8. **Set color** - Choose semantic color matching sub-agent's primary function (creator=blue, quality=green, ops=yellow, meta=purple, research=cyan, safety=red, other=orange)
