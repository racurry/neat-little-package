---
name: box-factory-slash-command-design
description: Interpretive guidance for designing Claude Code slash commands. Helps you apply official documentation effectively and create high-quality commands. Use when creating or reviewing slash commands.
---

# Slash Command Design Skill

This skill provides interpretive guidance and best practices for creating Claude Code slash commands. **ALWAYS fetch current official documentation before creating commands** - this skill helps you understand what the docs mean and how to create excellent commands.

## Required Reading Before Creating Commands

Fetch these docs with WebFetch every time:

- **https://code.claude.com/docs/en/slash-commands.md** - Core specification and examples
- **https://code.claude.com/docs/en/settings#tools-available-to-claude** - Verify tool names
- **https://code.claude.com/docs/en/model-config.md** - Model selection guidance

## Core Understanding

### Commands Are User-Triggered, Not Autonomous

**Key distinction:**

- **Commands** = User explicitly invokes with `/command-name`
- **Agents** = Claude autonomously delegates based on context
- **Skills** = Knowledge that loads when relevant

**Quality test:** If you want this to happen automatically based on context, it's an agent, not a command.

### Command Structure

Commands are Markdown files with optional YAML frontmatter:

```markdown
---
description: Brief description (optional, defaults to first line)
argument-hint: [expected-args]
allowed-tools: Tool1, Tool2
model: sonnet
disable-model-invocation: false
---

Command prompt content goes here.
Use $1, $2 for individual arguments or $ARGUMENTS for all.
```

## Frontmatter Fields (Official Specification)

All fields are optional:

| Field | Purpose | Default |
|-------|---------|---------|
| `description` | Brief command description for `/help` | First line of prompt |
| `argument-hint` | Expected arguments (e.g., `[pr-number] [priority]`) | None |
| `allowed-tools` | Restrict to specific tools (e.g., `Bash(git:*)`) | Inherits from conversation |
| `model` | Specific model to use | Inherits from conversation |
| `disable-model-invocation` | Prevents SlashCommand tool from auto-invoking | false |

**Best practice:** Always include `description` even though it's optional - improves discoverability and Claude's ability to use the SlashCommand tool.

## Argument Syntax (Official Specification)

**All arguments as single string:**

```markdown
$ARGUMENTS
```

Example: `/fix-issue 123 high-priority` → `$ARGUMENTS = "123 high-priority"`

**Individual positional arguments:**

```markdown
$1, $2, $3, etc.
```

Example: `/review-pr 456 high alice` → `$1="456"`, `$2="high"`, `$3="alice"`

**Official guidance:** "Use individual arguments (`$1`, `$2`) for complex commands with multiple parameters"

**Best practice:** Use `$1, $2` when you need arguments in different parts of the prompt or want to provide defaults. Keep argument parsing simple - if you need validation or complex logic, delegate to an agent.

## Advanced Features (Official Specification)

### Bash Execution with `!` Prefix

Execute bash commands before the prompt runs:

```markdown
---
allowed-tools: Bash(git:*)
---

!git status

Review the git status above and suggest next steps.
```

### File References with `@` Prefix

Include file contents in the prompt:

```markdown
Review @src/utils/helpers.js for potential improvements.
```

Multiple files: `Compare @src/old.js with @src/new.js`

### Subdirectory Namespacing

Organize commands in subdirectories:

```
.claude/commands/frontend/component.md → /component (project:frontend)
.claude/commands/backend/endpoint.md → /endpoint (project:backend)
```

Command name comes from filename, subdirectory appears in `/help` as namespace label.

## Decision Framework

### Command vs Agent vs Skill

**Use Command when:**

- User wants explicit control over when it runs
- Simple, deterministic operation
- Wrapping a bash script or tool sequence
- "I want to type `/something` to make X happen"

**Use Agent when:**

- Want autonomous delegation based on context
- Need isolated context window
- Require specific tool restrictions
- Complex decision-making involved

**Use Skill when:**

- Multiple contexts need the same knowledge
- Substantial procedural expertise
- Progressive disclosure would save tokens

## Best Practices (Opinionated Guidance)

### Delegation Pattern

Most robust commands delegate to specialized agents rather than implementing complex logic:

```markdown
---
description: Run full test suite and analyze failures
---

Use the test-runner agent to execute all tests and provide detailed failure analysis.
```

**Why this works:**

- Keeps command simple and focused
- Leverages specialized agent capabilities
- Avoids reimplementing logic
- Agent gets isolated context for complex work

**When to use:** Any command that needs file reading/parsing, complex decision trees, error recovery logic, or multi-step state management.

### Tool Restriction Pattern

For simple, deterministic operations, restrict tools for security and clarity:

```markdown
---
description: Show git status
allowed-tools: Bash(git status:*)
model: haiku
---

Run `git status` and display the output.
```

**Benefits:**

- Fast execution (haiku model)
- Restricted permissions
- Clear, single-purpose command

### Simple Sequential Pattern

**Commands CAN handle sequential bash operations** when they're straightforward and don't require file inspection or complex parsing:

```markdown
---
description: Install GitHub CLI if not present
allowed-tools: Bash
model: haiku
---

Check if gh CLI is installed. If not, provide installation instructions for the user's platform.

Simple workflow:
1. Check: `which gh` or `command -v gh`
2. If not found, provide platform-specific install guidance
3. Verify with `gh --version` if installed
4. Output success message or next steps
```

**This pattern is OK in commands when you have:**

✅ **3-5 sequential bash steps** - Simple linear workflow
✅ **Basic conditionals** - Simple if/else (installed vs not installed)
✅ **Simple verification** - Exit codes, command success/failure
✅ **User-facing instructions** - Output guidance, next steps

**When to keep it in a command:**

- Checking if a tool is installed (`which`, `command -v`)
- Installing via package manager (`brew install`, `apt-get install`)
- Running simple verification (`--version`, `status` checks)
- Providing user instructions based on results
- Linear workflows without branching complexity

**Rule of thumb:** If you can write it as 3-5 bash commands with simple if/else logic and no file reading, keep it in the command.

**Delegate to an agent when you need:**

❌ **File reading/parsing** - Requires Read, Grep, or complex text processing
❌ **Complex decision trees** - Framework detection, config file parsing, multi-path logic
❌ **Error recovery logic** - Retries, fallbacks, multiple failure modes
❌ **State management** - Tracking across multiple steps, rollback capability
❌ **Multiple tool orchestration** - Coordinating Read + Grep + Write + Bash

**Example requiring agent delegation:**

```markdown
# ❌ Too complex for command - needs agent
---
description: Set up test environment
---

Detect test framework by:
1. Read package.json, check for jest/mocha/vitest dependencies
2. Read test config files (.jestrc, mocha.opts, vitest.config.ts)
3. Scan for existing test files in src/, tests/, __tests__/
4. Parse configuration to determine coverage settings
5. Install missing dependencies based on framework
6. Generate framework-specific config if missing
7. Create example test files following detected patterns
8. Verify setup with test run
```

**Why this needs an agent:**

- Requires Read tool for multiple files
- Complex decision tree (framework detection)
- Config file parsing
- State management across steps
- Multiple failure modes to handle
- Error recovery (config generation, dependency installation)

**Better approach:**

```markdown
---
description: Set up test environment for current project
---

Use the test-setup agent to detect the test framework, install dependencies, and configure the testing environment.
```

**The threshold:**

- **Commands:** `which gh && gh --version || echo "Install with: brew install gh"`
- **Agents:** Anything requiring Read/Grep/Parse or complex multi-step decision-making

### Generation Pattern

For creating files/code, be specific about structure and requirements:

```markdown
---
description: Create a new React component with TypeScript
argument-hint: component-name
---

Create a new React component named `$1` in the components directory.

Include:
- TypeScript interface for props
- Basic component structure with proper typing
- Export statement
- Test file in __tests__ directory

Follow project conventions for imports and file structure.
```

## Common Pitfalls (Best Practices)

### Pitfall #1: Knowledge Storage in Commands

**Problem:** Using commands to store documentation instead of actions

**Example of wrong pattern:**

```markdown
---
description: Show API documentation standards
---

Our API documentation standards:
[50 lines of guidelines...]
```

**Why it's wrong:** This is knowledge, not an action. Commands should DO things.

**Better approach:** Create a skill for standards, command for action:

```markdown
---
description: Generate API documentation for current file
---

Use the api-documentation skill to generate comprehensive API docs for the current file.
```

### Pitfall #2: Reimplementing Agent Logic

**Problem:** Commands with complex logic that agents handle better

**Example of wrong pattern:**

```markdown
---
description: Run tests
---

First, scan for test files in src/, tests/, and __tests__.
Then determine the test framework by checking package.json.
If Jest, run `npm test`. If pytest, run `pytest -v`.
Parse the output for failures and categorize by severity...
```

**Why it's wrong:** Too much logic, too many decisions, better in isolated context.

**Better approach:**

```markdown
---
description: Run full test suite
---

Use the test-runner agent to execute the full test suite and analyze failures.
```

### Pitfall #3: Overly Complex Arguments

**Problem:** Arguments that need extensive parsing or validation

**Example of questionable pattern:**

```markdown
/deploy env=staging branch=main force=true rollback=false
```

**Why it's questionable:** No argument validation, no type checking, brittle parsing.

**Better approach:** Keep arguments simple, let agent handle complexity:

```markdown
---
description: Deploy to specified environment
argument-hint: environment
---

Deploy to $1 environment. The deployer agent will handle validation, rollback strategy, and confirmation.
```

### Pitfall #4: Scope Creep

**Problem:** Single command tries to do too much

**Example:**

```markdown
description: Test, lint, format, commit, and deploy
```

**Why it fails:** Multiple distinct operations with different failure modes.

**Better:** Separate commands or orchestrator agent that coordinates multiple specialized agents.

## Command Quality Checklist

Before finalizing a command:

**Structure (from official docs):**

- ✓ Valid YAML frontmatter (if used)
- ✓ Proper markdown formatting
- ✓ Filename is kebab-case (becomes command name)

**Best Practices (opinionated):**

- ✓ Includes `description` field for discoverability
- ✓ Uses `argument-hint` if arguments expected
- ✓ Action-oriented (not knowledge storage)
- ✓ Delegates to agents for complex logic (file parsing, decision trees, error recovery)
- ✓ Simple sequential bash is OK (3-5 steps, basic if/else)
- ✓ Arguments are simple (if present)
- ✓ Clear, single-purpose design
- ✓ Appropriate tool restrictions (if needed)
- ✓ Model choice matches complexity (haiku for simple, sonnet for complex)

## Path Resolution

**Official locations:**

- **Project-level:** `.claude/commands/` (shared with team)
- **User-level:** `~/.claude/commands/` (personal, all projects)
- **Plugin context:** `plugins/[name]/commands/` (when creating plugin commands)

**Resolution logic:**

1. If caller specifies exact path → use that
2. If in plugin context → use `plugins/[name]/commands/`
3. Default → `.claude/commands/` (project-level)
4. User-level → only when explicitly requested

## Name Normalization

Command names must be kebab-case (filename without .md extension):

**Transform these:**

- "Run Tests" → `run-tests.md`
- "create_component" → `create-component.md`
- "DeployStaging" → `deploy-staging.md`

## Example: Good Command Design

**Before (from hypothetical docs):**

```markdown
---
description: Create component
---

Create a new component.
```

**Issues:**

- ❌ Description too vague
- ❌ Prompt lacks specifics
- ❌ No argument handling when clearly needed
- ❌ No guidance on structure

**After (applying best practices):**

```markdown
---
description: Create a new React component with TypeScript and tests
argument-hint: component-name
---

Create a new React component named `$1`.

Requirements:
- Location: src/components/$1/$1.tsx
- TypeScript interface for props
- Proper exports (default and named)
- Test file: src/components/$1/__tests__/$1.test.tsx
- Storybook file: src/components/$1/$1.stories.tsx

Follow project conventions:
- Use existing component patterns as reference
- Include JSDoc comments
- Export types separately
```

**Improvements:**

- ✅ Specific description (React + TypeScript + tests)
- ✅ Clear argument placeholder and hint
- ✅ Detailed deliverables listed
- ✅ References project conventions
- ✅ Actionable and unambiguous

## Documentation References

These are the authoritative sources. Fetch them before creating commands:

**Core specifications:**

- https://code.claude.com/docs/en/slash-commands.md - Command structure, examples, patterns

**Tool verification:**

- https://code.claude.com/docs/en/settings#tools-available-to-claude - Current tool list

**Model selection:**

- https://code.claude.com/docs/en/model-config.md - Model guidance

**Remember:** Official docs provide structure and features. This skill provides best practices and patterns for creating excellent commands.
