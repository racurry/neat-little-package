# Forge Development Guidelines

## Philosophy

**Low-Maintenance First**
- Skills MUST defer to official docs via WebFetch (never hardcode model names, tool lists, syntax)
- Agents MUST fetch current specifications before creating components
- Documentation changes; principles don't

**Two-Layer Approach**
- Layer 1: Official specs (what docs explicitly say)
- Layer 2: Best practices (interpretive guidance, gotchas, anti-patterns)
- Always distinguish which layer you're in

**Evidence-Based**
- Claims must be grounded in official docs OR clearly marked as opinions
- Never present best practices as official requirements

## Component Patterns

### Skills
- Fetch-first: Always include "Required Reading" with WebFetch URLs
- Progressive disclosure: Core concepts → Advanced features
- Mark sections: "(Official Specification)" vs "(Best Practices)"
- Include: Decision frameworks, common pitfalls, quality checklists
- Filename: `SKILL.md` (uppercase) in `skills/[name]/` subdirectory

### Agents
- No user interaction language ("ask the user" = forbidden)
- Tools match autonomous responsibilities (reviewers = read-only, writers = write access)
- Strong delegation in description ("ALWAYS use when...", "Use proactively when...")
- Reference design skills for guidance
- Model: haiku (simple), sonnet (balanced), opus (complex reasoning)

### Commands
- Delegation pattern: Keep command simple, delegate to specialized agent
- Always include `description` field (improves discoverability)
- Use `argument-hint` for expected arguments
- Let agents handle complexity, validation, and decision-making

### Hooks
- Fast execution (< 60s or set custom timeout)
- Quote all variables: `"$VAR"` not `$VAR`
- Exit 2 = blocking (use sparingly, security/safety only)
- Validate inputs (path traversal, sensitive files)

## Decision Framework

**When creating Forge components, ask:**

1. **Skill vs Agent?**
   - Skill = Knowledge that loads when relevant, interpretive guidance
   - Agent = Does actual work autonomously (writes files, runs tests)

2. **Command pattern?**
   - ALL Forge commands delegate to specialized agents
   - Command = thin wrapper, agent = complex logic

3. **Read-only vs Write?**
   - Validation/review agents = Read, Grep, Glob, WebFetch only
   - Creation agents = Add Write, Edit as needed

4. **What design skill applies?**
   - Creating agents → use agent-design
   - Creating commands → use slash-command-design
   - Creating skills → use skill-design
   - Creating hooks → use hooks-design

## Quality Standards

**Before completing any Forge component:**

- ✓ Follows relevant design skill patterns
- ✓ Defers to official docs (no hardcoded specifics)
- ✓ Distinguishes specs from best practices
- ✓ Includes examples with before/after
- ✓ No user interaction language in agents
- ✓ Tools match responsibilities
- ✓ Clear, specific descriptions for autonomous delegation

## Anti-Patterns (Forbidden)

**In Skills:**
- ❌ Duplicating official documentation
- ❌ Hardcoding version-specific details (models, tools, syntax)
- ❌ Presenting opinions as official requirements

**In Agents:**
- ❌ User interaction language ("ask the user", "confirm with user")
- ❌ Tool mismatches (reviewer with Write, generator with Read-only)
- ❌ Vague descriptions that don't trigger delegation

**In Commands:**
- ❌ Reimplementing agent logic in command prompt
- ❌ Complex argument parsing (let agents handle)
- ❌ Missing description field

## Architecture

```
User → Command → Specialized Agent → Design Skill
         ↓            ↓                   ↓
     (thin wrap)  (complex logic)    (guidance)
```

**Example:** `/add-agent` → agent-writer → agent-design skill

All Forge components are self-documenting examples of the patterns they teach.
