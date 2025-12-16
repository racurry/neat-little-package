# Box Factory Development Guidelines

## Philosophy

**Low-Maintenance First**

- Skills MUST defer to official docs via WebFetch (never hardcode model names, tool lists, syntax)
- Agents MUST fetch current specifications before creating components
- All components MUST apply knowledge delta filter (only document what Claude doesn't know)
- Documentation changes; principles don't
- Version bumps are automated via pre-commit hook

**Two-Layer Approach**

- Layer 1: Official specs (what docs explicitly say)
- Layer 2: Best practices (interpretive guidance, gotchas, anti-patterns, user preferences)
- Always distinguish which layer you're in when it would otherwise confuse Claude (eg, claude might think an opinion is 'factually incorrect')

**Delegation Pattern**

- Commands are thin wrappers
- Agents do complex work in isolation
- Skills provide guidance to the main agent or sub-agents
- Hooks enforce deterministic rules

**Knowledge Delta Filter (Critical):**

- ✅ Include: User-specific preferences, edge cases, decision frameworks, things Claude gets wrong, new tech
- ❌ Exclude: Basic commands Claude knows, standard workflows, general best practices
- Focused components that add real value in documentation and prompts

## Component Patterns

### Skills

- Point to official docs for things Claude might not know (not basics)
- Progressive disclosure: Core concepts → Advanced features
- Include: Decision frameworks, common pitfalls, quality checklists
- Keep SKILL.md < 300 lines

### Agents

- No user interaction language ("ask the user" = forbidden)
- Tools match autonomous responsibilities
- Strong delegation in description ("ALWAYS use when...", "MUST BE USED when...")
- Reference skills for guidance when appropriate

### Commands

- Delegation pattern: Keep command simple, delegate to specialized agent for complex work
- Always include `description` field (improves discoverability)
- Use `argument-hint` for expected arguments
- Let agents handle complexity, validation, and decision-making

### Hooks

- Fast execution (< 60s or set custom timeout)
- Quote all variables: `"$VAR"` not `$VAR`
- Validate inputs (path traversal, sensitive files)

**Language Selection:**

- **Bash:** Simple operations (< 20 lines, text processing, command chaining)
- **Python+UV:** Complex logic (JSON parsing, API calls, validation, multi-step processing)

**Security:**

- Quote all variables
- Validate stdin JSON inputs
- Block path traversal (`..` in paths)
- Skip sensitive files (.env, credentials)
- Use absolute paths with environment variables

## Decision Framework

**When creating Box Factory components, ask:**

1. **Skill vs Agent?**

   - Skill = Knowledge that loads when relevant, interpretive guidance
   - Agent = Does actual work autonomously (writes files, runs tests)

2. **Command pattern?**

   - Command = thin wrapper, agent = complex logic

3. **Read-only vs Write?**

   - Validation/review agents = Read, Grep, Glob, WebFetch only
   - Creation agents = Add Write, Edit as needed

4. **What design skill applies?**

   - Creating agents → use sub-agent-design
   - Creating commands → use slash-command-design
   - Creating skills → use skill-design
   - Creating hooks → use hooks-design
   - Creating plugins → use plugin-design
   - Creating marketplace → use plugin-design

## Architecture

```
User → Command → Specialized Agent → Design Skill
         ↓            ↓                   ↓
     (thin wrap)  (complex logic)    (guidance)
```

**Example:** `/box-factory:add-sub-agent` → sub-agent-writer → sub-agent-design skill

All Box Factory components are self-documenting examples of the patterns they teach.

## Quality Standards

**Before completing any Box Factory component:**

- ✓ Follows relevant design skill patterns
- ✓ Defers to official docs (no hardcoded specifics)
- ✓ Applies knowledge delta filter (skills only)
- ✓ Includes examples with before/after
- ✓ No user interaction language in agents
- ✓ Tools match responsibilities
- ✓ Skill tool included if agent loads skills
- ✓ Task tool included if agent delegates
- ✓ Clear, specific descriptions for autonomous delegation

## Anti-Patterns

- ❌ Duplicating official documentation
- ❌ Hardcoding version-specific details (models, tools, syntax)
- ❌ Documenting basic commands Claude already knows
- ❌ Comprehensive documentation instead of knowledge delta
- ❌ Agents with user interaction language ("ask the user", "confirm with user")
- ❌ Vague descriptions that don't trigger delegation

## Validation Workflow

### Creating Components

1. Load relevant design skills
2. Fetch official documentation
3. Create component following patterns
4. Self-validate against quality checklist
5. Return complete result

### Validating Components

1. Load box-factory-architecture skill
2. Load component-specific design skill
3. Fetch official documentation
4. Check structure, syntax, specifications
5. Detect anti-patterns
6. Generate detailed report with file:line references

### Reviewing Components

1. Identify component type
2. Load box-factory-architecture + component-specific skill
3. Fetch official documentation
4. Analyze against design patterns
5. Provide prioritized feedback (critical, important, minor)
6. Suggest specific improvements with examples

## Component Creation Best Practices

### Writer Agents Must

1. Load both box-factory-architecture AND component-specific design skill
2. Fetch official documentation before creating
3. Self-validate against quality checklist
4. Delegate component creation to specialized agents (never create directly)

### Quality Agents Must

1. Load box-factory-architecture AND relevant design skills
2. Fetch current official documentation
3. Provide specific file:line references
4. Distinguish between errors (blocking) and warnings (quality)
5. Include actionable fix recommendations
