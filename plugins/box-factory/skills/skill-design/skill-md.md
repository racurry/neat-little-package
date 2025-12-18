# SKILL.md File Requirements

Every skill must have a `SKILL.md` (uppercase) in its root folder.

## Quick Reference

| Topic                                   | Description                                      |
| --------------------------------------- | ------------------------------------------------ |
| [Template](#template)                   | SKILL.md starter template                        |
| [Required Sections](#required-sections) | Frontmatter, intro, workflow table, core content |
| [Size Guidance](#size-guidance)         | Line limits for skills and subfiles              |
| [Quality Checklist](#quality-checklist) | Pre-completion validation                        |

## Template

```markdown
---
name: my-skill
description: "[What it does]. Use when [trigger 1], [trigger 2], [trigger 3]."
---

# [Skill Name]

[One to three sentences: what this skill provides and why]

## Workflow Selection

| If you need to... | Go to... |
|-------------------|----------|
| [Task 1] | [Section or file] |
| [Task 2] | [Section or file] |

## [Core Content]

[Your skill's main content - organized by topic]
```

## Required Sections

### Frontmatter

YAML frontmatter with `name` and `description`. The description should indicate when the skill loads.

### Introduction

One to three sentences explaining what the skill provides. Sets context for everything that follows.

### Fundamentals

Any required knowledge that must be read and applied by any agent reading the skill. Cannot be deferred to progressive disclosure.  Any prerequisites would go here.  This section can be omitted if there is no such content


### Workflow Selection Table

Routes agents to the right place without processing everything.  See box-factory:box-factory-architecture's "Navigation Table" for more info if needed.

**Format:**

- "If you need to..." column describes the task
- "Go to..." column links to section anchors OR subfiles
- Conditions must be specific enough to evaluate

**Good routing:**

```markdown
| If you need to... | Go to... |
|-------------------|----------|
| Format a commit message | [Message Format](#message-format) |
| Handle pre-commit failure | [Pre-Commit Edge Case](#pre-commit-edge-case) |
| Configure advanced options | [advanced-config.md](advanced-config.md) |
```

**Bad routing:**

```markdown
| Task | Reference |
|------|-----------|
| More info | [details.md](details.md) |
| Help | [troubleshooting.md](troubleshooting.md) |
```

### Core Content

The main body of the skill, organized by topic. For complex skills, this may be thin overviews routing to subfiles.

## Size Guidance

| Component           | Target             | Hard Limit |
| ------------------- | ------------------ | ---------- |
| SKILL.md (any type) | 50-200 lines       | 300 lines  |
| Subfiles            | 100-300 lines each | 500 lines  |

All skills should keep SKILL.md under 300 lines and offload details to subfiles. Main file provides navigation and core concepts; subfiles contain depth. Subfiles have more room for expansion (up to 500 lines) since they're loaded selectively.

## Quality Checklist

Before completing any skill:

**Structure:**

- [ ] SKILL.md exists (uppercase)
- [ ] Frontmatter has name and description
- [ ] Fundamentals & prerequisites present (if needed)
- [ ] Workflow Selection table present
- [ ] Routing conditions are specific

**Content:**

- [ ] Applies knowledge delta filter (only what Claude doesn't know)
- [ ] Subfiles are self-contained if present
- [ ] No README.md or CHANGELOG.md in skill folder

**Size:**

- [ ] SKILL.md under 300 lines
- [ ] Subfiles under 500 lines each
- [ ] Split if independent sections and over 200 lines total
