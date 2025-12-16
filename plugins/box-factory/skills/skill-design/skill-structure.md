# Skill Structure Reference

Universal patterns for skill folder layout and SKILL.md organization.

## Quick Reference

| Topic                                                                   | Description                    |
| ----------------------------------------------------------------------- | ------------------------------ |
| [Folder Structure](#folder-structure)                                   | Basic skill folder layout      |
| [Guidance for Splitting](#guidance-for-splitting-content-into-subfiles) | When to split vs keep unified  |
| [Subfile Organization](#subfile-organization)                           | Organizing subfolders          |
| [Subfile Content Structure](#subfile-content-structure)                 | What goes inside each subfile  |
| [Navigation Tables](#navigation-tables)                                 | Progressive disclosure pattern |
| [Scripts Folder](#scripts-folder)                                       | Executable automation          |
| [Non-Markdown Assets](#non-markdown-assets)                             | Templates, configs, images     |
| [Examples](#examples)                                                   | Common structure patterns      |

## Folder Structure

```text
my-skill/
├── SKILL.md              # Required (uppercase)
├── subtopic/             # Optional subfolder for related subfiles
    └── subtopic-main.md  # Optional subfile in subfolder
    └── sub-extra.md      # Optional additional subfile
├── topic-one.md          # Optional subfiles (any descriptive names)
├── topic-two.md
└── scripts/              # Optional (if skill has any supporting script files)
    └── helper.py
    └── helpo.sh
```

Only `SKILL.md` has a required name. Everything else is optional and can use any descriptive names.

## Guidance for Splitting Content into Subfiles

When deciding whether to keep all content in a single `SKILL.md` or split into subfiles, consider the following criteria:

**Keep in single SKILL.md when:**

- Content is interconnected (sections reference each other)
- Total under ~200 lines
- Agent typically needs most of the content together
- It's user preferences or philosophy (not lookup reference)

**Split into subfiles when:**

- Independent topics that don't reference each other
- Agent only needs one topic per task
- Any topic exceeds ~150 lines
- Content is lookup/reference style

**Decision test:** Would loading the full skill waste context on irrelevant sections?

- Yes → Split into subfiles
- No → Keep unified

## Subfile Organization

When using subfiles, organize them by topic with descriptive names. Subfiles can be standalone markdown files or grouped into subfolders for related content.

```text
my-skill/
├── SKILL.md
├── topic-one.md
└── related-topics/
    ├── subtopic-a.md
    └── subtopic-b.md
```

## Subfile Content Structure

Subfiles follow a lighter structure than SKILL.md. They're self-contained reference documents, not entry points.

**Required elements:**

| Element               | Purpose                            | When to Include |
| --------------------- | ---------------------------------- | --------------- |
| Title (`# Name`)      | Identify the subfile               | Always          |
| Brief intro           | Set context (1-2 sentences)        | Always          |
| Quick Reference table | Navigation for multi-section files | 3+ sections     |

**Optional elements (include when valuable):**

| Element               | Include When                              |
| --------------------- | ----------------------------------------- |
| Quality Checklist     | Multiple requirements easy to miss        |
| Anti-Patterns section | 3+ non-obvious mistakes worth documenting |
| Deep Dive Links       | Subfile references other detailed content |

**Subfile template:**

```markdown
# [Topic Name]

[1-2 sentence description of what this file covers]

## Quick Reference

| Topic | Description |
|-------|-------------|
| [Section One](#section-one) | What this covers |
| [Section Two](#section-two) | What this covers |

## [Section One]

[Content organized for scanning - tables, bullet points, examples]

## [Section Two]

[More content...]

## Quality Checklist (optional)

- [ ] Validation item
- [ ] Another item
```

**Key differences from SKILL.md:**

- No frontmatter (only SKILL.md needs `name` and `description`)
- No "Workflow Selection" (use "Quick Reference" instead)
- No "Official Documentation" section (SKILL.md handles that)
- Simpler structure - just the reference content

**Deep dive:** The box-factory-architecture skill's guidance on document structure covers full templates with section purposes and inclusion criteria. **Traverse when:** need comprehensive structure guidance, deciding which optional sections to include. **Skip when:** subfile template above covers your needs.

## Navigation Tables

Every file with multiple sections should have a navigation table near the top with anchor links. This enables progressive disclosure - agents scan the table, jump to what they need, skip the rest.

**Pattern:**

```markdown
# File Title

Brief intro sentence.

## Quick Reference

| Topic | Description |
|-------|-------------|
| [Section One](#section-one) | What this covers |
| [Section Two](#section-two) | What this covers |

---

## Section One
...
```

**Applies to:**

- SKILL.md (required - called "Workflow Selection")
- Subfiles with 3+ sections (strongly recommended)
- Reference/lookup files (essential)

**Skip when:**

- File has only 1-2 short sections
- Content is meant to be read sequentially (rare)

## Scripts Folder

Add `scripts/` when the skill includes executable automation (linting helpers, validation scripts, etc.):

```text
my-skill/
├── SKILL.md
├── guidance.md
└── scripts/
    ├── helper.py
    └── validate.sh
```

## Non-Markdown Assets

Template files, configuration examples, or reference assets live alongside markdown:

```text
my-skill/
├── SKILL.md
├── template.json
├── example.yaml
└── assets/
    ├── diagram.png
    └── config-sample.ini
```

## Examples

These examples illustrate common patterns, not rigid categories. Your skill's structure should match its content.

**User preferences skill (single file):**

```text
git-workflow/
└── SKILL.md    # Commit format, pre-commit retry, all interconnected
```

**Teaching skill (philosophy + reference subfiles):**

```text
skill-design/
├── SKILL.md              # Core philosophy + navigation
├── skill-structure.md    # Folder layout reference
├── skill-md.md           # SKILL.md file requirements
├── knowledge-delta.md    # What to include/exclude
└── common-pitfalls.md    # Anti-patterns lookup
```

**Reference skill (navigation + atomic pages):**

```text
home-assistant/
├── SKILL.md           # 60 lines - navigation only
├── automations.md     # 180 lines
├── services.md        # 120 lines
└── dashboards.md      # 150 lines
```
