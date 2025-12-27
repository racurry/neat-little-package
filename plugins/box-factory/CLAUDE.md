# Box Factory Development Guidelines

## Philosophy

**Why CLAUDE.md, not a skill:** This content is always relevant when developing Box Factory components. For guidance on memory organization itself, load the memory-design skill.

**Low-Maintenance First**

- Skills MUST defer to official docs via WebFetch (never hardcode model names, tool lists, syntax)
- Agents MUST fetch current specifications before creating components
- All components MUST apply knowledge delta filter (only document what Claude doesn't know)
- Documentation changes; principles don't

**Two-Layer Approach**

- Layer 1: Official specs (what docs explicitly say)
- Layer 2: Best practices (interpretive guidance, gotchas, anti-patterns, user preferences)
- Always distinguish which layer you're in when it would otherwise confuse Claude

**Delegation Pattern**

- Commands are thin wrappers that delegate to agents
- Agents do complex work in isolation (cannot ask user questions)
- Skills provide guidance that loads when relevant
- Hooks enforce deterministic rules (no judgment calls)

**Knowledge Delta Filter (Critical)**

- **Include:** User-specific preferences, edge cases, decision frameworks, things Claude gets wrong, post-training knowledge
- **Exclude:** Basic commands Claude knows, standard workflows, general best practices
- Focused components that add real value in documentation and prompts

## Decision Framework

**When creating Box Factory components, ask:**

1. **Skill vs Agent?**

   - Skill = Knowledge that loads when relevant, interpretive guidance
   - Agent = Does actual work autonomously (writes files, runs tests)

2. **Command pattern?**

   - Command = thin wrapper, agent = complex logic

3. **Read-only vs Write?**

   - Validation/review agents = Read, Grep, Glob, WebFetch, Skill only
   - Creation agents = Add Write, Edit, Bash as needed

4. **Which design skill to load?**

   - Creating agents → load box-factory:sub-agent-design
   - Creating commands → load box-factory:slash-command-design
   - Creating skills → load box-factory:skill-design
   - Creating hooks → load box-factory:hook-design
   - Creating plugins → load box-factory:plugin-design
   - Creating rules → load box-factory:memory-design
   - Choosing component types → load box-factory:box-factory-architecture

## Architecture

Box Factory uses a three-tier delegation pattern:

```
/add-sub-agent  →  sub-agent-writer  →  sub-agent-design skill
       ↓                  ↓                      ↓
  (thin wrap)      (creates agent)        (provides guidance)
```

**The pattern:**

1. User invokes command (e.g., `/box-factory:add-sub-agent`)
2. Command delegates to specialized agent (e.g., `sub-agent-writer`)
3. Agent loads design skill(s) via `skills:` field (e.g., `sub-agent-design`)
4. Agent navigates skill using Skill Usage section pointers
5. Agent inlines quality checklist in its Process section
6. Agent returns complete result

**Self-documenting:** All Box Factory components are examples of the patterns they teach. Study the writer agents and design skills to see the patterns in action.

## Cross-Component Patterns

These patterns span multiple components and aren't captured in individual design skills:

**Skill-backed agents always load two skills:**

```yaml
skills: box-factory:box-factory-architecture, box-factory:sub-agent-design
```

- `box-factory-architecture` skill = cross-cutting concerns (isolation, communication, paths)
- Component-specific design skill = detailed guidance for that component type

**Agents inline quality checklists:**

Design skills define quality checklists. Agents copy the checklist items into their Process section (not just reference them) to ensure validation happens.

**Navigation pointers use indirect references:**

When an agent references a skill it loads, use section names, not file paths:

- ✅ `Consult sub-agent-design for Tool Selection Philosophy`
- ❌ `See sub-agent-design/gotchas.md`

A skill's internal file structure is an implementation detail from the agent's perspective.

## Delegation

**Creating components:** Use `/box-factory:add-*` commands. They delegate to specialized writer agents that load design skills, fetch official docs, and self-validate.

**Validating components:** Use `/box-factory:validate-plugin` or invoke the `validation-agent` directly. It loads architecture + component-specific skills and generates detailed reports.

**Reviewing components:** Use `/box-factory:review-component`. The `component-reviewer` agent provides prioritized feedback with specific file:line references.

Don't manually follow validation workflows - delegate to the agents that implement them.
