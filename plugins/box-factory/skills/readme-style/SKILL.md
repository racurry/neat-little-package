---
name: readme-style
description: User's preferred ultra-terse README style for plugins. Use when writing or reviewing plugin README files.
---

# README Style Skill

This skill documents the user's specific README style preferences - a knowledge delta from standard README writing. Claude knows how to write READMEs; this documents what makes THIS user's style different.

## Core Philosophy (User Preference)

**Ultra-terse:** ~20 lines total, not 50-100
**Action-focused:** Show commands with inline comments, minimal prose
**No fluff:** Skip troubleshooting, file structure, version history

## Structure Pattern (User Preference)

````markdown
# Plugin Name

One-liner description.

## Overview

- What it tells Claude to do (bullet 1)
- What it tells Claude to do (bullet 2)

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

- Opening: Plugin name + single-line description
- Overview: 2-3 terse bullets describing what it does
- Commands: Grouped code blocks with inline `#` comments
- That's it. Nothing more.

## What to Include (User Preference)

**Include ONLY:**

- ✓ Plugin name (H1)
- ✓ One-liner description
- ✓ Terse bullet points (2-3) describing what it does
- ✓ Commands grouped by purpose (Setup, Main Actions, etc.)
- ✓ Inline `#` comments explaining each command
- ✓ Minimal section headers (just enough to group commands)

**Total length:** ~20 lines

## What to EXCLUDE (User Preference)

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

````markdown
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
````

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
```

**Improvements:**

- ✓ 20 lines total (vs 100+)
- ✓ Terse bullets in Overview
- ✓ Commands shown directly with inline comments
- ✓ No "Components", "Features", "How It Works" sections
- ✓ Action-focused, not explanation-focused

## Command Block Formatting (User Preference)

**Pattern:**

```markdown
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

**Example:**

````markdown
Setup
```

/plugin:init # initialize plugin configuration

```

Analysis
```

/plugin:check current # analyze current state
/plugin:check all # comprehensive analysis

```
````

## Quality Checklist

Before finalizing a plugin README:

- ✓ Total length ~20 lines (not 50-100)
- ✓ One-liner description at top
- ✓ Overview has 2-3 terse bullets (not prose paragraphs)
- ✓ Commands shown in code blocks with inline comments
- ✓ No "Components" section
- ✓ No "Features" section with prose descriptions
- ✓ No "How It Works" or philosophy sections
- ✓ No troubleshooting, installation, or file structure docs
- ✓ No resource links or references
- ✓ Minimal section headers (just grouping labels)

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

**Remember:** Use code examples with comments, not prose explanations.

## The Transformation Rule

**Standard README approach:**

```
Explain what it does → List features → Document components → Show examples
```

**Our approach:**

```
One-liner → 2-3 bullets → Commands with comments → Done
```

**Length target:** Standard README = 50-100 lines. We do ~20-50 lines.
