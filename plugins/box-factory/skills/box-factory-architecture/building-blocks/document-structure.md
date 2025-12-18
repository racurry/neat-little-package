# Document Structure

Standard skeleton for component documentation. Claude uses this when creating skills, agents, detailed READMEs, or guides.

## Applying to Component Types

| Component Type | Structure                                                                          |
| -------------- | ---------------------------------------------------------------------------------- |
| Skills         | Full structure with all sections                                                   |
| Agents         | Skill Usage (if loads skills), Process with navigation, inlined quality checklists |
| CLAUDE.md      | Decision frameworks for project conventions                                        |
| READMEs        | Abbreviated (fundamentals, reference, skip checklists)                             |

## Section Inclusion Criteria

| Section            | Include When                                | Skip When                       |
| ------------------ | ------------------------------------------- | ------------------------------- |
| Fundamentals       | Always                                      | Never                           |
| Workflow Selection | 2+ distinct sections, readers need only one | Linear content, short documents |
| Anti-Patterns      | 3+ non-obvious mistakes worth documenting   | Mistakes are obvious or rare    |
| Quality Checklist  | Multiple requirements easy to miss          | 1-2 obvious requirements        |

## The Template

```markdown
# [Component Name]

[1-2 sentence description]

## Fundamentals

Critical context. Always relevant. Include all "must know" information here.
Use [Decision Frameworks](./decision-frameworks.md) when choices exist.

## Workflow Selection

| If you need to...  | Go to...                   |
| ------------------ | -------------------------- |
| [User goal/intent] | [Link to relevant section] |

Navigation table routing readers to relevant content. See [Navigation Tables](./navigation-tables.md) for format.

## [Reference Sections]

At-a-glance content for the happy path.
See [Reference Sections](./reference-sections.md) for content depth.
Use [Deep Dive Links](./deep-dive-links.md) for cross-references.

### [Subsection 1]

[Summary content - enough for simple questions, scannable]

**Deep dive:** [Link] - What's there. **Traverse when:** X. **Skip when:** Y.

## Anti-Patterns

Common mistakes. Use [Anti-Pattern Catalog](./anti-pattern-catalog.md) format for 3+ pitfalls.
Skip if domain has no non-obvious mistakes.

## Quality Checklist

Checkbox validation. Use [Quality Checklist](./quality-checklist.md) format.
Skip if requirements are obvious.
```

## Section Purposes

| Section            | Purpose                             | Building Block Used                                                                    |
| ------------------ | ----------------------------------- | -------------------------------------------------------------------------------------- |
| Fundamentals       | Essential context, always read      | [Decision Frameworks](./decision-frameworks.md) (if choices exist)                     |
| Workflow Selection | Route readers to relevant content   | [Navigation Tables](./navigation-tables.md)                                            |
| Reference          | Detailed content, consult as needed | [Reference Sections](./reference-sections.md), [Deep Dive Links](./deep-dive-links.md) |
| Anti-Patterns      | Document common mistakes            | [Anti-Pattern Catalog](./anti-pattern-catalog.md)                                      |
| Quality Checklist  | Validate completeness               | [Quality Checklist](./quality-checklist.md)                                            |
