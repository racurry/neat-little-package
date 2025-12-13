# Markdownlint Rules Reference

Complete reference of markdownlint rules enforced in our configuration.

## Rules Enforced

| Rule  | Description                             | Fix                                         |
| ----- | --------------------------------------- | ------------------------------------------- |
| MD001 | Heading levels increment by one         | Don't skip from H1 to H3                    |
| MD003 | Heading style (ATX vs setext)           | Use `#` syntax consistently                 |
| MD004 | List marker style                       | Use consistent markers (all `-` or all `*`) |
| MD007 | List indentation                        | Use 2 or 4 spaces consistently              |
| MD009 | No trailing spaces                      | Remove spaces at line ends                  |
| MD012 | No multiple blank lines                 | Use single blank lines                      |
| MD018 | Space after hash in heading             | `# Heading` not `#Heading`                  |
| MD019 | Multiple spaces after hash              | Use single space after `#`                  |
| MD022 | Headings surrounded by blank lines      | Add blank lines before/after                |
| MD024 | Duplicate headings (siblings only)      | OK if not siblings                          |
| MD025 | Single H1 per document                  | Only one top-level heading                  |
| MD026 | No trailing punctuation in headings     | Remove `!?.` from headings                  |
| MD030 | Space after list marker                 | `- Item` not `-Item`                        |
| MD031 | Code blocks surrounded by blank lines   | Add spacing around code                     |
| MD032 | Lists surrounded by blank lines         | Add spacing around lists                    |
| MD033 | Inline HTML (specific elements allowed) | Use allowed elements only                   |
| MD037 | No spaces inside emphasis               | `**text**` not `** text **`                 |
| MD040 | Code blocks should specify language     | Add language to \`\`\` blocks               |
| MD046 | Code block style (fenced only)          | Use \`\`\` not indentation                  |
| MD047 | Single trailing newline                 | Files must end with newline                 |
| MD049 | Emphasis style consistency              | Use consistent `*` or `_` style             |
| MD050 | Strong emphasis style consistency       | Use consistent `**` or `__` style           |

## Disabled Rules

| Rule  | Description        | Why Disabled                         |
| ----- | ------------------ | ------------------------------------ |
| MD013 | Line length        | Write naturally, no arbitrary limits |
| MD041 | First line heading | Badges, images, etc. are fine at top |

## Rule Categories

**Heading rules:** MD001, MD003, MD018, MD019, MD022, MD024, MD025, MD026

**List rules:** MD004, MD007, MD030, MD032

**Code block rules:** MD031, MD040, MD046

**Whitespace rules:** MD009, MD012, MD047

**Inline rules:** MD033, MD034, MD037, MD049, MD050

## Complete Rule Documentation

For detailed explanations of each rule:

<https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md>
