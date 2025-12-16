# Core Architectural Concepts

## The Isolation Model (Critical Concept)

**The #1 thing to understand:** Claude Code uses **isolated contexts** with **return-based delegation**.

```markdown
User ↔ Main Claude Agent ──→ Sub-Agent (isolated context)
                        │
                        └──→ Returns final result to Main Claude Agent
                             (no back-and-forth)
```

**Critical implications:**

- Sub-agents **CANNOT** ask users questions
- Sub-agents **CANNOT** see main conversation history
- Sub-agents **CAN** do autonomous work (write files, run tests, analyze code)
- Main Claude Agent handles **ALL** user communication
- Delegation is **one-way** (call → return, not interactive)

**Why this matters:** Every design decision flows from this architecture.

**Common misconception:** "Agents are just like functions" - No, they're isolated AI instances with their own context and tool access.

## The Return-Based Model (Critical Concept)

**Execution flow:**

1. Main Claude decides to delegate
2. Sub-agent receives context + task
3. Sub-agent works autonomously in isolation
4. Sub-agent returns complete result
5. Main Claude Agent integrates result and continues

**What this means:**

- No mid-execution interaction
- No "asking for clarification"
- Agent must have everything it needs upfront
- Results must be complete and actionable

**Design test:** If your agent needs to ask questions mid-execution, redesign the delegation pattern.

## Progressive Disclosure Philosophy (Token Efficiency)

**Problem:** You can't put everything in the system prompt.

**Solution:** Load knowledge progressively when relevant.

**How it works:**

```markdown
Base Prompt (always loaded)
    ↓
Topic becomes relevant
    ↓
Skill loads automatically
    ↓
Provides specialized knowledge
```

**Why this matters:** Skills solve the "selective context" problem that CLAUDE.md and system prompts can't.

## Component Independence (Coupling Principle)

**Problem:** Components reference each other's internal file structure.

```markdown
**Deep dive:** [decision-frameworks.md](../other-skill/building-blocks/decision-frameworks.md)
```

**Why this fails:**

- Internal file structure may change
- Components may be reorganized
- Plugins may be distributed separately
- All direct paths become broken links

**Solution:** Reference components by identity, not internal structure.

```markdown
**Deep dive:** The box-factory-architecture skill's guidance on decision frameworks...
```

**Design principle:** A component's name and purpose are its public interface. Its internal file organization is an implementation detail.

**Why this matters:** Claude Code components are independently maintainable units. Cross-component references should survive internal reorganization.
