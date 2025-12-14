# Decision Framework Patterns

When skill content helps Claude choose between multiple options, use this structured format for clarity and consistency.

| If you need to...                             | Go to...                                                        |
| --------------------------------------------- | --------------------------------------------------------------- |
| Choose between two options (brief criteria)   | [Table-Driven Binary Decisions](#table-driven-binary-decisions) |
| Choose between two options (complex criteria) | [Binary Decisions](#binary-decisions)                           |
| Choose between three or more options          | [Multiple-Option Decisions](#multiple-option-decisions)         |

## Table-Driven Binary Decisions

### When to Use This Pattern

Use when you have multiple parallel binary decisions with brief, objective criteria.

**Choose table format when:**

- Criteria fit in 5-10 words
- No explanation needed - criteria are self-evident
- Multiple parallel decisions (multiple rows)

**Choose prose format ([Binary Decisions](#binary-decisions)) when:**

- Criteria need context or explanation
- Single decision point
- Tradeoffs are nuanced

### The Pattern

```markdown
| [Subject]    | [Condition A]     | [Condition B]    |
| ------------ | ----------------- | ---------------- |
| Item 1       | When to choose A  | When to choose B |
| Item 2       | When to choose A  | When to choose B |
```

Common header pairs:

- `Include When` / `Skip When`
- `Choose When` / `Avoid When`
- `Use` / `Don't Use`

### Example

From the Document Structure guidance in this skill:

```markdown
| Section            | Include When                                | Skip When                       |
| ------------------ | ------------------------------------------- | ------------------------------- |
| Fundamentals       | Always                                      | Never                           |
| Workflow Selection | 2+ distinct sections, readers need only one | Linear content, short documents |
| Anti-Patterns      | 3+ non-obvious mistakes worth documenting   | Mistakes are obvious or rare    |
| Quality Checklist  | Multiple requirements easy to miss          | 1-2 obvious requirements        |
```

This works as a table because each criterion is brief and objective - no explanation needed.

______________________________________________________________________

## Binary Decisions

### When to Use This Pattern

Use for yes/no, keep/split, enable/disable decisions where criteria need explanation.

### The Pattern

```markdown
## Choice 1
- **Choose When:**
  - Condition indicating to pick this one
  - Another positive criterion
- **Avoid When:**
  - Condition indicating to split (use [Choice 2](#choice-2) instead)
  - Another negative criterion  
## Choice 2
- **Choose When:**
  - Condition indicating to pick this one 
  - Another positive criterion
- **Avoid When:**
  - Condition indicating to keep (use [Choice 1](#choice-1) instead)
  - Another negative criterion
```

Example:

```markdown
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
```

## Multiple-Option Decisions

### When to Use This Pattern

**Use for multi-option decisions:**

- Choosing between 3+ alternatives (component types, tools, approaches)
- Options have complex tradeoffs that benefit from structured comparison
- Users express intent in varied ways that map to specific options

**Do NOT use for binary decisions:**

- Keep vs Split, Yes vs No, Enable vs Disable
- Binary choices work better as simple criteria lists (see [Binary Decisions](#binary-decisions) above)

### The Pattern

For each option in a decision:

```markdown
## [Option Name]

- **Key Trait:** Single sentence - what makes this option fundamentally distinct
- **Choose When:**
  - Condition that indicates this is the right choice
  - Another positive selection criterion
  - Pattern in user request that maps here
- **Avoid When:**
  - Condition indicating wrong choice (use [Alternative](#alternative) instead)
  - Another negative criterion (use [Other](#other) instead)
- **Example Requests:**
  - "Quoted phrase a user might say"
  - "Another real request pattern"
- **Examples:**
  - `concrete-example-1` - brief description
  - `concrete-example-2` - brief description
```

### Section Purposes

| Section              | Purpose                                                                     |
| -------------------- | --------------------------------------------------------------------------- |
| **Key Trait**        | Quick identification - the defining characteristic                          |
| **Choose When**      | Positive selection - conditions that indicate fit                           |
| **Avoid When**       | Negative selection with alternatives - prevents wrong choices AND redirects |
| **Example Requests** | User intent mapping - real phrases that trigger this choice                 |
| **Examples**         | Grounding - concrete instances that demonstrate the option                  |

### Example: Choosing a State Management Approach

This example demonstrates the pattern for a hypothetical React project skill:

### Local State

- **Key Trait:** Component-scoped state using useState/useReducer
- **Choose When:**
  - State only needed by one component or its direct children
  - No need to share across distant parts of the tree
  - Simple data that doesn't require complex updates
- **Avoid When:**
  - Multiple unrelated components need the same state (use [Context](#context) instead)
  - State updates are complex with many actions (use [External Store](#external-store) instead)
- **Example Requests:**
  - "Add a toggle for showing/hiding this panel"
  - "Track form input values"
- **Examples:**
  - `useState(false)` for modal open/close
  - `useReducer` for multi-field form state

### Context

- **Key Trait:** React-native sharing without prop drilling
- **Choose When:**
  - Multiple components need same state but updates are infrequent
  - Data is "global" to a subtree (theme, user, locale)
  - Want to avoid adding dependencies
- **Avoid When:**
  - Frequent updates causing re-render performance issues (use [External Store](#external-store) instead)
  - State is component-local (use [Local State](#local-state) instead)
- **Example Requests:**
  - "Make the current user available throughout the app"
  - "Add dark mode toggle accessible everywhere"
- **Examples:**
  - `ThemeContext` for color scheme
  - `AuthContext` for current user

### External Store

- **Key Trait:** Dedicated state library with optimized subscriptions
- **Choose When:**
  - Complex state logic with many actions
  - Need fine-grained subscription to avoid re-renders
  - State must persist or sync across tabs/sessions
- **Avoid When:**
  - Simple state that doesn't justify the dependency (use [Local State](#local-state) instead)
  - Just avoiding prop drilling with infrequent updates (use [Context](#context) instead)
- **Example Requests:**
  - "Add a shopping cart that persists across page refreshes"
  - "Implement undo/redo for the editor"
- **Examples:**
  - Zustand store for shopping cart
  - Redux for complex app state with devtools

### Applying This Pattern

When writing skill content that involves choosing between approaches:

1. Identify all options (should be 3+)
2. For each option, fill in all five sections
3. Ensure "Avoid When" always points to alternatives
4. Use real user language in "Example Requests"
5. Provide 2-3 concrete examples per option

**Skip this pattern when:**

- Binary decision (use criteria lists instead)
- No real alternatives exist
- Decision is trivial/obvious
