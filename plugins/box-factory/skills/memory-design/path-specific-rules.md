# Path-Specific Rules

Rules that only load when working with files matching specific glob patterns.

## Syntax (Official Specification)

YAML frontmatter with `paths` field:

```markdown
---
paths: src/api/**/*.ts
---

# API Development Rules

[Rules that only apply to TypeScript files in src/api/]
```

**Rules without `paths` field:** Load unconditionally, apply to all files.

## Glob Pattern Support

| Pattern                | Matches                                |
| ---------------------- | -------------------------------------- |
| `**/*.ts`              | All TypeScript files in any directory  |
| `src/**/*`             | All files under src/ directory         |
| `*.md`                 | Markdown files in project root         |
| `src/components/*.tsx` | React components in specific directory |

**Multiple patterns with braces:**

```yaml
paths: src/**/*.{ts,tsx}
```

**Combined patterns with commas:**

```yaml
paths: "{src,lib}/**/*.ts, tests/**/*.test.ts"
```

## When Path-Specific Rules Add Value (Best Practices)

**Use `paths` frontmatter when:**

- Rules only apply to specific file types (e.g., "React hooks must use useMemo")
- Different directories have different conventions (frontend vs backend)
- Loading rules unnecessarily would waste context
- Clear boundary between when rules apply

**Don't use `paths` when:**

- Rules apply project-wide
- Most work involves those paths anyway
- Path patterns would be overly complex
- Simpler to have one unconditional rule file

**Good example:**

```markdown
---
paths: src/components/**/*.tsx
---

# React Component Rules

- Use functional components with hooks
- PropTypes must be defined with TypeScript interfaces
- Components must include JSDoc comments
```

**Why this works:** Only loads when editing React components, irrelevant for backend.

## Common Pitfalls

### Pitfall #1: Overly Broad Patterns

❌ Bad:

```yaml
paths: "**/*"  # Matches everything - defeats purpose
```

✅ Better: Omit `paths` field entirely (unconditional rule)

### Pitfall #2: Overly Narrow Patterns

❌ Bad:

```yaml
paths: src/api/v2/endpoints/users/controller.ts  # Single file
```

✅ Better: Make rule general enough for directory or remove `paths`

### Pitfall #3: Competing Path Patterns

❌ Bad:

```
# typescript-rules.md
paths: **/*.ts

# api-rules.md
paths: src/api/**/*.ts  # Conflicts/overlaps
```

✅ Better: Organize by domain, not file type. API rules can mention TypeScript patterns without `paths` conflict.

## Quality Checklist

- ✓ `paths` field only when rules truly specific to file subset
- ✓ Glob patterns are clear and maintainable
- ✓ No overly broad (`**/*`) or overly narrow (single file) patterns
- ✓ No competing/overlapping path patterns across files
