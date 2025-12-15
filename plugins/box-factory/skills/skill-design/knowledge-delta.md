# Skill Design: Knowledge Delta Filter

The most important principle for skill content: **only document what Claude doesn't already know**.

## Quick Reference

| Topic                                                      | Description                                           |
| ---------------------------------------------------------- | ----------------------------------------------------- |
| [Why This Matters](#why-this-matters)                      | Token waste and maintenance burden                    |
| [What to Include](#what-to-include-the-delta)              | User preferences, edge cases, decision frameworks     |
| [What to Exclude](#what-to-exclude-claude-already-knows)   | Basic commands, standard workflows, general practices |
| [Decision Test](#decision-test)                            | Question framework for content decisions              |
| [Example: Git Workflow Skill](#example-git-workflow-skill) | Before/after comparison                               |

## Why This Matters

Claude's training includes extensive knowledge of common development tools, standard workflows, well-established frameworks, and general best practices. Skills that duplicate this base knowledge waste tokens and create maintenance burden without adding value.

**Skills document the DELTA** - the difference between Claude's base knowledge and what Claude needs to know for your specific context.

## What to Include (The Delta)

### User-Specific Preferences and Conventions

- "This user wants commit messages terse, single-line, no emojis, no attribution"
- "This team uses specific naming conventions not found in standard docs"
- "This project requires custom workflow steps"
- Example: User's preference for no "Generated with Claude Code" messages

### Edge Cases and Gotchas Claude Would Miss

- "Pre-commit hooks that modify files require retry with --amend"
- "This API has undocumented rate limiting behavior"
- "File system paths need special escaping in this environment"
- Example: Specific retry logic for linter hooks that auto-fix

### Decision Frameworks for Ambiguous Situations

- "When to use gh CLI vs GitHub MCP server in this project"
- "Tool selection hierarchy when multiple options exist"
- "Which pattern to prefer when standards conflict"
- Example: Prefer gh CLI when available, fall back to MCP

### Things Claude Gets Wrong Without Guidance

- "Claude invents unsupported frontmatter in slash commands"
- "Claude uses deprecated syntax for Tool X without this guidance"
- "Claude doesn't know about this project-specific integration pattern"
- Example: Claude making up `skills: git-workflow` frontmatter that doesn't exist

### New or Rapidly-Changing Technology (Post-Training)

- Claude Code itself (released after training cutoff)
- New framework versions with breaking changes
- Emerging tools not well-represented in training data
- Example: Claude Code plugin system specifics

### Integration Patterns Between Tools (Project-Specific)

- "How this project connects Tool A with Tool B"
- "Custom workflow orchestration"
- "Project-specific toolchain configuration"
- Example: Using both gh CLI and GitHub MCP server in same plugin

## What to Exclude (Claude Already Knows)

### Basic Commands for Well-Known Tools

- Don't document: git status, git commit, git push, git diff
- Don't document: npm install, pip install, docker run
- Don't document: Standard CLI flags and options Claude knows
- Claude learned this in training and doesn't need reminders

### Standard Workflows Claude Knows

- Don't document: Basic git branching workflow
- Don't document: Standard PR review process
- Don't document: Common testing patterns
- These are well-established practices in Claude's training

### General Best Practices (Not Project-Specific)

- Don't document: "Write clear commit messages"
- Don't document: "Test your code before committing"
- Don't document: "Use semantic versioning"
- Claude already knows these principles

### Well-Established Patterns for Common Tools

- Don't document: REST API design basics
- Don't document: Standard design patterns (MVC, etc.)
- Don't document: Common security practices Claude knows
- Training data covers these extensively

## Decision Test

Before including content in a skill, ask:

| Question                                           | If Yes               | If No               |
| -------------------------------------------------- | -------------------- | ------------------- |
| Would Claude get this wrong without the skill?     | Include (fills gap)  | Exclude (redundant) |
| Is this specific to this user/project/context?     | Include (contextual) | Probably exclude    |
| Is this well-documented in Claude's training data? | Exclude (standard)   | Include (new/edge)  |
| Would this information change Claude's behavior?   | Include (corrective) | Exclude (no impact) |

## Example: Git Workflow Skill

### Bad (Includes Base Knowledge)

```text
480 lines including:
- How to use git status, git diff, git commit
- Basic branching operations
- Standard commit message formats
- Common git commands
```

**Result:** 95% redundant, 5% valuable

### Good (Only Includes Delta)

```text
~80 lines including:
- User's specific commit format preferences
- Edge case: pre-commit hook retry logic
- User requirement: no attribution text
```

**Result:** 100% valuable, focused on what Claude doesn't know

## The Delta Principle

Skills should only contain knowledge that bridges the gap between what Claude knows and what Claude needs to know for this specific context.

**Target size:** ~50-150 lines of delta knowledge, not ~500 lines of redundant documentation.
