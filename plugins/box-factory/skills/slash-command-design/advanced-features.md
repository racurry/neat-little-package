# Advanced Features

This document covers advanced slash command features from the official specification.

## Bash Execution with `!` Prefix (Official Specification)

Execute bash commands before the prompt runs:

```markdown
---
allowed-tools: Bash(git:*)
---

!git status

Review the git status above and suggest next steps.
```

### When to Use

**Good for:**

- Quick status checks before analysis (`!git status`, `!npm test`)
- Gathering context for Claude's response
- Running read-only commands that inform the prompt

**Avoid for:**

- Complex bash logic (delegate to agent instead)
- Write operations without confirmation
- Multi-step conditional workflows

## File References with `@` Prefix (Official Specification)

Include file contents in the prompt:

```markdown
Review @src/utils/helpers.js for potential improvements.
```

Multiple files: `Compare @src/old.js with @src/new.js`

### When to Use

**Good for:**

- Simple file review tasks
- Direct comparison of specific files
- Quick analysis of known paths

**Avoid for:**

- Large files (token limits)
- Complex file analysis requiring multiple reads
- Dynamic file discovery (delegate to agent instead)

## Subdirectory Namespacing (Official Specification)

Organize commands in subdirectories:

```text
.claude/commands/frontend/component.md → /component (project:frontend)
.claude/commands/backend/endpoint.md → /endpoint (project:backend)
```

Command name comes from filename, subdirectory appears in `/help` as namespace label.

### When to Use

**Good for:**

- Large projects with distinct subsystems
- Commands specific to tech stack areas
- Avoiding command name collisions

**Avoid for:**

- Small projects (flat structure is clearer)
- Over-categorization (3-5 commands don't need subdirectories)

## Tool Restriction (Official Specification)

Restrict commands to specific tools via `allowed-tools`:

```markdown
---
description: Show git status
allowed-tools: Bash(git status:*)
---

Run `git status` and display the output.
```

### When to Use

**Good for:**

- Security-sensitive operations
- Single-purpose commands with clear scope
- Preventing accidental file modifications

**Common patterns:**

- `Bash(git:*)` - Git operations only
- `Bash(git status:*)` - Specific git command
- `Read, Grep, Glob` - Read-only file operations
- Omit field entirely to inherit conversation tools
