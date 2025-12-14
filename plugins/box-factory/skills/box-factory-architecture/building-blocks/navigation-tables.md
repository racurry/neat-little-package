# Navigation Tables

Tables at the top of markdown files that route readers to relevant content. The core pattern for progressive discovery.

| If you need to...                                | Go to...                                              |
| ------------------------------------------------ | ----------------------------------------------------- |
| Choose a table format (workflow vs reference)    | [Choosing a Variation](#choosing-a-variation)         |
| Write effective left columns (semantic matching) | [Semantic Coverage](#semantic-coverage)               |
| Avoid common mistakes                            | [Anti-Patterns](#anti-patterns)                       |
| Decide whether to include a nav table            | [When to Include](#when-to-include-navigation-tables) |

## The Pattern

```markdown
| [Left Column Header]  | [Right Column Header] |
| --------------------- | --------------------- |
| What reader is seeking | Where to find it     |
```

**Placement:** After title and brief description, before main content.

## Choosing a Variation

| Reader comes with...        | Use...                                            |
| --------------------------- | ------------------------------------------------- |
| A task or goal (action)     | [Workflow Selection](#workflow-selection-default) |
| A subject to look up (noun) | [Reference Lookup](#reference-lookup)             |

## Workflow Selection (Default)

The standard navigation table for components (skills, agents, commands). Use when readers come with a task or goal in mind.

**Headers:** `If you need to...` | `Go to...`

```markdown
## Workflow Selection

| If you need to...                                       | Go to...                                    |
| ------------------------------------------------------- | ------------------------------------------- |
| Choose a component type (skill vs agent vs command)     | [Component Selection](#component-selection) |
| Understand delegation patterns (who calls whom)         | [Delegation](./architecture/delegation.md)  |
| Structure choices and tradeoffs (decision frameworks)   | [Building Blocks](#building-blocks)         |
```

**Left column guidelines:**

- Start with action verb: "Understand", "Create", "Debug", "Choose"
- Use **parentheticals for semantic expansion**: `Choose a component type (skill vs agent)`
- Phrase as user goal, not content description
- Keep primary phrase concise (5-10 words), parenthetical adds keywords

**When to use:** Most components. This is the default choice.

## Reference Lookup

Use when readers come with a subject they want to learn about, not a task to accomplish.

**Headers:** `[Subject Type]` | `Go to...` (e.g., `Component`, `Topic`, `Symptom`)

```markdown
| Component   | Go to...                                 |
| ----------- | ---------------------------------------- |
| `Sub-agent` | [Sub-agent](#when-to-create-a-sub-agent) |
| `Skill`     | [Skill](#when-to-create-a-skill)         |
| `Command`   | [Command](#when-to-create-a-command)     |
```

```markdown
| Topic              | Go to...                |
| ------------------ | ----------------------- |
| Directory layout   | [Structure](#structure) |
| Naming conventions | [Naming](#naming)       |
```

**Left column guidelines:**

- Use noun phrases (not action verbs)
- Use code ticks for technical entity names (`Sub-agent`), plain text for concepts (Directory layout)
- List in logical order (most common first, or by importance)
- Keep names exact (match what readers would search for)

**When to use:** Reference documents, guides, tutorials—anywhere readers browse by subject rather than goal.

## Creating Custom Variations

If standard variations don't fit, create your own by following these principles:

1. **Left column = what reader knows** (their goal, the entity name, the topic)
2. **Right column = where to go** (always links)
3. **Headers should be self-explanatory** (reader should understand without context)

**Example custom variation for a troubleshooting doc:**

```markdown
| Symptom                    | Solution                          |
| -------------------------- | --------------------------------- |
| Build fails silently       | [Silent Failures](#silent)        |
| Tests pass locally but not CI | [CI Issues](#ci-issues)        |
```

## Semantic Coverage

The left column must catch how agents actually frame their needs. Agents do fuzzy semantic matching, not string matching—but key concepts must be present.

**The recognition test** for each row:

1. If an agent has this need, will they recognize this row? (must be yes)
2. If they DON'T have this need, will they incorrectly match? (should be no)

**Techniques for coverage:**

| Technique                | Example                                       | When to use                                           |
| ------------------------ | --------------------------------------------- | ----------------------------------------------------- |
| Parenthetical expansion  | `Choose a component (skill vs agent)`         | Add keywords without killing scannability             |
| Problem + action framing | `Debug delegation (calls not reaching agent)` | Catch both "I have problem X" and "I need to do Y"    |
| Escape hatch row         | `Get oriented / unsure where to start`        | Complex documents where agents may not see themselves |

**Problem vs action framing:**

Agents think two ways:

- "I have a problem" → "unsure which component type"
- "I need to do something" → "choose a component type"

Good rows accommodate both when natural: `Choose a component (unsure what type fits)`

**Escape hatch for complex documents:**

```markdown
| If you need to...                    | Go to...              |
| ------------------------------------ | --------------------- |
| Get oriented / unsure where to start | [Overview](#overview) |
```

Catches agents who don't see themselves in any row. Prevents "skip the table, read everything."

## Anti-Patterns

| Anti-Pattern               | Problem                                             | Fix                                                |
| -------------------------- | --------------------------------------------------- | -------------------------------------------------- |
| Verbose left columns       | Kills scannability                                  | Use parentheticals, not prose                      |
| Many-to-one redundant rows | Creates noise, agent wonders "are these different?" | One row per destination, expand with parenthetical |
| Too terse                  | Missing semantic coverage, agents miss the row      | Add parenthetical keywords                         |
| No escape hatch            | Agents with unclear needs read everything           | Add "Get oriented" row for complex docs            |

## When to Include Navigation Tables

**Include when:**

- Document has 3+ distinct topics or sections
- Readers might need only one section per visit
- Content serves multiple use cases

**Skip when:**

- Document is short and linear (< 50 lines)
- Content must be read sequentially
- Single-purpose reference

## Quality Checklist

**Structure:**

- [ ] Placed immediately after title/intro
- [ ] Right column contains working links
- [ ] 3-8 rows (fewer = skip table; more = reorganize document)
- [ ] Headers are self-explanatory

**Semantic coverage:**

- [ ] Each row passes recognition test (matching agents recognize, non-matching don't false-match)
- [ ] Key concepts present via parentheticals where needed
- [ ] Complex documents have escape hatch row
- [ ] Left column uses agent's framing (problem or action), not content description
