# System Prompt Best Practices

Reference file for sub-agent-design skill. Read when writing or reviewing agent system prompts.

## Structure

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

## Content Quality

**Be specific and actionable:**

- "Run pytest -v and parse output for failures"
- "Only analyze Python files in src/ directory"

**Avoid vague instructions:**

- "Run tests and check for problems"
- "Analyze code"

**Include constraints:**

- "Never modify production configuration files"
- "Only analyze; never modify code"

## Section Guidelines

### Purpose Section

One paragraph explaining:

- What the agent does
- When it should be invoked
- What it returns

### Process Section

Numbered steps for the agent's workflow:

1. Load required skills (if any)
1. Gather context
1. Execute task
1. Validate results
1. Return findings

### Guidelines Section

Bullet points for key principles:

- Domain-specific rules
- Quality standards
- Decision frameworks

### Constraints Section

What the agent should NOT do:

- Scope boundaries
- Forbidden operations
- Safety limits

## Skill-Backed Agent Pattern

When agent loads a skill, the system prompt should defer knowledge:

```markdown
## Process

1. **Load design skill (REQUIRED)**
   Use Skill tool: skill="plugin:skill-name"

2. **Follow skill guidance** for [task]:
   - See `SKILL.md` for [core concepts]
   - See `subfile.md` for [detailed topic]

3. **Execute task** per skill patterns

4. **Validate** against skill checklist
```

**Key principle:** Process steps stay in agent; knowledge lives in skill.
