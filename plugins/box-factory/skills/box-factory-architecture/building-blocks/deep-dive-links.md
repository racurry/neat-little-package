# Deep Dive Links

Link format pattern for cross-references to detailed content. Helps agents decide whether to traverse to more information or skip based on their current need.

## The Pattern

```markdown
**Deep dive:** [Link text](./path/to/file.md) - What it contains. **Traverse when:** conditions warranting traversal. **Skip when:** conditions where summary suffices.
```

**Three required parts:**

| Part             | Purpose                                            | Example                                                            |
| ---------------- | -------------------------------------------------- | ------------------------------------------------------------------ |
| What it contains | Help agent understand what's there without reading | "Full decision framework with CHOOSE IF/DO NOT CHOOSE IF criteria" |
| Traverse when    | Conditions that warrant reading the linked content | "ambiguous choice, edge cases, need Example User Requests"         |
| Skip when        | Conditions where the current content is enough     | "summary table clearly answers the question"                       |

## Where to Use

Deep Dive Links appear wherever there's optional deeper content:

| Location                                      | Example                                                      |
| --------------------------------------------- | ------------------------------------------------------------ |
| [Reference Sections](./reference-sections.md) | After summary content, linking to comprehensive detail       |
| Fundamentals                                  | After key concepts table, linking to full explanations       |
| Navigation Tables                             | In "Go to..." column when external file has much more detail |
| Inline mentions                               | When referencing a topic covered in depth elsewhere          |

## Cross-Component References

When linking to content in another component (especially another skill), use **indirect references** rather than direct file paths.

**Direct path (fragile):**

```markdown
**Deep dive:** [decision-frameworks.md](../other-skill/building-blocks/decision-frameworks.md) - ...
```

**Indirect reference (resilient):**

```markdown
**Deep dive:** The box-factory-architecture skill's guidance on decision frameworks covers full templates with structured choice formats. **Traverse when:** ...
```

**Why:** Components are independently maintainable. Internal file structure may change; the component's name and purpose are its stable public interface.

| Reference Type      | Approach                                        |
| ------------------- | ----------------------------------------------- |
| Same component      | Direct paths OK (`./subdir/file.md`)            |
| Different component | Indirect references ("the X skill's Y section") |

## Examples

### Good Deep Dive Link

```markdown
**Deep dive:** [Choosing the Right Component](./components/choosing.md) - Full decision framework with KEY CHARACTERISTIC, CHOOSE IF, DO NOT CHOOSE IF, and Example User Requests for each component. **Traverse when:** ambiguous component choice, need to map user intent phrases, edge cases not covered by summary. **Skip when:** summary tables clearly answer the question.
```

**Why this works:**

- Agent knows exactly what the file contains (decision framework format)
- Clear trigger for traversal (ambiguous choice, intent mapping)
- Clear signal to skip (summary suffices)

### Bad Deep Dive Link

```markdown
For more information, see [the detailed guide](./guide.md).
```

**Why this fails:**

- "More information" tells agent nothing about what's there
- No guidance on when to traverse
- Agent must read to know if it's relevant
- Wastes tokens on unnecessary traversal

### Another Bad Example

```markdown
**Deep dive:** [Component Details](./details.md) - Contains more details about components. **Traverse when:** you need more details. **Skip when:** you don't need more details.
```

**Why this fails:**

- "More details" is circular - doesn't describe actual content
- Traverse/skip conditions are tautological
- Agent still can't make informed decision

## Writing Good Conditions

### Traverse When

Use specific, recognizable conditions:

| Good                                       | Bad                       |
| ------------------------------------------ | ------------------------- |
| "ambiguous component choice"               | "you need more info"      |
| "debugging delegation failures"            | "something isn't working" |
| "need Example User Requests to map intent" | "want examples"           |
| "designing multi-component workflow"       | "complex task"            |

### Skip When

Reference what's already available:

| Good                                        | Bad                      |
| ------------------------------------------- | ------------------------ |
| "summary table clearly answers"             | "you don't need details" |
| "Fundamentals section covers your question" | "it's simple"            |
| "single-component task"                     | "basic use case"         |

## Anti-Patterns

| Anti-Pattern               | Problem                       | Fix                                                     |
| -------------------------- | ----------------------------- | ------------------------------------------------------- |
| "See X for more"           | No content description        | Describe what X contains                                |
| Tautological conditions    | "Traverse when you need it"   | Use specific, recognizable scenarios                    |
| Missing skip guidance      | Agent always traverses        | Add clear "skip when"                                   |
| Vague content description  | "Details about X"             | Describe format/structure: "Decision framework with..." |
| Cross-component file paths | Internal structure may change | Use indirect references ("the X skill's Y section")     |

## Quality Checklist

Before finalizing a Deep Dive Link:

- [ ] Content description says what's IN the file (format, structure), not just the topic
- [ ] "Traverse when" uses specific, recognizable conditions
- [ ] "Skip when" references what's already available in current context
- [ ] Agent can decide without reading the linked file
- [ ] Neither condition is tautological ("when you need it" / "when you don't")
- [ ] Cross-component references use indirect format (skill name + topic), not file paths
