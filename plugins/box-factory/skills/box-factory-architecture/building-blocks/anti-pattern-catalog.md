# Anti-Pattern Catalog

Structure for documenting common mistakes and how to avoid them. Combines quick-reference lookup with detailed explanations.

## The Pattern

Two-part structure:

1. **Quick Reference Table** - Summary at top for fast lookup
2. **Detailed Sections** - One section per anti-pattern

```markdown
# [Topic]: Common Pitfalls

Reference for anti-patterns in [domain]. Look up specific pitfalls when [use case].

## Quick Reference

| Pitfall | Symptom | Fix |
| ------- | ------- | --- |
| [#1 Short name](#pitfall-1-full-name) | Brief symptom | Brief fix |
| [#2 Short name](#pitfall-2-full-name) | Brief symptom | Brief fix |

---

## Pitfall #1: Full Name

**Problem:** What goes wrong

[Bad example in code block]

**Why it fails:** Explanation

**Better:**

[Good example in code block]

---

## Pitfall #2: Full Name
...
```

## Quick Reference Table

The summary table enables fast lookup without reading everything.

**Columns:**

| Column  | Purpose             | Guidelines                        |
| ------- | ------------------- | --------------------------------- |
| Pitfall | Linked name         | `[#N Short name](#anchor)` format |
| Symptom | How to recognize it | Observable behavior, not cause    |
| Fix     | One-line solution   | Action verb, brief                |

**Example:**

```markdown
| Pitfall | Symptom | Fix |
| ------- | ------- | --- |
| [#1 Duplicating docs](#pitfall-1-duplicating-documentation) | Hardcoded lists that change | Point to official docs |
| [#2 Kitchen sink](#pitfall-2-kitchen-sink-scope) | >3 domains in one file | Split into focused parts |
| [#3 No triggers](#pitfall-3-missing-triggers) | Vague description | Add "Use when..." conditions |
```

## Detailed Section Structure

Each pitfall follows this structure:

### 1. Header with Number

```markdown
## Pitfall #1: Descriptive Name
```

Numbering enables quick reference table links and conversation shortcuts ("see pitfall #3").

### 2. Problem Statement

```markdown
**Problem:** [One sentence describing what goes wrong]
```

### 3. Bad Example

````markdown
```language
[Code or content showing the anti-pattern]
````

````

Show realistic examples, not strawmen. Reader should recognize their own code.

### 4. Why It Fails

```markdown
**Why it fails:** [Explanation of consequences]
````

Explain the actual harm - maintenance burden, confusion, bugs, wasted resources.

### 5. Better Example

````markdown
**Better:**

```language
[Code or content showing the correct approach]
````

````

Show the same scenario done correctly. Should be drop-in replacement where possible.

### 6. Optional: Key Improvements

For complex refactors, summarize what changed:

```markdown
**Key improvements:**

- 480 lines → 80 lines (83% reduction)
- Removed redundant content
- Kept only delta knowledge
````

## Section Separators

Use horizontal rules between pitfalls for visual separation:

```markdown
---

## Pitfall #2: Next One
```

## Example: Complete Anti-Pattern Catalog

````markdown
# Widget Design: Common Pitfalls

Reference for anti-patterns in widget design. Look up specific pitfalls when reviewing or debugging widgets.

## Quick Reference

| Pitfall | Symptom | Fix |
| ------- | ------- | --- |
| [#1 God widget](#pitfall-1-god-widget) | Widget does everything | Split by responsibility |
| [#2 Prop drilling](#pitfall-2-prop-drilling) | Props passed 4+ levels | Use context or composition |

---

## Pitfall #1: God Widget

**Problem:** Single widget handles too many responsibilities

```jsx
function Dashboard({ user, posts, comments, settings, notifications... }) {
  // 500 lines handling everything
}
````

**Why it fails:** Hard to test, maintain, and reuse. Changes ripple everywhere.

**Better:**

```jsx
function Dashboard() {
  return (
    <DashboardLayout>
      <UserProfile />
      <PostList />
      <NotificationPanel />
    </DashboardLayout>
  )
}
```

______________________________________________________________________

## Pitfall #2: Prop Drilling

**Problem:** Props passed through many intermediate components

```jsx
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <Avatar user={user} />  // Finally used here
    </Sidebar>
  </Layout>
</App>
```

**Why it fails:** Intermediate components coupled to data they don't use.

**Better:**

```jsx
<UserContext.Provider value={user}>
  <App>
    <Layout>
      <Sidebar>
        <Avatar />  // Gets user from context
      </Sidebar>
    </Layout>
  </App>
</UserContext.Provider>
```

```

## When to Create an Anti-Pattern Catalog

**Create when:**

- Domain has 3+ common mistakes worth documenting
- Mistakes are non-obvious (people keep making them)
- Correct approach requires explanation

**Skip when:**

- Only 1-2 pitfalls (include inline in main docs)
- Mistakes are obvious
- Domain is too narrow
```
