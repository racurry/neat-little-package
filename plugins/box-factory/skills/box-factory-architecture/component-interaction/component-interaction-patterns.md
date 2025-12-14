# Component Interaction Patterns (Best Practices)

## Core Philosophy

### Thin Wrapper Principle

**Core principle:** Each component has one focused responsibility.

**Command responsibilities:**

- Argument handling
- User-facing description
- Delegation to agent

**Agent responsibilities:**

- Complex logic
- File operations
- Tool orchestration
- Result synthesis

**Skill responsibilities:**

- Interpretive guidance
- Best practices
- Decision frameworks
- Progressive knowledge

**Hook responsibilities:**

- Deterministic enforcement
- Lifecycle integration
- External tool execution

### Single Responsibility

**Good component scope:**

- Focused on one domain
- Self-contained knowledge/behavior
- Clear boundaries
- Composable with other components

**Bad component scope:**

- "Do everything" agent
- Command that reimplements agent logic
- Skill covering unrelated topics
- Hook with complex branching logic

**Examples:**

✅ `python-test-runner` agent (specific language)
✅ `api-design` skill (focused domain)
✅ `deploy-staging` command (single operation)
✅ PostToolUse:Write→prettier hook (one formatter)

❌ `full-stack-developer` agent (too broad)
❌ `all-standards` skill (kitchen sink)
❌ `do-everything` command (unclear purpose)
❌ Hook with 10 conditional branches (too complex)

## Interaction Patterns

### Pattern 1: Command → Agent (Delegation)

**Most common Box Factory pattern:** Commands are thin wrappers that delegate to specialized agents.

```text
User types: /add-agent

Command: add-agent.md
├── Description: "Create a new Claude Code agent"
├── Arguments: $1 (agent name), $2 (purpose)
└── Prompt: "Use the agent-writer agent to create..."

Agent: agent-writer.md
├── Isolated context
├── Tools: Read, Write, WebFetch
├── Loads: agent-design skill
└── Returns: Complete agent file
```

**Why this works:**

- Command stays simple (argument handling)
- Agent handles complexity in isolation
- Skill provides interpretive guidance
- Clear separation of concerns

**Examples in Box Factory:**

- `/add-agent` → `agent-writer`
- `/add-command` → `slash-command-writer`
- `/add-skill` → `skill-writer`

### Pattern 2: Agent → Skill (Knowledge Loading)

**Progressive disclosure pattern:** Agents load skills automatically when topics become relevant.

```text
Agent: agent-writer
├── Task: Create new agent
├── Topic: "agent design"
├── Trigger: skill-design description matches
└── Loads: agent-design skill
    ├── Fetches: Official docs
    ├── Provides: Best practices
    └── Guides: Creation process
```

**Why this works:**

- Skill loaded only when needed (token efficient)
- Agent gets specialized knowledge automatically
- Skill defers to official docs (low maintenance)
- Two-layer approach (specs + guidance)

**Examples in Box Factory:**

- Creating agents → loads `agent-design`
- Creating skills → loads `skill-design`
- Creating commands → loads `slash-command-design`

### Pattern 3: Main Claude Agent → Sub-Agent (Nested Delegation)

**Nested delegation pattern:** Agents can delegate to more specialized sub-agents.

```text
Main Claude
    ↓
Command → Main Claude Agent
             ↓
         Sub-Agent (specialized)
             ↓
         Returns result
```

**Critical constraints:**

- All agents operate in isolated contexts
- No mid-execution questions upward
- Each level returns complete results
- Tools must be granted at each level

**Example flow:**

```text
User: "Create a comprehensive test suite"

Main Claude Agent → test-suite-creator (primary agent)
    ├── Analyzes codebase structure
    ├── Identifies test needs
    └── Delegates → test-file-generator (sub-agent)
        ├── Creates individual test files
        └── Returns test code

test-suite-creator receives results
    ├── Integrates test files
    └── Returns complete suite to Main Claude
```

### Pattern 4: Hook + Agent (Enforcement + Intelligence)

**Combined pattern:** Hooks enforce rules, sub-agents provide intelligence.

```text
PreToolUse:Bash hook
    ├── Validates command safety (deterministic)
    ├── Blocks dangerous operations (exit 2)
    └── If borderline → delegates to security-reviewer sub-agent
        ├── Sub-agent analyzes context
        └── Returns recommendation
```

**Why combine:**

- Hook provides guaranteed enforcement
- Sub-agent provides context-aware judgment
- Best of both worlds

**Example:**

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "~/.claude/hooks/security-check.sh"
        },
        {
          "type": "prompt",
          "command": "Analyze this bash command for security risks"
        }
      ]
    }
  ]
}
```

### Pattern 5: Skill + Multiple Components (Shared Knowledge)

**Knowledge reuse pattern:** One skill guides multiple sub-agents and commands.

```text
agent-design skill
    ↑
    ├── Loaded by: agent-writer agent
    ├── Loaded by: component-reviewer agent
    └── Loaded by: validation-agent agent
```

**Why this works:**

- Single source of truth
- Consistent guidance across components
- Update skill → improves all consumers
- Token efficient (load once, use many times)

## Anti-Patterns

**Command with complex logic:**

```markdown
# ❌ Bad: Command doing agent's work
---
description: Create agent
---
Read the codebase, analyze patterns, generate agent file,
validate structure, write to disk, run tests...

# ✅ Good: Command delegating
---
description: Create agent
---
Use the agent-writer agent to create a new agent named $1 for purpose: $2
```

**Scope violations:**

| Component | Anti-Pattern            | Correct Scope        |
| --------- | ----------------------- | -------------------- |
| Sub-agent     | `full-stack-developer`  | `python-test-runner` |
| Skill     | `all-standards`         | `api-design`         |
| Command   | `do-everything`         | `deploy-staging`     |
| Hook      | 10 conditional branches | Single formatter     |
