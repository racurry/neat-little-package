# Common Markdown Pitfalls

Detailed examples of common mistakes and how to fix them.

## Pitfall #1: Inconsistent Heading Styles

**Problem:** Mixing ATX and setext heading styles

```markdown
# Heading 1

Heading 2
---------
```

**Why it fails:** MD003 requires consistent heading style (we use ATX)

**Better:**

```markdown
# Heading 1

## Heading 2
```

## Pitfall #2: Missing Code Block Languages

**Problem:** Fenced code blocks without language specifiers

````markdown
```
code here
```
````

**Why it fails:** MD040 requires language specification for syntax highlighting

**Better:**

````markdown
```javascript
code here
```
````

## Pitfall #3: Using Indented Code Blocks

**Problem:** Using indentation instead of fences

```markdown
Some text

    code here
    more code
```

**Why it fails:** MD046 requires fenced code blocks (our style setting)

**Better:**

````markdown
Some text

```javascript
code here
more code
```
````

## Pitfall #4: Trailing Whitespace

**Problem:** Invisible spaces at end of lines (hard to spot)

**Why it fails:** MD009 - trailing spaces can cause rendering issues

**Better:** Configure editor to show/remove trailing whitespace automatically

## Pitfall #5: No Blank Lines Around Elements

**Problem:**

```markdown
# Heading
Content immediately after
- List item
More content
```

**Why it fails:** MD022, MD032 require spacing for readability

**Better:**

```markdown
# Heading

Content with proper spacing

- List item

More content
```

## Pitfall #6: Disallowed Inline HTML

**Problem:** Using HTML elements not in our allowed list

```markdown
This is <span style="color: red">red text</span>
```

**Why it fails:** MD033 - only specific elements are allowed

**Better:** Use markdown emphasis or allowed HTML elements:

```markdown
This is **important text**
Use <kbd>Ctrl</kbd>+<kbd>C</kbd> to copy
```

## Pitfall #7: Skipping Heading Levels

**Problem:**

```markdown
# Main Heading

### Subheading (skipped H2)
```

**Why it fails:** MD001 requires proper heading hierarchy

**Better:**

```markdown
# Main Heading

## Section Heading

### Subheading
```

## Pitfall #8: Multiple Top-Level Headings

**Problem:**

```markdown
# Introduction

Some content

# Another Top-Level Heading
```

**Why it fails:** MD025 requires single H1 per document

**Better:**

```markdown
# Introduction

## Another Section Heading
```

## Pitfall #9: Bare URLs

**Problem:**

```markdown
Check out https://example.com for more info
```

**Why it fails:** MD034 requires proper link syntax

**Better:**

```markdown
Check out <https://example.com> or [Example Site](https://example.com) for more info
```

## Pitfall #10: Inconsistent List Markers

**Problem:**

```markdown
- Item one
* Item two
- Item three
```

**Why it fails:** MD004 requires consistent list markers

**Better:**

```markdown
- Item one
- Item two
- Item three
```
