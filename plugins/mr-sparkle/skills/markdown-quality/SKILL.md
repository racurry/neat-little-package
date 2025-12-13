---
name: markdown-quality
description: Interpretive guidance for applying markdownlint rules using our opinionated configuration. Use when creating or editing markdown files, configuring markdownlint, troubleshooting linting issues, or reviewing markdown quality.
---

# Markdown Quality Skill

This skill teaches how to interpret and apply markdownlint rules effectively using our opinionated configuration. It provides guidance on what the rules mean in practice, when exceptions are appropriate, and how our configuration balances strictness with flexibility.

## Required Reading Before Editing Markdown

Fetch official markdownlint documentation when needed for reference:

- **<https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md>** - Complete rule reference with examples
- **<https://github.com/DavidAnson/markdownlint-cli2>** - CLI tool documentation and configuration options

**Why fetch:** Rules and best practices evolve. This skill interprets the rules; official docs define them.

## Core Understanding

### Our Markdown Philosophy

**Key principle:** Prioritize readability and practical modern usage over rigid formatting constraints.

**What this means:**

- **No line length limits** - Write naturally; let content breathe
- **Specific HTML allowed** - Markdown can't do everything; HTML fills gaps
- **Flexible document structure** - First line can be badges, images, or other metadata
- **Strict code formatting** - Always fenced blocks with language specification

**Decision test:** Does this rule enhance readability and consistency, or does it create unnecessary friction?

### Markdownlint Architecture

**How markdownlint works:**

1. Parses markdown into AST (Abstract Syntax Tree)
2. Applies configured rules to AST nodes
3. Reports violations with line numbers
4. Auto-fixes simple formatting issues (when possible)

**Important:** Not all violations are auto-fixable. Structural issues (heading hierarchy, link format) often require manual intervention.

## Configuration Approach (Best Practices)

### Layer 1: Default Rules (Official Specification)

**Official behavior:** When `"default": true`, all rules are enabled unless explicitly overridden.

**From official docs:** This is the recommended baseline - comprehensive coverage of common markdown issues.

### Layer 2: Opinionated Overrides (Best Practices)

**Our philosophy-driven configuration:**

See `default-config.jsonc` in this skill directory for the complete configuration file.

**Why these overrides work:**

- **MD013 disabled** - Modern editors handle long lines; artificial line breaks harm readability
- **MD033 selective** - Allows semantic HTML that markdown can't express
- **MD041 disabled** - Enables badges, shields.io, and metadata-first documents
- **MD024 siblings_only** - Allows "Usage" sections under different features
- **MD046 strict** - Fenced blocks are explicit, syntax-highlighting compatible

## Document Structure (Official Specification)

**From markdownlint docs:**

- **MD001** - Heading increment by one level at a time (no skipping)
- **MD022** - Headings surrounded by blank lines
- **MD025** - Single H1 per document
- **MD032** - Lists surrounded by blank lines

**Syntax:**

```markdown
# Document Title

Introductory paragraph.

## Section Heading

Content here.

### Subsection

More content.
```

## Document Structure (Best Practices)

**When hierarchy matters:**

- ✅ Use proper nesting for table of contents generation
- ✅ One H1 per document (document title)
- ✅ Sections flow logically (H2 → H3, never H2 → H4)

**When to bend rules:**

- First line can be badges/images (MD041 disabled)
- Duplicate H2 headings OK if under different H1s (MD024 siblings_only)

**Anti-pattern:**

```markdown
# Title

#### Subsection  <!-- ❌ Skipped levels -->
```

**Better:**

```markdown
# Title

## Section

### Subsection  <!-- ✅ Proper hierarchy -->
```

## Code Blocks (Official Specification)

**Required behavior (MD046):**

- MUST use fenced code blocks (triple backticks)
- MUST NOT use indented code blocks (4 spaces)
- SHOULD specify language for syntax highlighting

## Code Blocks (Best Practices)

**Always specify language:**

```markdown
<!-- ❌ No language specified -->
```

code here

````

<!-- ✅ Language specified -->
```javascript
code here
````

````

**Why:** Enables syntax highlighting, makes intent clear, helps tools process content.

**Language identifiers:**

- `javascript`, `typescript`, `python`, `bash`, `json`, `yaml`, `markdown`
- Use `text` or `plaintext` when no language applies

## Allowed HTML Elements (Best Practices)

**Our configuration allows specific HTML when markdown is insufficient:**

| Element | Use Case | Example |
|---------|----------|---------|
| `<br>` | Line breaks within paragraphs | `Line one<br>Line two` |
| `<details>` + `<summary>` | Collapsible sections | See below |
| `<img>` | Advanced image attributes | `<img src="..." width="100">` |
| `<kbd>` | Keyboard input styling | Press `<kbd>Ctrl</kbd>+<kbd>C</kbd>` |
| `<sub>` / `<sup>` | Subscript/superscript | H<sub>2</sub>O, x<sup>2</sup> |

**Collapsible section pattern:**

```markdown
<details>
<summary>Click to expand</summary>

Content here (can include markdown).

</details>
````

**Anti-pattern:**

```markdown
<!-- ❌ Arbitrary HTML -->
<div class="custom">Content</div>

<!-- ✅ Use allowed elements only -->
<details>
<summary>Custom Section</summary>
Content
</details>
```

## Links and Emphasis (Official Specification)

**From markdownlint rules:**

- **MD034** - No bare URLs (must be in angle brackets or link syntax)
- **MD037** - No spaces inside emphasis markers
- **MD049/MD050** - Consistent emphasis style

## Links and Emphasis (Best Practices)

**Link formatting:**

```markdown
<!-- ❌ Bare URL -->
Check https://example.com for details

<!-- ✅ Proper link syntax -->
Check <https://example.com> for details
Check [documentation](https://example.com) for details
```

**Emphasis consistency:**

```markdown
<!-- ✅ Consistent style -->
Use **bold** for strong emphasis
Use *italic* for emphasis

<!-- ❌ Inconsistent -->
Use **bold** and __bold__ mixed
```

**Spacing:**

```markdown
<!-- ❌ Spaces inside markers -->
** bold text **

<!-- ✅ No spaces -->
**bold text**
```

## Common Pitfalls

### Pitfall #1: Heading Hierarchy Violations

**Problem:** Skipping heading levels breaks document outline and navigation.

```markdown
# Main Title

### Subsection  <!-- ❌ MD001: Skipped H2 level -->
```

**Why it fails:** Screen readers, table-of-contents generators, and navigation tools expect proper hierarchy.

**Better:**

```markdown
# Main Title

## Section

### Subsection  <!-- ✅ Proper progression -->
```

### Pitfall #2: Indented Code Blocks

**Problem:** Using 4-space indentation instead of fenced blocks.

```markdown
<!-- ❌ Indented code block (MD046) -->
    const x = 1;
    console.log(x);
```

**Why it fails:** No language specification, less explicit, harder to process.

**Better:**

````markdown
<!-- ✅ Fenced code block with language -->
```javascript
const x = 1;
console.log(x);
````

````

### Pitfall #3: Missing Blank Lines

**Problem:** No spacing around structural elements.

```markdown
# Heading
Content immediately after heading
- List item  <!-- ❌ MD032: No blank line before list -->
````

**Why it fails:** Reduces readability, can cause parsing ambiguities.

**Better:**

```markdown
# Heading

Content with proper spacing.

- List item  <!-- ✅ Blank lines around structural elements -->
```

### Pitfall #4: Trailing Whitespace

**Problem:** Invisible spaces at end of lines.

**Why it fails:** Causes unnecessary diff noise, some markdown parsers interpret as hard breaks.

**Detection:** Most editors can highlight trailing whitespace.

**Fix:** Configure editor to strip trailing whitespace on save, or run `markdownlint-cli2 --fix`.

## Automatic Hook Behavior

The mr-sparkle plugin includes a PostToolUse hook that:

1. Triggers after Write and Edit operations
2. Detects markdown files (`.md`, `.markdown`)
3. Runs `markdownlint-cli2 --fix` automatically
4. Reports unfixable issues (non-blocking)
5. Silently skips if markdownlint-cli2 not installed

**What this means:** Most formatting issues auto-fix on save. Pay attention to reported unfixable issues.

## Quality Checklist

**Before finalizing markdown:**

**From official rules:**

- ✓ Proper heading hierarchy (no skipped levels)
- ✓ Blank lines around headings, lists, code blocks
- ✓ Code blocks are fenced with language specified
- ✓ No trailing whitespace
- ✓ Links use proper syntax (not bare URLs)
- ✓ Single H1 per document

**Best practices:**

- ✓ Only allowed HTML elements used
- ✓ Consistent emphasis style (`**bold**`, `*italic*`)
- ✓ Language specified for all code blocks
- ✓ Collapsible sections use `<details>` + `<summary>`
- ✓ Natural line length (no artificial breaks)

## Commands

### `/mr-sparkle:lint-md [path]`

**Use when:**

- Reviewing existing markdown files
- Checking documentation before commit
- Identifying issues without making changes
- Learning which rules apply to your content

**Example:** `/mr-sparkle:lint-md docs/` or `/mr-sparkle:lint-md README.md`

### `/mr-sparkle:fix-md [path]`

**Use when:**

- Cleaning up formatting issues
- Preparing markdown for commit
- Batch-fixing multiple files
- After configuration changes

**Note:** Not all issues can be auto-fixed. Structural problems require manual intervention.

**Example:** `/mr-sparkle:fix-md docs/` or `/mr-sparkle:fix-md .`

## Reference Documentation

**Detailed guides** (loaded on-demand for progressive disclosure):

- `rules-reference.md` - Complete table of markdownlint rules enforced
- `pitfalls-reference.md` - Common mistakes with detailed examples
- `troubleshooting.md` - Debugging guide for common issues
- `default-config.jsonc` - Full configuration file with opinionated defaults

**Official documentation to fetch:**

- <https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md> - Complete rule reference
- <https://github.com/DavidAnson/markdownlint-cli2> - CLI tool and configuration
- <https://commonmark.org/> - CommonMark standard
- <https://github.github.com/gfm/> - GitHub Flavored Markdown

**Remember:** This skill interprets markdownlint rules and our configuration philosophy. Always fetch official docs for current rule definitions and syntax details.
