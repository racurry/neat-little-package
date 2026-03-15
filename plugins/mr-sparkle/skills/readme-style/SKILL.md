---
name: readme-style
description: User's README style preferences — ultra-terse, action-focused, ~20 lines. Use when writing or reviewing any README file, not just Claude Code components.
---

# README Style

User preferences and corrections for writing READMEs. Claude knows how to write READMEs; this documents what makes THIS user's style different.

## Core Philosophy

**Ultra-terse:** ~20-50 lines total, not 50-100
**Action-focused:** Show commands with inline comments, minimal prose
**No fluff:** Skip troubleshooting, file structure, version history

## Structure Pattern

````markdown
# Project Name

One-liner description.

## Overview

- What it does (bullet 1)
- What it does (bullet 2)

## Commands

Setup

```
/plugin:setup # walks through configuration
```

Main Actions

```
/plugin:do-thing # does the thing
/plugin:do-thing with args # does the thing with these args
/plugin:do-other selective stuff # does other with just the selective stuff
```
````

**Key characteristics:**

- Opening: Project name + single-line description
- Overview: 2-3 terse bullets describing what it does
- Commands: Grouped code blocks with inline `#` comments
- That's it. Nothing more.

## What to Include

**Include ONLY:**

- ✓ Project name (H1)
- ✓ One-liner description
- ✓ Terse bullet points (2-3) describing what it does
- ✓ Commands grouped by purpose (Setup, Main Actions, etc.)
- ✓ Inline `#` comments explaining each command
- ✓ Minimal section headers (just enough to group commands)

## What to EXCLUDE

**Exclude ALL of these common README elements:**

- ❌ Detailed feature descriptions
- ❌ Philosophy/design sections
- ❌ "How it works" explanations
- ❌ Workflow examples
- ❌ Troubleshooting guides
- ❌ File structure documentation
- ❌ Version history or changelog
- ❌ Resource links or references
- ❌ "Components" sections listing agents/skills
- ❌ Verbose installation instructions
- ❌ Contribution guidelines
- ❌ License information
- ❌ Prerequisites sections
- ❌ Configuration details (beyond setup command)

## Before/After Examples

### Bad (Standard README Approach)

```markdown
# Development Workflow Plugin

Comprehensive tooling for Git and GitHub workflows with intelligent automation.

## Features

This plugin provides:

- **Smart Git Operations**: Streamlined commit workflows with automatic formatting
- **GitHub Integration**: Seamless PR creation and issue management
- **Workflow Automation**: Pre-commit hooks and quality checks

## Components

### Agents

- `pr-creator` - Creates pull requests with proper formatting
- `commit-helper` - Assists with commit message formatting

### Skills

- `git-workflow` - Documents git workflow preferences
- `github-workflow` - GitHub interaction patterns

### Commands

- `/pr` - Create pull request
- `/commit` - Smart commit with formatting

## How It Works

The plugin integrates with your local git repository to provide enhanced
workflow capabilities. It uses the GitHub CLI when available and falls back
to the GitHub MCP server for API operations...

[... continues for 50+ more lines ...]
```

**Issues:**

- ❌ Too verbose (100+ lines)
- ❌ "Features" section with prose descriptions
- ❌ "Components" section listing internals
- ❌ "How It Works" section explaining architecture
- ❌ Prose explanations instead of code examples

### Good (Our Preferred Style)

````markdown
# DMV

Git and GitHub workflow preferences for Claude.

## Overview

- Tells Claude the user's commit message format (terse, no emojis, no attribution)
- Tells Claude to prefer gh CLI over GitHub MCP when available
- Documents pre-commit hook retry logic (edge case handling)

## Commands

Setup
```
/dmv:setup # walks through git and GitHub configuration
```

Main Actions
```
/pr # create pull request from current branch
/pr --draft # create draft pull request
/commit "message" # commit with user's preferred format
/github:issue <number> # fetch and analyze issue
```
````

## Command Block Formatting

**Pattern:**

````markdown
Group Label
```
/command # what it does
/command with args # what it does with args
/command:subcommand # what the subcommand does
```
````

**Details:**

- Group label as plain text (not heading): `Setup`, `Main Actions`, `Analysis`
- Code block with commands left-aligned
- Inline `#` comments right-aligned (use spaces to align)
- One blank line between groups
- No prose explanations outside code blocks

## Anti-Pattern Detection

**If you see these in a README draft, flag for removal:**

- "Features" heading followed by prose
- "Components" section listing agents/skills
- "How It Works" explanations
- "Philosophy" or "Design" sections
- "Installation" steps (beyond setup command)
- "Troubleshooting" section
- "Prerequisites" section
- "File Structure" documentation
- Workflow examples with step-by-step prose
- Version history or changelog
- Contribution guidelines

## The Transformation Rule

**Standard README approach:**

```
Explain what it does → List features → Document components → Show examples
```

**Our approach:**

```
One-liner → 2-3 bullets → Commands with comments → Done
```
