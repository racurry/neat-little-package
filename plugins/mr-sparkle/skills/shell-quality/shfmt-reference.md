# shfmt Reference

Detailed guide to shfmt shell script formatting options and configuration.

## Overview

shfmt formats shell scripts with consistent style. It uses `.editorconfig` files for configuration, following the EditorConfig standard.

**Official documentation:** <https://github.com/mvdan/sh>

## Command-Line Usage

**Basic formatting:**

```bash
shfmt script.sh           # Print formatted to stdout
shfmt -w script.sh        # Write changes to file
shfmt -d script.sh        # Show diff without writing
```

**Common flags:**

- `-i <num>` - Indent with N spaces (0 = tabs)
- `-bn` - Binary ops (`&&`, `||`) may start lines
- `-ci` - Indent switch cases
- `-sr` - Add space after redirect operators
- `-kp` - Keep padding in column alignment
- `-fn` - Function opening brace on next line

**Language selection:**

- `-ln bash` - Bash (default)
- `-ln posix` - POSIX shell
- `-ln mksh` - MirBSD Korn shell

## EditorConfig Integration

shfmt reads formatting preferences from `.editorconfig` files:

**Example configuration:**

```ini
# .editorconfig
root = true

[*.sh]
indent_style = space
indent_size = 2
binary_next_line = true
switch_case_indent = true
```

**EditorConfig properties shfmt understands:**

| Property | Values | shfmt Flag Equivalent |
|----------|--------|----------------------|
| `indent_style` | `space`, `tab` | `-i 0` (tab) or `-i N` (space) |
| `indent_size` | number | `-i N` |
| `binary_next_line` | `true`, `false` | `-bn` |
| `switch_case_indent` | `true`, `false` | `-ci` |
| `space_redirects` | `true`, `false` | `-sr` |
| `keep_padding` | `true`, `false` | `-kp` |
| `function_next_line` | `true`, `false` | `-fn` |

**Command-line flags override EditorConfig settings.**

## Formatting Examples

### Indentation

**2-space indentation:**

```bash
# Input
if [ -f file ]; then
echo "exists"
fi

# Output (indent_size = 2)
if [ -f file ]; then
  echo "exists"
fi
```

**Tab indentation:**

```bash
# .editorconfig: indent_style = tab
if [ -f file ]; then
→ echo "exists"
fi
```

### Binary Operators

**Default (operator at end of line):**

```bash
if [ "$status" = "ok" ] &&
  [ "$count" -gt 0 ]; then
  echo "valid"
fi
```

**With `-bn` (operator at start of line):**

```bash
if [ "$status" = "ok" ] \
  && [ "$count" -gt 0 ]; then
  echo "valid"
fi
```

### Switch/Case Indentation

**Without `-ci`:**

```bash
case "$action" in
start)
  echo "starting"
  ;;
stop)
  echo "stopping"
  ;;
esac
```

**With `-ci`:**

```bash
case "$action" in
  start)
    echo "starting"
    ;;
  stop)
    echo "stopping"
    ;;
esac
```

### Redirect Spacing

**Without `-sr`:**

```bash
echo "output" >file.txt
cat <input.txt
```

**With `-sr`:**

```bash
echo "output" > file.txt
cat < input.txt
```

### Function Formatting

**Default (opening brace on same line):**

```bash
function myFunc() {
  echo "hello"
}
```

**With `-fn` (opening brace on next line):**

```bash
function myFunc()
{
  echo "hello"
}
```

## Configuration Patterns

### Minimal (Recommended)

Start with basic indentation only:

```ini
# .editorconfig
root = true

[*.sh]
indent_style = space
indent_size = 2
```

### Consistent with Google Shell Style

```ini
[*.sh]
indent_style = space
indent_size = 2
binary_next_line = false
switch_case_indent = true
```

### Allman Brace Style

```ini
[*.sh]
indent_style = tab
function_next_line = true
```

### Team Standardization Example

```ini
root = true

# All shell scripts
[*.{sh,bash}]
indent_style = space
indent_size = 2
binary_next_line = true
switch_case_indent = true
space_redirects = false

# Build scripts specifically
[scripts/build/*.sh]
indent_size = 4
```

## Best Practices

**Let shfmt handle:**

- ✅ All indentation (don't manually indent)
- ✅ Spacing around operators
- ✅ Alignment of case statements
- ✅ Line continuation consistency

**You handle:**

- ❌ Logic and correctness
- ❌ Variable naming
- ❌ Comment content

**EditorConfig placement:**

- Put `.editorconfig` at project root
- Use `root = true` to prevent searching parent directories
- Be consistent across all scripts in project

**Testing configuration:**

```bash
# Test formatting without writing
shfmt -d script.sh

# Apply and review diff
git diff
```

**Integration:**

- Run shfmt before committing (pre-commit hook)
- Run on save in editor (if supported)
- Include in CI/CD formatting checks

## Troubleshooting

**shfmt makes unexpected changes:**

1. Check for `.editorconfig` in parent directories
2. Verify indent_style/indent_size settings
3. Use `shfmt -d` to preview changes before applying

**shfmt refuses to format:**

- Likely syntax error in script
- Run `bash -n script.sh` to check syntax
- Fix syntax errors first, then format

**Conflicting with editor formatting:**

- Disable editor's shell formatting
- Let shfmt be the single source of truth
- Configure editor to run shfmt on save

## Related Tools

**Use with shellcheck:**

1. Run shfmt first (formatting)
2. Run shellcheck second (linting)
3. This order prevents formatting from affecting analysis

**EditorConfig plugins:**

- Most editors have EditorConfig plugins
- shfmt reads same `.editorconfig` as editor
- Consistent formatting in editor and CLI

## Further Reading

- Official repository: <https://github.com/mvdan/sh>
- EditorConfig spec: <https://editorconfig.org/>
- Shell formatting discussions: <https://github.com/mvdan/sh/issues>
