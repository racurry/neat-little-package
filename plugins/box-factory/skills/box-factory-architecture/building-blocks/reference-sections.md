# Reference Sections

Content design pattern for the main body of documents. Reference sections provide at-a-glance information for the happy path - enough for agents to answer simple questions without traversing to deeper content.

## The Pattern

Each reference section should be:

- **Self-contained** - Answers questions about its topic without requiring other sections
- **Happy path focused** - Covers the 80% case, common scenarios
- **Scannable** - Structured for quick lookup (tables, bullet points, clear headers)
- **Quality-check ready** - Contains enough detail for standards validation

## Content Depth Guidelines

| Include                                                     | Exclude                        |
| ----------------------------------------------------------- | ------------------------------ |
| Common scenarios and their solutions                        | Edge cases and rare situations |
| Key decision criteria (summary level)                       | Exhaustive decision trees      |
| Quick-reference tables                                      | Lengthy explanations           |
| Concrete examples (1-2 per concept)                         | Comprehensive example catalogs |
| Links to detail via [Deep Dive Links](./deep-dive-links.md) | Inline deep explanations       |

**The test:** Can an agent answer a straightforward question about this topic using only this section? If yes, depth is right. If they need to traverse for basic questions, add more. If they never need the detail, trim it.

## Structure

```markdown
## [Section Name]

[1-2 sentence description of what this section covers]

[Core content: tables, bullet points, brief explanations]

[Optional: Quick example or two]

**Deep dive:** [Link] - What's there. **Traverse when:** X. **Skip when:** Y.
```

## Example: Good Reference Section

```markdown
## Component Selection

Choose components based on what you need to accomplish.

| Need | Component | Key Trait |
|------|-----------|-----------|
| Autonomous work | Agent | Isolated context, returns results |
| Reusable guidance | Skill | Loads when relevant |
| User-triggered action | Command | Explicit invocation |
| Guaranteed enforcement | Hook | Deterministic execution |

**Deep dive:** [Choosing the Right Component](./components/choosing.md) - Full decision framework with CHOOSE IF/DO NOT CHOOSE IF criteria. **Traverse when:** ambiguous choice, edge cases. **Skip when:** table answers clearly.
```

**Why this works:**

- Table answers "which component for X?" at a glance
- Enough for simple selection decisions
- Links to detail for complex cases
- Agent can validate component choices against this

## Example: Bad Reference Section

```markdown
## Component Selection

Components are the building blocks of Claude Code. There are many types
of components, each with their own purpose and use cases. Understanding
when to use each component is critical for building effective solutions.

Agents are isolated AI instances that perform autonomous work. They operate
in their own context and return complete results. You should use agents when
you have complex logic that requires isolation...

[continues for 200 lines covering every detail]
```

**Why this fails:**

- No quick-reference structure
- Can't scan for answers
- Buries the happy path in exhaustive detail
- Agent must read everything to find anything

## When Sections Need Deep Dive Links

| Section State                              | Action                                     |
| ------------------------------------------ | ------------------------------------------ |
| Covers happy path, detail exists elsewhere | Add [Deep Dive Link](./deep-dive-links.md) |
| Covers everything needed                   | No link needed                             |
| Too shallow for basic questions            | Add content, not just links                |
| Too deep for scanning                      | Move detail to subfile, add link           |

## Quality Checklist

Before finalizing a reference section:

- [ ] Answers common questions about the topic at a glance
- [ ] Structured for scanning (tables, bullets, clear headers)
- [ ] Covers 80% case without requiring traversal
- [ ] Self-contained (doesn't require reading other sections)
- [ ] Links to detail using Deep Dive pattern when deeper content exists
- [ ] Not so detailed that it's hard to scan
