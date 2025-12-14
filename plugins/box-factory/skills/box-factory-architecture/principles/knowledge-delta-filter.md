# Knowledge Delta Filter

The most important principle for Box Factory content: **only document what Claude doesn't already know**.

## Why This Matters

Claude's training includes extensive knowledge of common development tools, standard workflows, well-established frameworks, and general best practices. Content that duplicates this base knowledge wastes tokens and creates maintenance burden without adding value.

**Box Factory components document the DELTA** - the difference between Claude's base knowledge and what Claude needs to know for your specific context.

This applies everywhere Claude reads your content:

- **Skills** - Guidance and interpretive knowledge
- **Agents** - Prompts and descriptions
- **Commands** - Prompt templates and instructions
- **Hooks** - Comments, error messages, validation logic
- **CLAUDE.md** - Project and plugin guidelines
- **README.md** - User-facing documentation

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

Before including content in any Box Factory component, ask:

| Question                                           | If Yes               | If No               |
| -------------------------------------------------- | -------------------- | ------------------- |
| Would Claude get this wrong without this content?  | Include (fills gap)  | Exclude (redundant) |
| Is this specific to this user/project/context?     | Include (contextual) | Probably exclude    |
| Is this well-documented in Claude's training data? | Exclude (standard)   | Include (new/edge)  |
| Would this information change Claude's behavior?   | Include (corrective) | Exclude (no impact) |

## Examples

### Skill: Git Workflow

**Bad (Includes Base Knowledge):**

```text
480 lines including:
- How to use git status, git diff, git commit
- Basic branching operations
- Standard commit message formats
- Common git commands
```

Result: 95% redundant, 5% valuable

**Good (Only Includes Delta):**

```text
~80 lines including:
- User's specific commit format preferences
- Edge case: pre-commit hook retry logic
- User requirement: no attribution text
```

Result: 100% valuable, focused on what Claude doesn't know

### Agent Description

**Bad (Includes Base Knowledge):**

```text
Agent that helps with git operations. Can run git status, git commit,
git push. Understands branching and merging. Follows best practices
for version control.
```

Result: 100% redundant - Claude already knows git

**Good (Only Includes Delta):**

```text
Commits using user's format: terse single-line, no emojis, no attribution.
Retries with --amend when pre-commit hooks modify files.
```

Result: 100% valuable - user-specific behavior Claude would miss

### CLAUDE.md

**Bad (Includes Base Knowledge):**

```markdown
Use git for version control. Write tests before committing.
Follow coding standards. Use meaningful variable names.
```

Result: Generic advice Claude already follows

**Good (Only Includes Delta):**

```markdown
Run `git pub` instead of `git push` (alias that sets upstream).
Scripts use UV inline metadata (PEP 723) - see uv-scripts skill.
```

Result: Project-specific patterns Claude would miss

### Command Prompt

**Bad (Includes Base Knowledge):**

```markdown
Create a pull request. PRs should have clear descriptions explaining
what changed and why. Include any relevant context for reviewers.
```

Result: Standard PR advice Claude knows

**Good (Only Includes Delta):**

```markdown
Create PR with Problem/Solution format. NEVER add Claude attribution.
```

Result: User-specific requirements Claude wouldn't assume

## The Delta Principle

Components should only contain knowledge that bridges the gap between what Claude knows and what Claude needs to know for this specific context.

**Target:** Focused, high-value delta knowledge - not comprehensive documentation of things Claude already knows.
