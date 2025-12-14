# Skill Design: Common Pitfalls

Reference for anti-patterns in skill design. Look up specific pitfalls when reviewing or debugging skills.

## Quick Reference

| Pitfall                                                                         | Symptom                         | Fix                                          |
| ------------------------------------------------------------------------------- | ------------------------------- | -------------------------------------------- |
| [#1 Duplicating docs](#pitfall-1-duplicating-official-documentation)            | Hardcoded lists that change     | Point to official docs, interpret don't copy |
| [#2 Version-specific](#pitfall-2-hardcoding-version-specific-details)           | Tool names, model IDs inline    | Reference docs, teach philosophy             |
| [#3 Opinions as specs](#pitfall-3-presenting-opinions-as-official-requirements) | "MUST" without citation         | Mark as "(Best Practices)"                   |
| [#4 Kitchen sink](#pitfall-4-kitchen-sink-skills)                               | >3 domains in one skill         | Split into focused skills                    |
| [#5 No triggers](#pitfall-5-no-clear-triggering-conditions)                     | Vague description               | Add "Use when..." conditions                 |
| [#6 Base knowledge](#pitfall-6-documenting-claudes-base-knowledge)              | Documenting git/npm/etc basics  | Apply knowledge delta filter                 |
| [#7 Monolithic reference](#pitfall-7-monolithic-reference-skills)               | Independent domains in one file | Split into subpages                          |

______________________________________________________________________

## Pitfall #1: Duplicating Official Documentation

**Problem:** Skill becomes outdated copy of docs

```markdown
## Available Models

The following models are available:
- claude-sonnet-4-5-20250929
- claude-opus-4-20250514
- claude-3-5-haiku-20241022
```

**Why it fails:** Model names change, skill becomes outdated

**Better:**

```markdown
## Model Selection

Fetch current model options from:
https://code.claude.com/docs/en/model-config.md

**Best practice:** Use haiku for simple tasks, sonnet for balanced work, opus for complex reasoning.
```

______________________________________________________________________

## Pitfall #2: Hardcoding Version-Specific Details

**Problem:** Skill includes specifics that change

```markdown
## Tool Permissions

Grant these tools to your agent:
- Read (for reading files)
- Write (for writing files)
- Edit (for editing files)
```

**Why it fails:** Tool list may expand, descriptions may change

**Better:**

```markdown
## Tool Selection Philosophy

**Match tools to autonomous responsibilities:**

- If agent analyzes only → Read, Grep, Glob
- If agent writes code → Add Write, Edit
- If agent runs commands → Add Bash

Fetch current tool list from:
https://code.claude.com/docs/en/settings#tools-available-to-claude
```

______________________________________________________________________

## Pitfall #3: Presenting Opinions as Official Requirements

**Problem:** Blurs the line between specs and best practices

```markdown
## Agent Description Field

The description field MUST use strong directive language like "ALWAYS use when" to ensure proper delegation.
```

**Why it fails:** Official docs don't require this; it's a best practice opinion

**Better:**

```markdown
## Description Field Design (Best Practices)

Official requirement: "Natural language explanation of when to invoke"

**Best practice:** Use specific triggering conditions and directive language to improve autonomous delegation. While not required, this pattern increases the likelihood of proper agent invocation.
```

______________________________________________________________________

## Pitfall #4: Kitchen Sink Skills

**Problem:** One skill tries to cover everything

```markdown
# Full-Stack Development Skill

This skill covers:
- Frontend frameworks (React, Vue, Angular)
- Backend APIs (Node, Python, Go, Rust)
- Databases (SQL, NoSQL)
- DevOps (Docker, K8s, CI/CD)
- Security best practices
- Testing strategies
...
```

**Why it fails:** Too broad, overwhelming, hard to maintain, loads unnecessarily

**Better:** Split into focused skills:

- `frontend-architecture`
- `api-design`
- `testing-strategy`

______________________________________________________________________

## Pitfall #5: No Clear Triggering Conditions

**Problem:** Description doesn't indicate when skill should load

```markdown
---
name: api-standards
description: API documentation standards
---
```

**Why it fails:** Unclear when this skill is relevant

**Better:**

```markdown
---
name: api-standards
description: Guidelines for designing and documenting REST APIs following team standards. Use when creating endpoints, reviewing API code, or writing API documentation.
---
```

______________________________________________________________________

## Pitfall #6: Documenting Claude's Base Knowledge

**Problem:** Skill includes comprehensive documentation of tools and workflows Claude already knows from training, creating token waste and maintenance burden without adding value.

**Bad example (hypothetical 480-line git-workflow skill):**

```markdown
---
name: git-workflow
description: Comprehensive git usage guide
---

# Git Workflow Skill

## Common Git Operations

**Checking Repository Status:**

git status  # Shows staged, unstaged, and untracked files

**See detailed diff:**

git diff  # Unstaged changes
git diff --staged  # Staged changes

**Branch Operations:**

git checkout -b feature-name  # Create and switch
git switch main  # Switch to main

[... 400 more lines documenting standard git commands ...]
```

**Why it fails:**

- Claude already knows all standard git commands from training
- 95% of content is redundant with base knowledge
- Wastes tokens loading information Claude doesn't need
- Creates maintenance burden (skill needs updates when nothing actually changed)
- Obscures the 5% that's actually valuable (user-specific preferences)
- No behavioral change - Claude would do the same without this skill

**Better (focused 80-line version documenting only the delta):**

```markdown
---
name: git-workflow
description: User-specific git workflow preferences and edge case handling. Use when creating commits or handling pre-commit hook failures.
---

# Git Workflow Skill

This skill documents workflow preferences and edge cases specific to this user. For standard git knowledge, Claude relies on base training.

## Commit Message Requirements (User Preference)

**This user requires:**

- Terse, single-line format (max ~200 characters)
- No emojis or decorative elements
- **No attribution text** (no "Co-Authored-By:", no "Generated with Claude Code")

## Pre-Commit Hook Edge Case (Critical)

**Problem:** Pre-commit hooks modify files during commit, causing failure.

**Workflow:**

1. Attempt: `git commit -m "message"`
2. Hook modifies files (auto-format)
3. Commit FAILS (working directory changed)
4. Stage modifications: `git add .`
5. Retry ONCE: `git commit --amend --no-edit`

**Critical:** Only retry ONCE to avoid infinite loops.
```

**Key improvements:**

- 480 lines → 80 lines (83% reduction)
- Removed all standard git knowledge Claude already has
- Kept only user-specific preferences and edge cases
- 100% of content is valuable delta knowledge

______________________________________________________________________

## Pitfall #7: Monolithic Reference Skills

**Problem:** Reference skill covers multiple independent domains in a single file, forcing agents to load irrelevant content.

**Bad example (750-line home-assistant skill):**

```markdown
---
name: home-assistant
description: Home Assistant guidance
---

# Home Assistant Skill

## Automation Patterns
[200 lines of automation syntax...]

## Service Calls
[150 lines of service call syntax...]

## Dashboard Configuration
[200 lines of Lovelace card types...]

## Integrations
[100 lines of integration patterns...]

## MCP Setup
[100 lines of MCP configuration...]
```

**Why it fails:**

- Agent working on automations loads 550 lines of irrelevant content
- Wastes context window on dashboard syntax when only needing services
- Independent domains don't benefit from being together
- This is a reference skill (lookup patterns), not a teaching skill (philosophy)

**Better (split into atomic subpages):**

```text
skills/home-assistant/
├── SKILL.md           # 77 lines - core concepts + navigation table
├── automations.md     # 180 lines - trigger, condition, action patterns
├── services.md        # 120 lines - service call syntax
├── dashboards.md      # 150 lines - Lovelace card types
├── integrations.md    # 130 lines - template sensors, MQTT
├── mcp-setup.md       # 100 lines - MCP server configuration
└── troubleshooting.md # 150 lines - pitfalls, debugging
```

**Main SKILL.md provides navigation:**

```markdown
## Workflow Selection

| If you need to... | Go to... |
|-------------------|----------|
| Create/edit automations | [automations.md](automations.md) |
| Call services | [services.md](services.md) |
| Build dashboards | [dashboards.md](dashboards.md) |
```

**Key improvements:**

- Agent loads ~250 lines (main + one subpage) instead of 750
- Each subpage is self-contained
- Navigation table helps agent choose what to load
- Subpages can be updated independently
