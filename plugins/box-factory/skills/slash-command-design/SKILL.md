---
name: slash-command-design
description: Interpretive guidance for designing Claude Code slash commands. Helps you apply official documentation effectively and create high-quality commands. Use when creating or reviewing slash commands.
---

# Slash Command Design

This skill provides interpretive guidance and best practices for creating Claude Code slash commands. It helps you understand how to create excellent commands.

## Workflow Selection

| If you need to...                                                            | Go to...                                                         |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Understand command vs agent vs skill (when to use each component type)       | [Decision Framework](#decision-framework)                        |
| See basic command structure (quick reference for creating commands)          | [Quick Start](#quick-start)                                      |
| Learn frontmatter fields (official specification)                            | [Frontmatter Fields](#frontmatter-fields-official-specification) |
| Use arguments in commands (positional vs all-arguments patterns)             | [argument-patterns.md](argument-patterns.md)                     |
| Execute bash or reference files (! prefix, @ prefix, tool restrictions)      | [advanced-features.md](advanced-features.md)                     |
| Decide delegation vs direct implementation (when to use agents vs commands)  | [Best Practices](#best-practices-opinionated-guidance)           |
| Avoid common mistakes (anti-patterns catalog with symptoms and fixes)        | [common-pitfalls.md](common-pitfalls.md)                         |
| Validate before completing (final checklist before creating command)         | [Quality Checklist](#quality-checklist)                          |
| Determine where to create command files (project vs user vs plugin contexts) | [Path Resolution](#path-resolution)                              |

## Quick Start

Create a command at `.claude/commands/my-command.md`:

```markdown
---
description: Brief description of what this command does
argument-hint: expected-args
---

Command prompt content here.
Use $1, $2 for individual arguments or $ARGUMENTS for all.
```

**Delegation pattern (recommended for complex tasks):**

```markdown
---
description: Run full test suite and analyze failures
---

Use the test-runner agent to execute all tests and provide detailed failure analysis.
```

## Official Documentation

**Claude Code changes rapidly and is post-training knowledge.** Fetch these docs when creating commands to ensure current syntax:

- **<https://code.claude.com/docs/en/slash-commands.md>** - Core specification and examples
- **<https://code.claude.com/docs/en/settings#tools-available-to-claude>** - Verify tool names

## Core Understanding

### Commands Are User-Triggered, Not Autonomous

**Key distinction:**

- **Commands** = User explicitly invokes with `/command-name`
- **Agents** = Claude autonomously delegates based on context
- **Skills** = Knowledge that loads when relevant

**Quality test:** If you want this to happen automatically based on context, it's an agent, not a command.

### Command Structure (Official Specification)

Commands are Markdown files with optional YAML frontmatter:

```markdown
---
description: Brief description (optional, defaults to first line)
argument-hint: [expected-args]
allowed-tools: Tool1, Tool2
disable-model-invocation: false
---

Command prompt content goes here.
Use $1, $2 for individual arguments or $ARGUMENTS for all.
```

## Frontmatter Fields (Official Specification)

All fields are optional:

| Field                      | Purpose                                             | Default                    |
| -------------------------- | --------------------------------------------------- | -------------------------- |
| `description`              | Brief command description for `/help`               | First line of prompt       |
| `argument-hint`            | Expected arguments (e.g., `[pr-number] [priority]`) | None                       |
| `allowed-tools`            | Restrict to specific tools (e.g., `Bash(git:*)`)    | Inherits from conversation |
| `disable-model-invocation` | Prevents SlashCommand tool from auto-invoking       | false                      |

**Best practice:** Always include `description` even though it's optional - improves discoverability and Claude's ability to use the SlashCommand tool.

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

**Deep dive:** [Choosing the Right Component](../box-factory-architecture/components/choosing-the-right-component.md) - Full decision framework with KEY CHARACTERISTIC, CHOOSE IF, DO NOT CHOOSE IF sections for all component types. **Traverse when:** ambiguous component choice, need to map user intent phrases to component type, edge cases not covered by summary. **Skip when:** summary above clearly answers the question.

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
---

Run `git status` and display the output.
```

**Benefits:**

- Restricted permissions
- Clear, single-purpose command

**Deep dive:** [Advanced Features - Tool Restriction](advanced-features.md#tool-restriction-official-specification) - When to use tool restrictions, common patterns, security implications. **Traverse when:** need to restrict command permissions, creating security-sensitive commands. **Skip when:** command delegates to agent or needs full tool access.

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

## Quality Checklist

Before finalizing a command:

**Structure (from official docs):**

- [ ] Valid YAML frontmatter (if used)
- [ ] Proper markdown formatting
- [ ] Filename is kebab-case (becomes command name)

**Best Practices (opinionated):**

- [ ] Includes `description` field for discoverability
- [ ] Uses `argument-hint` if arguments expected
- [ ] Action-oriented (not knowledge storage)
- [ ] Delegates to agents for complex logic (file parsing, decision trees, error recovery)
- [ ] Arguments are simple (if present)
- [ ] Clear, single-purpose design
- [ ] Appropriate tool restrictions (if needed)
