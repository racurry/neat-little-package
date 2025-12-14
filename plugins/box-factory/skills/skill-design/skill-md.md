# SKILL.md File Requirements

Every skill must have a `SKILL.md` (uppercase) in its root folder.

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

### Workflow Selection Table

Routes agents to the right place without processing everything.

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
| Subfiles            | 100-200 lines each | 250 lines  |

Even teaching skills with interconnected content should keep SKILL.md under 300 lines and offload details to subfiles. Main file provides navigation and core concepts; subfiles contain depth.

## Quality Checklist

Before completing any skill:

**Structure:**

- [ ] SKILL.md exists (uppercase)
- [ ] Frontmatter has name and description
- [ ] Workflow Selection table present
- [ ] Routing conditions are specific

**Content:**

- [ ] Applies knowledge delta filter (only what Claude doesn't know)
- [ ] Subfiles are self-contained if present
- [ ] No README.md or CHANGELOG.md in skill folder

**Size:**

- [ ] SKILL.md under 300 lines
- [ ] Subfiles under 250 lines each
- [ ] Split if independent sections and over 200 lines total
