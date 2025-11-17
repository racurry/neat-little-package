# Troubleshooting Guide

Common issues and solutions for markdownlint-cli2 and the code-quality plugin.

## Hook Not Running

**Symptoms:** Markdown files created but not linted

**Causes:**

1. markdownlint-cli2 not installed → Install with npm
2. Hook disabled in settings → Check `.claude/settings.json` or `.claude/hooks.json`
3. File extension not .md or .markdown → Rename file or update hook configuration
4. Hook script not executable → Check file permissions
5. Wrong working directory → Hook runs from project root

**Solution:**

```bash
# Install markdownlint-cli2 (using local/project npm)
npm install --save-dev markdownlint-cli2

# Or install globally (alternative)
npm install -g markdownlint-cli2

# Test manually
markdownlint-cli2 --fix yourfile.md

# Check hook configuration
cat .claude/hooks.json
```

## Unfixable Issues

**Symptoms:** Hook reports issues that remain after fixing

**Causes:**

1. Rule requires manual judgment (e.g., heading hierarchy, heading content)
2. Content violates multiple conflicting rules
3. Structural issues (missing language, wrong heading level)
4. Semantic issues (duplicate headings, improper nesting)

**Solution:** Run `/mr-sparkle:lint-md` to see detailed error messages, then fix manually

**Common unfixable issues:**

- Heading hierarchy violations (must restructure manually)
- Multiple H1 headings (decide which to demote)
- Missing code block language (must choose appropriate language)
- Duplicate heading content (reword one of them)

## Configuration Not Applied

**Symptoms:** Custom rules not taking effect

**Causes:**

1. Configuration file in wrong location (see file precedence below)
2. Invalid JSON syntax (use a JSON validator)
3. Wrong filename or precedence issue
4. Parent directory config overriding your settings
5. Cached configuration (stale)
6. Using markdownlint file instead of markdownlint-cli2 file

**Solution:**

```bash
# Validate JSON syntax
npx jsonlint .markdownlint-cli2.jsonc

# Check which config file is being used
markdownlint-cli2 --help  # Shows search order

# Test with explicit config
markdownlint-cli2 --config .markdownlint-cli2.jsonc "**/*.md"

# Debug config loading
markdownlint-cli2 yourfile.md 2>&1 | grep -i config
```

**File precedence reminder:**

1. `.markdownlint-cli2.jsonc` (highest priority, recommended)
2. `.markdownlint-cli2.yaml`
3. `.markdownlint.jsonc`
4. `.markdownlint.json`

For complete configuration details, fetch the official documentation: https://github.com/DavidAnson/markdownlint-cli2

## Linting Errors on Valid Markdown

**Symptoms:** Markdownlint reports errors on markdown that renders correctly

**Cause:** Markdown renderers are permissive; linters enforce stricter standards

**Solution:** This is expected behavior - linting enforces best practices even if renderers are forgiving

**Example:**

```markdown
#No space after hash - renders fine but fails MD018
```

Better to follow the standard for consistency.

## Performance Issues

**Symptoms:** Linting is slow on large repositories

**Solutions:**

1. Add appropriate ignore patterns to `.markdownlint-cli2.jsonc`
2. Use `.gitignore` integration (already enabled in our config)
3. Lint specific directories instead of entire tree
4. Exclude large generated files

```json
{
  "ignores": [
    "node_modules/**",
    "dist/**",
    "build/**",
    "**/*.min.md",
    "vendor/**"
  ]
}
```

## Command Not Found

**Symptoms:** `markdownlint-cli2: command not found`

**Causes:**

1. Not installed globally
2. npm global bin directory not in PATH
3. Installed locally instead of globally

**Solution:**

```bash
# Install globally
npm install -g markdownlint-cli2

# Or use npx (no installation needed)
npx markdownlint-cli2 "**/*.md"

# Or install locally and use npm scripts
npm install --save-dev markdownlint-cli2
# Then add to package.json scripts
```

## False Positives

**Symptoms:** Linter flags correct markdown as errors

**Solution:** If a rule doesn't fit your workflow, disable it in config:

```json
{
  "config": {
    "MD013": false  // Disable specific rule
  }
}
```

Or disable inline for specific cases:

```markdown
<!-- markdownlint-disable MD013 -->
This very long line won't be flagged
<!-- markdownlint-enable MD013 -->
```

## Hook Returns Non-Zero Exit

**Symptoms:** Hook fails and blocks Claude operations

**Cause:** Unfixable linting errors return exit code 1 (by design, non-blocking)

**Expected behavior:** The hook should report errors but NOT block the operation

**If blocking occurs:** Check hook configuration - should use `exit 1` (report) not `exit 2` (block)

## Getting Help

1. Check `pitfalls-reference.md` for common mistakes
2. Check `rules-reference.md` for rule details
3. Run `/mr-sparkle:lint-md` for detailed error messages
4. Visit <https://github.com/DavidAnson/markdownlint-cli2/issues>
5. Check markdownlint rules: <https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md>
