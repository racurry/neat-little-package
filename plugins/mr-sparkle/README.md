# Mr. Sparkle Plugin

![Mr. Sparkle](./assets/mr-sparkle.png)

Automated code quality enforcement with linting and auto-formatting for Claude Code.

## Supported Languages

| Language | Tool | Commands | Skill |
|----------|------|----------|-------|
| Markdown | [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) | `/mr-sparkle:lint-md`, `/mr-sparkle:fix-md` | `markdown-quality` |

## Features

- **Automatic Linting**: PostToolUse hook that runs after every Write/Edit operation
- **Manual Commands**: Slash commands for on-demand linting and fixing
- **Best Practices Skills**: Comprehensive guidance on formatting rules and conventions
- **Non-Blocking**: Linting failures don't prevent file operations
- **Extensible**: Designed to support multiple languages and linters

## Installation

### 1. Install the Plugin

Add the mr-sparkle plugin to your Claude Code environment:

```bash
/plugin install mr-sparkle@neat-little-package
```

Or add manually by copying the plugin directory to your `.claude/plugins/` folder.

### 2. Install Required Tools

Install the linting tools for the languages you want to use. See the [Supported Languages](#supported-languages) table for specific tools.

**Example (Markdown):**

```bash
npm install -g markdownlint-cli2
```

**Verification:**

```bash
markdownlint-cli2 --version
```

### 3. Optional: Configure Rules

Each linter may support configuration files in your project root. See language-specific skills for configuration guidance.

## Components

### Hook: Automatic Linting

**Event:** PostToolUse (Write, Edit)

**Behavior:**

- Detects supported file types based on extension
- Runs appropriate linter with auto-fix automatically
- Shows success feedback when files are formatted
- Reports unfixable issues without blocking
- Gracefully skips if linter tools not installed

**Example output:**

```text
Formatted successfully: docs/api.md
```

**Example output (when issues can't be auto-fixed):**

```text
Linting found unfixable issues in src/app.js:
  line 42: Missing semicolon
Run: eslint src/app.js to see details
```

### Commands: `/mr-sparkle:lint-{lang}` and `/mr-sparkle:fix-{lang}`

Each supported language has two commands:

**Lint command** - Inspect files for linting issues without making changes

**Usage pattern:**

```bash
/mr-sparkle:lint-{lang}                # Lint current directory
/mr-sparkle:lint-{lang} path/          # Lint specific directory
/mr-sparkle:lint-{lang} file.ext       # Lint specific file
```

**Fix command** - Automatically fix linting issues

**Usage pattern:**

```bash
/mr-sparkle:fix-{lang}                 # Fix current directory
/mr-sparkle:fix-{lang} path/           # Fix specific directory
/mr-sparkle:fix-{lang} file.ext        # Fix specific file
```

See the [Supported Languages](#supported-languages) table for available commands.

### Skills

Each supported language has an associated skill providing:

- Linting rules and their interpretations
- Configuration options and examples
- When to use each command
- Troubleshooting guide
- Quality checklist

See the [Supported Languages](#supported-languages) table for available skills.

## Usage Examples

### Scenario 1: Creating New Files

```text
User: Create a new API documentation file

Claude: [Creates docs/api.md with content]

[Hook automatically runs linter and applies fixes]
Formatted successfully: docs/api.md
```

### Scenario 2: Manual Review Before Commit

```bash
/mr-sparkle:lint-md docs/

# Review output showing issues
# Fix any that require manual attention
# Run again to verify clean
```

### Scenario 3: Batch Fixing Existing Files

```bash
/mr-sparkle:fix-md .

# All files in project are fixed
# Review git diff to see changes
# Commit the improvements
```

### Scenario 4: Understanding a Linting Error

```text
User: Why is the linter complaining about this?

Claude: [Loads appropriate skill]
[Explains the rule and provides guidance]
```

## Hook Behavior Details

### What Gets Linted

**Included:**

- Files with extensions matching supported languages
- Files created or modified via Write or Edit tools

**Excluded:**

- Files without supported extensions
- Files in `.git/`, `node_modules/`, etc. (via linter defaults)
- Binary files
- Hidden files (unless explicitly edited)

### Performance

- **Timeout:** 30 seconds (configurable in hooks.json)
- **Typical execution:** < 1 second for most files
- **Large files:** May take longer but won't block operations

### Error Handling

**Linter not installed:**

- Hook exits silently (exit 0)
- No error messages
- File operations complete normally

**Linting succeeds:**

- Hook exits with code 0
- Shows success message with file path
- File is properly formatted

**Linting finds fixable issues:**

- Issues are automatically corrected
- Hook exits with code 0
- File is modified with fixes
- Success message displayed

**Linting finds unfixable issues:**

- Hook reports to stderr (non-blocking error)
- Shows actual linter output
- Hook exits with code 1
- File operations complete
- User is notified to review manually

## Troubleshooting

### Hook Not Running

**Symptom:** Files are created but not linted

**Solutions:**

1. **Check if linter tool is installed:**

   ```bash
   which <tool-name>
   <tool-name> --version
   ```

   If not found, install the appropriate tool (see [Supported Languages](#supported-languages))

2. **Verify plugin is enabled:**
   Check that mr-sparkle appears in `/plugin list`

3. **Check file extension:**
   Only files with supported extensions are processed

4. **View hook execution in transcript mode:**
   Press `CTRL-R` in Claude Code to see hook output

### Issues Not Auto-Fixed

**Symptom:** Hook reports issues remain after running

**Explanation:** Some rules require manual judgment based on code context

**Solution:**

1. Run the appropriate lint command to see specific issues
2. Review the language-specific skill for guidance
3. Fix manually based on context
4. Consider disabling the rule if it doesn't apply to your project

### Configuration Not Applied

**Symptom:** Custom rules in configuration file are ignored

**Solutions:**

1. **Check file location:** Must be in project root
2. **Validate syntax:** Use appropriate validator for config file format
3. **Check rule identifiers:** Must match official rule names for that linter
4. **Restart Claude Code:** Configuration is loaded at startup

### Permission Issues

**Symptom:** Hook fails with permission denied

**Solution:**

```bash
chmod +x plugins/mr-sparkle/hooks/*.sh
```

## Future Roadmap

The mr-sparkle plugin is designed to expand to multiple languages:

### Planned Language Support

- **JavaScript/TypeScript**: ESLint integration
- **Python**: pylint, flake8, or ruff integration
- **Go**: gofmt, golangci-lint integration
- **Rust**: rustfmt, clippy integration
- **JSON/YAML**: Schema validation

### Planned Features

- **Pre-commit integration**: Run all linters before commits
- **Configuration UI**: Slash command to configure rules interactively
- **Custom rule sets**: Team-specific linting profiles
- **Performance monitoring**: Track linting speed and optimization
- **Editor integration**: Apply fixes directly in IDE

### Extensibility

The plugin architecture supports:

- Multiple linters per language
- Language-specific configuration
- Custom linter integration
- Conditional linting based on project type

## Testing Section - Updated Again

This section tests the hook output to see if it actually runs.
