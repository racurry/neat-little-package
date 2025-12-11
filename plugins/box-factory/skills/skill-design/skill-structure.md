# Skill Structure Reference

Universal patterns for skill folder layout and SKILL.md organization.

## Folder Structure

```text
my-skill/
├── SKILL.md              # Required (uppercase)
├── topic-one.md          # Optional subfiles (any descriptive names)
├── topic-two.md
└── scripts/              # Optional (if skill has automation)
    └── helper.py
```

Only `SKILL.md` has a required name. Everything else is optional and can use any descriptive names.

## SKILL.md Template

```markdown
---
name: my-skill
description: "[What it does]. Use when: [trigger 1], [trigger 2], [trigger 3]."
---

# [Skill Name]

[One sentence: what this skill provides and why]

## Workflow Selection

| If you need to... | Go to... |
|-------------------|----------|
| [Task 1] | [Section or file] |
| [Task 2] | [Section or file] |
| [Task 3] | [Section or file] |

## [Core Content]

[Your skill's main content - organized by topic]

## Quality Checklist

[Validation items specific to this skill's domain]
```

## Workflow Selection (Required)

Every skill needs a Workflow Selection table as the first content section.

**Purpose:** Route agents to the right place without processing everything.

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

## When to Split into Subfiles

**Keep in single SKILL.md when:**

- Content is interconnected (sections reference each other)
- Total under ~200 lines
- Agent typically needs most of the content together
- It's user preferences or philosophy (not lookup reference)

**Split into subfiles when:**

- Independent topics that don't reference each other
- Agent only needs one topic per task
- Any topic exceeds ~150 lines
- Content is lookup/reference style (not teaching)

**Decision test:** Would loading the full skill waste context on irrelevant sections?

- Yes → Split into subfiles
- No → Keep unified

## Size Guidance

| Component                | Target             | Consider splitting if...                 |
| ------------------------ | ------------------ | ---------------------------------------- |
| SKILL.md (unified)       | 50-200 lines       | Over 300 lines with independent sections |
| SKILL.md (with subfiles) | 30-80 lines        | Just navigation + core concepts          |
| Subfiles                 | 100-200 lines each | Over 250 lines                           |
| Quick Start section      | ≤20 lines          | Needs more than basic example            |

**Teaching/philosophy skills** can be longer (500+ lines) if content is truly interconnected.

## Scripts Folder

Add `scripts/` when the skill includes automation:

```text
my-skill/
├── SKILL.md
└── scripts/
    ├── main-operation.py
    └── helper.py
```

Document scripts in SKILL.md:

```markdown
## Scripts

| Script | Purpose | When to use |
|--------|---------|-------------|
| `scripts/main-operation.py` | [What] | [Condition] |
```

## Quality Checklist

Before completing any skill:

**Structure:**

- ✓ SKILL.md exists (uppercase)
- ✓ Workflow Selection table present
- ✓ Routing conditions are specific

**Content:**

- ✓ Applies knowledge delta filter (only what Claude doesn't know)
- ✓ Subfiles are self-contained if present
- ✓ No README.md or CHANGELOG.md in skill folder

**Size:**

- ✓ SKILL.md appropriate for content type
- ✓ Subfiles under 250 lines each
- ✓ Split if independent sections and over 200 lines total

## Examples

**User preferences skill (single file, ~150 lines):**

```text
git-workflow/
└── SKILL.md    # Commit format, pre-commit retry, all interconnected
```

**Teaching skill (single file, ~500 lines):**

```text
skill-design/
├── SKILL.md              # Core philosophy
├── skill-structure.md    # This file - structure reference
├── knowledge-delta.md    # What to include/exclude
└── common-pitfalls.md    # Anti-patterns lookup
```

**Reference skill (multiple subfiles):**

```text
home-assistant/
├── SKILL.md           # 60 lines - navigation only
├── automations.md     # 180 lines
├── services.md        # 120 lines
└── dashboards.md      # 150 lines
```
