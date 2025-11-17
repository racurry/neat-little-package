# Forge

A comprehensive toolkit for creating and managing all Claude Code components: agents, commands, plugins, skills, and hooks. Forge provides powerful commands and expert guidance to streamline your development workflow, whether you're building a complete plugin or adding individual components to existing ones.

## Features

### Commands

Forge provides commands for creating, validating, and reviewing all Claude Code component types:

#### `/add-plugin`

Create a new Claude Code plugin with complete scaffolding. Delegates to the plugin-writer agent.

**Usage:** `/add-plugin`

#### `/add-agent`

Add a new agent to a plugin. Delegates to the agent-writer agent.

**Usage:** `/add-agent`

#### `/add-command`

Add a new slash command to a plugin. Delegates to the slash-command-writer agent.

**Usage:** `/add-command`

#### `/add-skill`

Add a new skill to a plugin. Delegates to the skill-writer agent.

**Usage:** `/add-skill`

#### `/add-hook`

Add a new hook to a plugin. Delegates to the hooks-writer agent.

**Usage:** `/add-hook`

#### `/validate-plugin`

Validate a plugin's structure and components against official specs and best practices. Delegates to the validation-agent.

**Usage:** `/validate-plugin [plugin-path]`

#### `/review-component`

Review a component (agent, command, skill, hook) for quality and best practices. Delegates to the component-reviewer agent.

**Usage:** `/review-component [component-path]`

### Agents

Forge includes specialized agents that handle component creation and quality assurance:

#### Writer Agents

**plugin-writer** - Creates complete plugins with scaffolding, delegates to other writers
**agent-writer** - Creates agents following agent-design patterns
**slash-command-writer** - Creates commands following slash-command-design patterns
**skill-writer** - Creates skills following skill-design patterns
**hooks-writer** - Creates hooks following hooks-design patterns

#### Quality Agents

**validation-agent** - Validates plugins and components (read-only)
**component-reviewer** - Reviews components for quality (read-only)

### Skills

Forge includes comprehensive design guidance skills that help you create high-quality Claude Code components:

#### `agent-design`

Interpretive guidance for designing Claude Code agents and subagents.

**What it provides:**

- Agent architecture understanding (isolated context, no user interaction)
- Critical gotchas and common mistakes
- Tool selection philosophy
- Description field design for autonomous delegation
- Validation workflow

**When to use:**

- Creating or reviewing agents
- Understanding when to use agents vs other patterns
- Ensuring agents follow best practices

#### `slash-command-design`

Interpretive guidance for designing Claude Code slash commands.

**What it provides:**

- Command vs agent vs skill decision framework
- Argument syntax and best practices
- Advanced features (bash execution, file references, namespacing)
- Delegation patterns (commands that invoke agents)
- Common pitfalls and how to avoid them

**When to use:**

- Creating or reviewing slash commands
- Deciding between command and other patterns
- Understanding command-specific features

#### `plugin-design`

Interpretive guidance for designing Claude Code plugins.

**What it provides:**

- Plugin architecture understanding (packaging, not functionality)
- Critical directory structure rules
- Marketplace distribution strategies
- Development workflow best practices
- Version management and semantic versioning

**When to use:**

- Creating or reviewing plugins
- Understanding marketplace distribution
- Planning multi-component packages

#### `hooks-design`

Interpretive guidance for designing Claude Code hooks.

**What it provides:**

- Hook lifecycle and architecture
- Exit code communication patterns
- Security considerations
- Event-specific usage patterns
- stdin/stdout handling

**When to use:**

- Creating or reviewing hooks
- Understanding deterministic control flow
- Implementing guaranteed execution patterns

#### `skill-design`

Meta-skill that teaches how to design skills following Forge philosophy.

**What it provides:**

- Forge philosophy (low-maintenance, fetch-first, two-layer approach)
- When to create skills vs agents vs commands
- Structure for progressive disclosure
- Evidence-based recommendations
- Quality checklist and anti-patterns

**When to use:**

- Creating or reviewing skills
- Understanding skill architecture
- Learning Forge design principles

## Design Philosophy

Forge follows a specific philosophy for creating maintainable, high-quality Claude Code components:

### Low-Maintenance by Design

**Skills should:**

- Defer all specific syntax and requirements to official documentation via WebFetch
- Focus on interpretation and best practices, not duplication
- Avoid hardcoding version-specific details (model names, tool lists)
- Remain valid as Claude Code evolves

**Why:** Documentation changes, but design principles and gotchas remain constant.

### Official Specs + Opinionated Guidance

**The two-layer approach:**

1. **Official Specification** - Always fetch current docs, cite them clearly
2. **Best Practices** - Add interpretive guidance the docs don't emphasize

**Example:** Docs say "description field for commands." Best practice says "always include description even though it's optional - improves discoverability."

### Evidence-Based Recommendations

**All claims should be:**

- Grounded in official documentation, or
- Clearly marked as opinionated best practices, or
- Based on common pitfalls and real-world experience

**Avoid:** Presenting opinions as official requirements or making unsupported claims.

## When to Create What

Understanding when to use each component type is critical for good architecture.

### Skill vs Agent vs Command vs Hook

**Use a Skill when:**

- Multiple contexts need the same knowledge
- Substantial procedural expertise that's reusable
- Progressive disclosure would save tokens
- Providing interpretive guidance
- You want to teach "how to think about" something

**Examples:**

- `agent-design` - Teaches how to design agents
- `api-documentation-standards` - Reusable formatting rules
- `testing-strategy` - Methodologies applicable across projects

**Use an Agent when:**

- Need isolated context (won't pollute main conversation)
- Want autonomous delegation (triggered by context)
- Complex decision-making or analysis involved
- Task runs as part of larger workflows
- Require specific tool restrictions

**Examples:**

- `test-runner` - Execute tests and analyze failures
- `code-reviewer` - Security and quality analysis
- `doc-generator` - Generate API documentation

**Use a Command when:**

- User wants explicit control over when it runs
- Simple, deterministic operation
- Wrapping a bash script or tool sequence
- One-off operations triggered by user
- "I want to type `/something` to make X happen"

**Examples:**

- `/deploy` - Explicit deployment trigger
- `/create-component` - User-initiated file generation
- `/git-commit` - Controlled git operations

**Use a Hook when:**

- Need guaranteed execution every time (deterministic)
- Simple, deterministic rule (format, lint, validate)
- Integrating with external tools
- Performance/safety enforcement
- Must happen at specific lifecycle event

**Examples:**

- PostToolUse formatter - Always format after writes
- PreToolUse security check - Always validate bash commands
- SessionStart context loader - Always inject project guidelines

### Detailed Decision Trees

#### "I want to enforce something always happens"

→ **Hook** (deterministic, guaranteed execution)

**Example:** Always run prettier after file edits

#### "I want Claude to intelligently handle something"

→ **Agent** (isolated context, autonomous delegation)

**Example:** Analyze test failures and suggest fixes

#### "I want reusable knowledge/guidelines"

→ **Skill** (knowledge that loads when relevant)

**Example:** API documentation standards

#### "I want the user to trigger something"

→ **Command** (explicit user control)

**Example:** Deploy to production

#### "I need to package multiple related components"

→ **Plugin** (distribution mechanism)

**Example:** Complete testing suite with runner agent, test command, and testing skill

## Installation

### From the Marketplace

1. Add the marketplace (if not already added):

   ```
   /plugin marketplace add /Users/aaron/workspace/infra/claude-marketplace
   ```

2. Install the plugin:

   ```
   /plugin install forge@my-claude-plugins
   ```

3. Start creating components!

## Quick Start Guide

### Creating Your First Plugin

1. Run `/add-plugin`
2. The plugin-writer agent will guide you through:
   - Plugin name and metadata
   - Initial components to include
   - Directory structure creation
3. Plugin is created with proper structure, README, and plugin.json
4. Install and test your new plugin

### Adding Features to Existing Plugins

**Add a command:**

```
/add-command
```

Then follow the prompts.

**Add a skill:**

```
/add-skill
```

Then follow the prompts.

### Getting Design Guidance

Use the design skills for expert guidance:

- **agent-design** - Creating agents and subagents
- **slash-command-design** - Creating slash commands
- **plugin-design** - Creating and distributing plugins
- **hooks-design** - Creating lifecycle hooks
- **skill-design** - Creating skills with Forge philosophy

These skills will:

1. Fetch current official documentation
2. Provide interpretive guidance
3. Identify common pitfalls
4. Suggest best practices

## Component Design Best Practices

### Skills

**Do:**

- Fetch official docs with WebFetch every time
- Focus on interpretation, not duplication
- Distinguish official specs from best practices
- Avoid hardcoding version-specific information
- Mark opinionated guidance clearly
- Provide decision frameworks and gotchas

**Don't:**

- Duplicate official documentation
- Hardcode model names, tool lists, or syntax
- Present opinions as official requirements
- Make unsupported claims
- Create overlapping skills

**Philosophy:**
Skills should be a lens for reading official docs effectively, not a replacement for them.

### Agents

**Do:**

- Design for isolated context (no user interaction)
- Grant tools matching autonomous responsibilities
- Use directive description language for delegation
- Define single, focused responsibility
- Include clear constraints
- Test that delegation triggers work

**Don't:**

- Include user interaction language ("ask the user")
- Over-restrict tools (agent can't do its job)
- Create overly broad scope (one agent, many jobs)
- Hardcode version-specific details

**Key insight:**
Agents can't ask questions but should do actual work autonomously.

### Commands

**Do:**

- Keep action-oriented (not knowledge storage)
- Delegate to agents for complex logic
- Use simple arguments or let agents handle complexity
- Include description for discoverability
- Leverage advanced features (bash `!`, file `@`)

**Don't:**

- Store knowledge in commands (use skills)
- Reimplement agent logic
- Create overly complex arguments
- Skip the description field

**Key insight:**
Most robust commands delegate to specialized agents.

### Hooks

**Do:**

- Keep fast (< 60s or set custom timeout)
- Use exit 2 only for critical blocking
- Quote all variables
- Validate and sanitize inputs
- Test in safe environments first
- Include clear error messages

**Don't:**

- Block everything with aggressive matchers
- Create slow hooks without custom timeouts
- Assume user interaction
- Ignore security (path traversal, etc.)
- Forget to handle errors gracefully

**Key insight:**
Hooks execute automatically on every event - they must be fast, safe, and reliable.

### General

**Do:**

- Version plugins semantically (1.0.0 → 1.1.0 → 2.0.0)
- Document everything in README files
- Test thoroughly after changes
- Use lowercase, hyphenated names
- Keep JSON files properly formatted
- Reference official docs for current details

**Don't:**

- Make breaking changes without bumping major version
- Skip documentation
- Use spaces or special characters in names
- Commit without testing
- Hardcode details that will become outdated

## Development Workflow

### Iterative Development

1. Create or modify plugin files
2. Uninstall the plugin:

   ```
   /plugin uninstall [plugin-name]@my-claude-plugins
   ```

3. Reinstall the plugin:

   ```
   /plugin install [plugin-name]@my-claude-plugins
   ```

4. Test the changes
5. Repeat as needed

### Testing Components

**Commands:**

```
/[command-name]
```

Verify it behaves as expected.

**Skills:**

1. Use the Skill tool
2. Select your skill
3. Test it in various scenarios
4. Refine SKILL.md as needed

**Agents:**

Reference the agent in prompts or let delegation trigger it, then verify behavior.

**Hooks:**

Make a change that triggers the hook event, press CTRL-R to view execution.

## File Structure Reference

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin metadata
├── commands/                # Optional: Slash commands
│   ├── command1.md
│   └── command2.md
├── skills/                  # Optional: Agent skills
│   ├── skill1/
│   │   └── SKILL.md
│   └── skill2/
│       └── SKILL.md
├── agents/                  # Optional: Custom agents
│   ├── agent1.md
│   └── agent2.md
├── hooks/                   # Optional: Event handlers
│   └── hooks.json
└── README.md               # Recommended: Documentation
```

**Critical:** All component directories must be at plugin root, NOT inside `.claude-plugin/`.

## Troubleshooting

### Plugin not showing up

- Verify plugin.json is valid JSON
- Check that plugin is registered in marketplace.json
- Try removing and re-adding the marketplace
- Ensure directory structure is correct (components at root)

### Command not working

- Ensure command file is in `commands/` directory
- Check that filename matches command name (kebab-case)
- Verify YAML frontmatter is properly formatted
- Reinstall the plugin
- Check `/help` to see if command appears

### Skill not recognized

- Verify SKILL.md exists in `skills/[skill-name]/` directory
- Check YAML frontmatter formatting
- Ensure skill directory name is lowercase, hyphenated
- Reinstall the plugin
- Use Skill tool to verify it appears in list

### Agent not being invoked

- Check description field uses directive language
- Verify agent file is in `agents/` directory
- Ensure tools list matches agent's responsibilities
- Look for user interaction language (forbidden)
- Test by explicitly requesting the agent

### Hook not firing

- Verify hooks configuration in settings.json
- Review and approve hooks via `/hooks` menu
- Check matcher syntax (case-sensitive)
- Press CTRL-R to view hook execution logs
- Ensure hook exits properly (exit 0, 2, or other)

### Changes not taking effect

- Always reinstall the plugin after making changes
- Check for syntax errors in JSON/markdown files
- Verify file paths are correct
- Restart Claude Code if needed

## Examples

### Example plugin.json

```json
{
  "name": "my-plugin",
  "description": "A helpful plugin for my workflow",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "keywords": ["productivity", "automation"]
}
```

### Example Command File

`commands/deploy.md`:

```markdown
---
description: Deploy the application to production
argument-hint: environment
---

Deploy to the $1 environment.

Use the deployment agent to handle:
- Pre-deployment validation
- Build process
- Deployment execution
- Post-deployment verification
- Rollback strategy if needed
```

### Example Skill File

`skills/api-standards/SKILL.md`:

```markdown
---
name: api-standards
description: Guidelines for designing and documenting REST APIs following team standards
---

# API Standards Skill

When designing or documenting APIs, follow these team standards:

## Endpoint Naming

- Use plural nouns: `/users`, `/products`
- Use kebab-case for multi-word resources: `/user-profiles`
- Avoid verbs in URLs (use HTTP methods)

## Response Format

All responses should follow:

```json
{
  "data": { ... },
  "meta": {
    "timestamp": "ISO8601",
    "version": "v1"
  }
}
```

## Documentation Requirements

Each endpoint must document:

- Purpose and use case
- Request parameters with types
- Response schema with examples
- Error codes and meanings
- Authentication requirements

```

### Example Agent File

`agents/test-runner.md`:

```markdown
---
name: test-runner
description: ALWAYS use when test suites need execution and failures require analysis. Use proactively when encountering test-related errors.
tools: Bash, Read, Grep
model: haiku
---

# Test Runner Agent

You execute and analyze test results.

## Process

1. Run the requested test suite using Bash
2. Parse output for failures using Grep
3. Read relevant source/test files
4. Provide concise failure summary with file:line references

## Constraints

- Never modify code; only analyze and report findings
- Only run tests, never build or deploy commands
- Keep summaries focused on actionable items
```

### Example Hook Configuration

`hooks/hooks.json`:

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "prettier --write \"$CLAUDE_FILE_PATHS\" 2>/dev/null || true",
          "timeout": 30
        }
      ]
    }
  ],
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/security-check.sh"
        }
      ]
    }
  ]
}
```

## Resources

### Official Documentation

Always fetch current documentation:

- **Plugins**: <https://code.claude.com/docs/en/plugins>
- **Slash Commands**: <https://code.claude.com/docs/en/slash-commands>
- **Agents**: <https://code.claude.com/docs/en/sub-agents>
- **Hooks**: <https://code.claude.com/docs/en/hooks>
- **Skills**: Part of agent documentation

### Design Skills (Included in Forge)

Use these skills for expert guidance:

- `agent-design` - Agent and subagent design
- `slash-command-design` - Command design and best practices
- `plugin-design` - Plugin architecture and distribution
- `hooks-design` - Hook lifecycle and patterns
- `skill-design` - Skill creation following Forge philosophy

**Design Philosophy:**

- Low-maintenance: Defer to official docs via WebFetch, avoid hardcoding
- Two-layer approach: Official specs + opinionated guidance
- Evidence-based: All recommendations grounded in docs or clearly marked as opinions
- Delegation pattern: Commands delegate to specialized agents that follow design skills

## TODO

- [ ] Add a command to update docs.  README, CLAUDE.md
