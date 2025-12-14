# Quality Checklist

Checkbox-style validation section placed at the end of documents. Ensures completeness before finishing work.

## The Pattern

```markdown
## Quality Checklist

Before completing [what]:

**[Category]:**

- [ ] Requirement 1
- [ ] Requirement 2

**[Another Category]:**

- [ ] Requirement 3
- [ ] Requirement 4
```

**Placement:** At or near the end of the document, after all instructional content.

## Structure Guidelines

**Opening line:** Always start with "Before completing \[X\]:" or "Before finalizing \[X\]:"

- Clarifies what the checklist validates
- Examples: "Before completing any skill:", "Before finalizing a plugin README:"

**Categories:** Group related items under bold headers

- Keep categories to 2-4 items each
- Use noun phrases: "Structure:", "Content:", "Size:", "Security:"

**Checklist items:**

- Start with past participle or present tense verb: "Includes...", "Has...", "Under..."
- Keep items atomic (one thing to check per line)
- Make items objectively verifiable (not subjective judgments)

## Good vs Bad Items

**Good items (verifiable):**

```markdown
- [ ] SKILL.md exists (uppercase)
- [ ] Frontmatter has name and description
- [ ] Total length under 300 lines
- [ ] Links work (anchors match heading slugs)
```

**Bad items (subjective or vague):**

```markdown
- [ ] Content is well-organized
- [ ] Code is clean
- [ ] Documentation is comprehensive
- [ ] Follows best practices
```

## Examples

### Component Creation Checklist

```markdown
## Quality Checklist

Before completing any skill:

**Structure:**

- [ ] SKILL.md exists (uppercase)
- [ ] Frontmatter has name and description
- [ ] Workflow Selection table present
- [ ] Routing conditions are specific

**Content:**

- [ ] Applies knowledge delta filter
- [ ] Subfiles are self-contained
- [ ] No README.md in skill folder

**Size:**

- [ ] SKILL.md under 300 lines
- [ ] Subfiles under 250 lines each
```

### Documentation Checklist

```markdown
## Quality Checklist

Before finalizing a plugin README:

- [ ] Total length ~20 lines (not 50-100)
- [ ] One-liner description at top
- [ ] Overview has 2-3 terse bullets
- [ ] Commands shown in code blocks with inline comments
- [ ] No "Components" or "Features" sections
- [ ] No "How It Works" explanations
```

### Validation Checklist (for reviewers)

```markdown
## Quality Checklist

When reviewing this component:

**Required:**

- [ ] Passes all automated checks
- [ ] No hardcoded version-specific details
- [ ] Defers to official docs where appropriate

**Recommended:**

- [ ] Examples included for complex patterns
- [ ] Anti-patterns documented where relevant
```

## When to Include

**Include when:**

- Document teaches how to create something
- Multiple requirements must be met
- Easy to miss important details

**Skip when:**

- Document is purely informational (no action required)
- Only 1-2 obvious requirements
- Checklist would duplicate the main content

## Checklist Length

| Items | Guidance                                  |
| ----- | ----------------------------------------- |
| 1-3   | Skip checklist, requirements are obvious  |
| 4-10  | Ideal range                               |
| 11-15 | Consider splitting into categories        |
| 16+   | Document is too complex, split into parts |
