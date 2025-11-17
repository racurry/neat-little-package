---
name: box-factory-architecture
description: Interpretive guidance for understanding Claude Code component architecture and choosing between agents, skills, commands, and hooks. Helps decide which component type fits a use case, understand delegation and isolation, debug cross-component issues, and design cohesive plugin architectures. Use when choosing component types, designing plugins with multiple components, debugging delegation failures, asking about component interaction patterns, or creating Box Factory-compliant components.
---

# Box Factory Architecture Skill

This meta-skill teaches the Claude Code ecosystem architecture - how components interact, when to use each type, and how to design cohesive multi-component solutions. **This applies to both Main Claude (choosing what to create) and sub-agents (understanding their role).**

## Required Reading Before Designing Components

Fetch these docs with WebFetch to understand the official ecosystem:

- **https://code.claude.com/docs/en/sub-agents.md** - Agent architecture and isolation model
- **https://code.claude.com/docs/en/slash-commands.md** - Command structure and triggering
- **https://code.claude.com/docs/en/hooks** - Hook lifecycle and execution
- **https://code.claude.com/docs/en/plugins** - Plugin packaging and distribution

## Core Architectural Understanding

### The Isolation Model (Critical Concept)

**The #1 thing to understand:** Claude Code uses **isolated contexts** with **return-based delegation**.

```
User ↔ Main Claude ──→ Sub-Agent (isolated context)
                        │
                        └──→ Returns final result
                             (no back-and-forth)
```

**Critical implications:**

- Sub-agents **CANNOT** ask users questions
- Sub-agents **CANNOT** see main conversation history
- Sub-agents **CAN** do autonomous work (write files, run tests, analyze code)
- Main Claude handles **ALL** user communication
- Delegation is **one-way** (call → return, not interactive)

**Why this matters:** Every design decision flows from this architecture.

**Common misconception:** "Agents are just like functions" - No, they're isolated AI instances with their own context and tool access.

### The Return-Based Model (Critical Concept)

**Execution flow:**

1. Main Claude decides to delegate
2. Sub-agent receives context + task
3. Sub-agent works autonomously in isolation
4. Sub-agent returns complete result
5. Main Claude integrates result and continues

**What this means:**

- No mid-execution interaction
- No "asking for clarification"
- Agent must have everything it needs upfront
- Results must be complete and actionable

**Design test:** If your agent needs to ask questions mid-execution, redesign the delegation pattern.

### Progressive Disclosure Philosophy (Token Efficiency)

**Problem:** You can't put everything in the system prompt.

**Solution:** Load knowledge progressively when relevant.

**How it works:**

```
Base Prompt (always loaded)
    ↓
Topic becomes relevant
    ↓
Skill loads automatically
    ↓
Provides specialized knowledge
```

**Why this matters:** Skills solve the "selective context" problem that CLAUDE.md and system prompts can't.

## Component Comparison (Official Specification)

What each component IS according to official documentation:

### Agents (from sub-agents.md)

**Official definition:** Specialized AI instances that run in isolated contexts with specific tools and prompts.

**Official structure:**
- YAML frontmatter with `name`, `description`, `model`, `tools`
- Markdown system prompt
- Return results to delegating agent

**Key characteristic:** Autonomous delegation based on context.

### Commands (from slash-commands.md)

**Official definition:** User-triggered prompts with optional argument substitution.

**Official structure:**
- Optional YAML frontmatter
- Markdown prompt with `$1`, `$2` or `$ARGUMENTS` placeholders
- Triggered explicitly by user typing `/command-name`

**Key characteristic:** Explicit user invocation.

### Skills (from sub-agents.md)

**Official definition:** Knowledge loaded when relevant topics arise.

**Official structure:**
- YAML frontmatter with `name`, `description`
- Markdown content in `SKILL.md` file
- Lives in `skills/[name]/SKILL.md` subdirectory

**Key characteristic:** Progressive knowledge disclosure.

### Hooks (from hooks documentation)

**Official definition:** Deterministic execution at lifecycle events.

**Official structure:**
- JSON configuration in settings
- Command-based (bash scripts) or prompt-based (Claude Haiku queries)
- Fire at specific events (PreToolUse, PostToolUse, SessionStart, etc.)

**Key characteristic:** Guaranteed execution every time.

## Component Comparison (Best Practices)

Decision framework for choosing the right component type:

### When to Use Each Component

**Use Agent when:**

- Need isolated context (won't pollute main conversation)
- Want autonomous delegation (triggered by context, not explicit request)
- Doing actual work (writing files, running tests, analyzing code)
- Require specific tool restrictions
- Complex decision-making within defined scope
- Task is part of larger workflows

**Examples:**
- `test-runner` - Executes tests and analyzes failures autonomously
- `code-reviewer` - Provides feedback without modifying code
- `documentation-generator` - Creates docs from code

**Use Command when:**

- User wants explicit control over when it runs
- Thin wrapper that delegates to specialized agent
- Simple argument substitution needed
- One-off user-triggered operation
- Wrapping bash scripts or tool sequences

**Examples:**
- `/add-agent` - User explicitly requests creating an agent
- `/deploy` - User controls deployment timing
- `/analyze-security` - User-triggered analysis

**Use Skill when:**

- Knowledge needed across multiple contexts
- Substantial procedural expertise (20+ lines)
- Interpretive guidance that enhances understanding
- Best practices that apply to multiple scenarios
- Progressive disclosure saves tokens
- Teaching "how to think about" something

**Examples:**
- `agent-design` - Guidance for creating agents
- `api-standards` - Team API conventions
- `testing-strategy` - Testing philosophy and patterns

**Use Hook when:**

- Need **guaranteed** execution every single time
- Simple, deterministic rule enforcement
- Integrating external tools (linters, formatters)
- Performance or safety enforcement
- Must happen at specific lifecycle event
- "Always" matters more than "usually"

**Examples:**
- Format code after every write
- Security validation before bash commands
- Load project context at session start
- Auto-commit after conversation stops

## Component Interaction Patterns (Best Practices)

### Pattern 1: Command → Agent (Delegation Pattern)

**Most common Box Factory pattern:** Commands are thin wrappers that delegate to specialized agents.

```
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

```
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

### Pattern 3: Agent → Sub-Agent (Specialized Delegation)

**Nested delegation pattern:** Agents can delegate to more specialized sub-agents.

```
Main Claude
    ↓
Command → Primary Agent
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

```
User: "Create a comprehensive test suite"

Main Claude → test-suite-creator (primary agent)
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

**Combined pattern:** Hooks enforce rules, agents provide intelligence.

```
PreToolUse:Bash hook
    ├── Validates command safety (deterministic)
    ├── Blocks dangerous operations (exit 2)
    └── If borderline → delegates to security-reviewer agent
        ├── Agent analyzes context
        └── Returns recommendation
```

**Why combine:**

- Hook provides guaranteed enforcement
- Agent provides context-aware judgment
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

**Knowledge reuse pattern:** One skill guides multiple agents and commands.

```
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

## Delegation Chains (Architecture Deep Dive)

### How Isolated Context Works

**When Main Claude delegates to sub-agent:**

```
Main Claude context:
├── Full conversation history
├── User messages
├── Previous tool calls
└── All context accumulated

Sub-Agent context:
├── Only: Task description from delegation
├── Only: Files/data explicitly passed
├── No access to main conversation
└── Fresh, isolated environment
```

**Critical: Information flow is ONE WAY (Main → Sub)**

### What Agents Can't Do (Because of Isolation)

**Forbidden patterns:**

❌ "Ask the user for the target directory"
❌ "Request clarification from the user"
❌ "Confirm with the user before proceeding"
❌ "Wait for user input"
❌ "Check with the user about preferences"

**Why these fail:** Agent is isolated, can't communicate with user.

**Correct patterns:**

✅ "Use the provided directory parameter or default to ./src"
✅ "Infer from project structure and available context"
✅ "Make reasonable assumptions based on common patterns"
✅ "Use environment context to determine approach"
✅ "Default to [specific behavior] when unclear"

### Multi-Level Delegation Example

**Complete flow with isolation model:**

```
User: "/add-agent test-runner 'Run tests and analyze failures'"

Main Claude:
├── Sees: Full conversation history
├── Interprets: User wants new agent created
├── Triggers: /add-agent command (explicit)
└── Delegates to: agent-writer agent
    │
    Sub-Agent (agent-writer):
    ├── Context: Only task params (name, purpose)
    ├── Loads: agent-design skill (triggered by topic)
    ├── Fetches: Official docs (per skill guidance)
    ├── Creates: test-runner.md agent file
    └── Returns: "Created agent at .claude/agents/test-runner.md"

Main Claude:
├── Receives: Complete result from sub-agent
├── Integrates: Into conversation
└── Responds: "I've created the test-runner agent..."
```

**Key observations:**

1. Command triggered explicitly (user typed `/add-agent`)
2. Agent-writer operates in isolation (can't ask questions)
3. Skill loads automatically (relevant topic)
4. Agent returns complete result (file created)
5. Main Claude integrates and communicates with user

## Cross-Component Patterns (Best Practices)

### The Thin Wrapper Philosophy

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

**Anti-pattern:** Command with complex logic that belongs in agent.

**Correct pattern:**

```markdown
# Command: add-agent.md
Use the agent-writer agent to create a new agent named $1 for purpose: $2

# Agent: agent-writer.md
[Full creation logic, file writing, validation]

# Skill: agent-design.md
[Interpretive guidance on agent design principles]
```

### Single Responsibility Per Component

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

### Tool Permission Strategy

**Match tools to responsibilities:**

```
Review/Analysis Agents:
└── Tools: Read, Grep, Glob, WebFetch
    (Read-only, can't modify code)

Creation Agents:
└── Tools: Read, Write, Edit, WebFetch, Glob
    (Can create/modify files)

Test/Build Agents:
└── Tools: Read, Bash, Grep
    (Can execute, analyze output)

Full-Power Agents:
└── Tools: All available
    (Unrestricted, use carefully)
```

**Anti-pattern:** Review agent with Write access (temptation to fix instead of report).

**Correct pattern:** Separate agents for review vs fixing.

## Common Architectural Anti-Patterns

### Anti-Pattern 1: Interactive Agent Design

**Problem:** Agent designed assuming user interaction.

**What it looks like:**

```markdown
# Agent system prompt
1. Analyze the codebase
2. Ask the user which files to focus on  ← FORBIDDEN
3. Request user's preferred style       ← FORBIDDEN
4. Generate documentation
5. Confirm with user before writing     ← FORBIDDEN
```

**Why it fails:** Agents operate in isolated context with no user access.

**Solution:**

```markdown
# Agent system prompt
1. Analyze the codebase
2. Use provided file parameters or infer from project structure
3. Apply documented style from CLAUDE.md or common conventions
4. Generate documentation
5. Write files using available context and defaults
```

**Key change:** Replace all user interaction with autonomous decision-making.

### Anti-Pattern 2: Command with Complex Logic

**Problem:** Command tries to implement business logic instead of delegating.

**What it looks like:**

```markdown
---
description: Run tests
---

First check if pytest or jest is configured.
If pytest, scan for conftest.py and parse fixtures.
If jest, check jest.config.js for custom settings.
Determine test file patterns from package.json or setup.cfg.
Execute tests with appropriate flags based on environment.
Parse output for failures and categorize by type.
Generate summary report with statistics.
```

**Why it fails:**

- Too complex for simple prompt substitution
- No error handling capability
- Hard to maintain
- Doesn't leverage agent isolation
- Can't use tools effectively

**Solution:**

```markdown
---
description: Run full test suite and analyze failures
---

Use the test-runner agent to execute all tests and provide detailed failure analysis.
```

**Agent handles:**
- Framework detection
- Configuration parsing
- Test execution
- Output analysis
- Report generation

### Anti-Pattern 3: Knowledge Duplication

**Problem:** Same knowledge hardcoded in multiple places.

**What it looks like:**

```
agent-writer.md:
  [50 lines about agent design best practices]

command-writer.md:
  [50 lines about agent design best practices]

hook-writer.md:
  [50 lines about agent design best practices]
```

**Why it fails:**

- Maintenance nightmare (update in 3 places)
- Token waste (loads redundantly)
- Inconsistency risk (versions drift)

**Solution:**

```
agent-design skill:
  [Comprehensive agent design guidance]

Agents load skill automatically:
  ├── agent-writer (loads when creating agents)
  ├── component-reviewer (loads when reviewing)
  └── validation-agent (loads when validating)
```

**Benefits:**

- Single source of truth
- Token efficient (progressive disclosure)
- Consistent guidance
- Easy to update

### Anti-Pattern 4: Hook Complexity Explosion

**Problem:** Hook tries to handle too many scenarios.

**What it looks like:**

```bash
#!/bin/bash
if [[ "$TOOL" == "Write" ]]; then
  if [[ "$FILE" == *.py ]]; then
    if [[ -f "pyproject.toml" ]]; then
      black "$FILE"
    elif [[ -f "setup.py" ]]; then
      autopep8 "$FILE"
    fi
  elif [[ "$FILE" == *.js ]]; then
    if [[ -f ".prettierrc" ]]; then
      prettier "$FILE"
    else
      eslint --fix "$FILE"
    fi
  fi
fi
```

**Why it fails:**

- Complex, brittle logic
- Hard to test
- Slow execution
- Difficult to debug
- Doesn't scale

**Solution:** Separate hooks for separate concerns.

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "prettier --write \"$CLAUDE_FILE_PATHS\" 2>/dev/null || true"
        }
      ]
    }
  ]
}
```

**Or:** Delegate intelligence to agent if needed.

### Anti-Pattern 5: Vague Component Descriptions

**Problem:** Descriptions don't trigger appropriate loading/delegation.

**What it looks like:**

```yaml
# Agent
description: "Helps with agents"

# Skill
description: "Agent information"

# Command
description: "Agent stuff"
```

**Why it fails:**

- Claude can't determine when to delegate
- Skill won't load automatically
- Command not discoverable in /help
- Poor user experience

**Solution:** Specific, triggering descriptions.

```yaml
# Agent
description: "Creates Claude Code agents following official specifications and best practices. ALWAYS use when user requests creating a new agent, or when you need to generate an agent autonomously."

# Skill
description: "Interpretive guidance for designing Claude Code agents. Helps apply official documentation effectively and avoid common pitfalls. Use when creating or reviewing agents."

# Command
description: "Create a new Claude Code agent with specified name and purpose"
```

**Pattern:** `[What] for [domain]. [Benefit]. Use when [triggers].`

## Plugin Architecture (Multi-Component Design)

### Cohesive Plugin Design

**Good plugin architecture:**

```
security-tools/
├── commands/
│   ├── scan-vulnerabilities.md    ← User-triggered scan
│   └── generate-security-report.md
├── agents/
│   ├── vulnerability-scanner.md    ← Does actual scanning
│   ├── security-reviewer.md        ← Reviews code
│   └── report-generator.md         ← Creates reports
├── skills/
│   └── security-best-practices/
│       └── SKILL.md                ← Shared knowledge
└── hooks/
    └── hooks.json                  ← Pre-bash security checks
```

**Component interaction:**

```
User: /scan-vulnerabilities
    ↓
Command: scan-vulnerabilities.md
    ├── Delegates → vulnerability-scanner agent
    │   ├── Loads → security-best-practices skill
    │   ├── Scans codebase
    │   └── Returns findings
    │
    └── Delegates → report-generator agent
        ├── Receives findings
        └── Returns formatted report

Meanwhile:
PreToolUse:Bash hook
    └── Enforces security constraints on all bash commands
```

**Why this works:**

- Commands are thin wrappers
- Agents do specialized work
- Skill provides shared knowledge
- Hooks enforce guarantees
- Components complement each other
- Clear separation of concerns

### Plugin Scope Philosophy

**Focused plugin (good):**

```
python-testing-suite/
└── Everything related to Python testing
    ├── Commands for running tests
    ├── Agents for test generation
    ├── Skills for testing strategy
    └── Hooks for auto-formatting test files
```

**Kitchen sink plugin (bad):**

```
development-tools/
└── Unrelated utilities
    ├── Python testing
    ├── Git helpers
    ├── Documentation generators
    ├── Deployment scripts
    └── Random utilities
```

**Problems with kitchen sink:**

- Unclear purpose
- Users only want subset
- Hard to maintain
- Versioning conflicts
- Discovery problems

## Debugging Cross-Component Issues

### Common Delegation Failures

**Symptom:** Agent not being invoked automatically.

**Diagnosis:**

1. Check agent description - too vague?
2. Verify agent is properly installed
3. Check tool permissions - missing required tools?
4. Review context - does situation match description?

**Fix:** Strengthen description with specific triggering conditions.

### Common Hook Failures

**Symptom:** Hook not executing.

**Diagnosis:**

1. Check hook configuration syntax
2. Verify matcher pattern (case-sensitive)
3. Review hook logs (CTRL-R in Claude Code)
4. Check timeout settings

**Fix:** Validate JSON, test hook in isolation.

### Common Skill Loading Issues

**Symptom:** Skill not loading when expected.

**Diagnosis:**

1. Check skill description - matches topic?
2. Verify filename is `SKILL.md` (uppercase)
3. Check directory structure (`skills/name/SKILL.md`)
4. Review frontmatter YAML syntax

**Fix:** Improve description triggering conditions.

## Quality Checklist for Multi-Component Design

Before finalizing a plugin or component set:

**Architecture (best practices):**

- ✓ Each component has single, focused responsibility
- ✓ Commands delegate to agents (thin wrapper pattern)
- ✓ Agents use appropriate tools for their role
- ✓ Skills provide shared knowledge (no duplication)
- ✓ Hooks enforce deterministic rules only
- ✓ No interactive patterns in agents
- ✓ Clear delegation chains documented

**Component interaction (best practices):**

- ✓ Commands → Agents delegation is clear
- ✓ Agents → Skills loading makes sense
- ✓ Agents → Sub-agents delegation is justified
- ✓ Hooks + Agents complement each other
- ✓ No circular dependencies
- ✓ Tool permissions match responsibilities

**Descriptions (best practices):**

- ✓ Agent descriptions trigger autonomous delegation
- ✓ Skill descriptions trigger automatic loading
- ✓ Command descriptions are discoverable in /help
- ✓ All descriptions follow "what, benefit, when" pattern

**Testing (best practices):**

- ✓ Test each component independently
- ✓ Test delegation chains end-to-end
- ✓ Verify skills load in appropriate contexts
- ✓ Confirm hooks execute at right events
- ✓ Validate error handling at each level

## Design Decision Tree

Use this when choosing component types:

```
START: What are you building?

├─ Do you need GUARANTEED execution every time?
│  └─ YES → Hook (deterministic enforcement)
│
├─ Is this USER-TRIGGERED explicitly?
│  └─ YES → Command
│      └─ Is it complex logic?
│          ├─ YES → Command delegates to Agent
│          └─ NO → Simple command with argument substitution
│
├─ Is this KNOWLEDGE that loads when relevant?
│  └─ YES → Skill
│      └─ Substantial (20+ lines)?
│          ├─ YES → Create skill
│          └─ NO → Put in CLAUDE.md instead
│
└─ Is this AUTONOMOUS WORK?
   └─ YES → Agent
       ├─ Need isolated context? → Sub-agent
       ├─ Need specific tools? → Configure tools field
       └─ Complex task? → Consider sub-agent delegation
```

## Examples: Complete Component Ecosystems

### Example 1: Testing Ecosystem

**Architecture:**

```
Commands (user-triggered):
├── /run-tests → Delegates to test-runner agent
└── /generate-tests → Delegates to test-generator agent

Agents (autonomous work):
├── test-runner
│   ├── Tools: Read, Bash, Grep
│   ├── Loads: testing-strategy skill
│   └── Purpose: Execute tests, analyze failures
│
└── test-generator
    ├── Tools: Read, Write, Glob
    ├── Loads: testing-strategy skill
    └── Purpose: Create test files from code

Skills (shared knowledge):
└── testing-strategy
    ├── Testing pyramid philosophy
    ├── When to mock patterns
    └── Test design principles

Hooks (enforcement):
└── PostToolUse:Write (*.test.*)
    └── Auto-format test files
```

**Interaction flow:**

```
User: /run-tests
    ↓
Command executes → test-runner agent
    ├── Loads testing-strategy skill
    ├── Detects test framework (pytest/jest)
    ├── Runs tests via Bash tool
    ├── Analyzes failures
    └── Returns detailed report

Main Claude:
    ├── Receives report
    ├── Suggests fixes
    └── May delegate to test-generator for missing tests
```

### Example 2: Documentation Ecosystem

**Architecture:**

```
Commands:
├── /document-api → Delegates to api-doc-generator
└── /review-docs → Delegates to doc-reviewer

Agents:
├── api-doc-generator
│   ├── Tools: Read, Write, WebFetch
│   ├── Loads: api-documentation-standards skill
│   └── Creates API documentation
│
└── doc-reviewer
    ├── Tools: Read, Grep
    ├── Loads: api-documentation-standards skill
    └── Reviews existing docs for compliance

Skills:
└── api-documentation-standards
    ├── OpenAPI specification patterns
    ├── Example formats
    └── Common pitfalls

Hooks:
└── PostToolUse:Write (*.md in docs/)
    └── Validates markdown syntax
```

### Example 3: Box Factory Meta-Ecosystem (Self-Documenting)

**Architecture:**

```
Commands:
├── /add-agent → agent-writer
├── /add-command → slash-command-writer
├── /add-skill → skill-writer
├── /add-hook → hooks-writer
└── /review-component → component-reviewer

Agents:
├── agent-writer (loads agent-design)
├── slash-command-writer (loads slash-command-design)
├── skill-writer (loads skill-design)
├── hooks-writer (loads hooks-design)
└── component-reviewer (loads all design skills)

Skills:
├── agent-design
├── slash-command-design
├── skill-design
├── hooks-design
├── plugin-design
└── box-factory-architecture (this skill!)
```

**Why this is powerful:**

- Box Factory uses its own patterns to create itself
- Each component exemplifies what it teaches
- Meta-skills guide creation of new components
- Self-documenting, self-consistent ecosystem

## Documentation References

These are the authoritative sources for the ecosystem:

**Core architecture:**

- https://code.claude.com/docs/en/sub-agents.md - Isolation model, delegation patterns
- https://code.claude.com/docs/en/slash-commands.md - User-triggered operations
- https://code.claude.com/docs/en/hooks - Lifecycle integration
- https://code.claude.com/docs/en/plugins - Component packaging

**Component-specific:**

- Fetch agent-design skill for agent creation guidance
- Fetch slash-command-design skill for command patterns
- Fetch skill-design skill for knowledge organization
- Fetch hooks-design skill for hook best practices
- Fetch plugin-design skill for multi-component packaging

**Remember:** This meta-skill teaches ecosystem patterns. Always fetch official docs and component-specific skills for detailed guidance.
