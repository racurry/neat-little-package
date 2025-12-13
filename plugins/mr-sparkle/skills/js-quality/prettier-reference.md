# Prettier Reference

This document provides practical reference for using Prettier in JavaScript and TypeScript projects.

## What is Prettier?

Prettier is an opinionated code formatter that enforces a consistent style across your codebase. Unlike linters that catch bugs, Prettier focuses purely on formatting.

**Key characteristics:**

- **Opinionated:** Minimal configuration, strong defaults
- **Multi-language:** JavaScript, TypeScript, JSX, JSON, CSS, Markdown, etc.
- **AST-based:** Parses and reprints code (safe transformations)
- **Consistent:** Same input always produces same output
- **Integrates:** Works alongside ESLint, supports editor integration

**Philosophy:** "You press save and code is formatted. No need to discuss style in code review."

## Command Overview

```bash
# Format file
prettier --write file.js

# Check formatting (no changes)
prettier --check file.js

# Format multiple files
prettier --write "src/**/*.{js,ts,jsx,tsx}"

# Format stdin
echo "const x=1" | prettier --parser babel
```

**Most common:** `prettier --write` (formats and saves)

## Configuration Files

Prettier looks for config in this order:

1. `prettier.config.js` (or `.cjs`, `.mjs`)
2. `.prettierrc` (JSON or YAML)
3. `.prettierrc.json`
4. `.prettierrc.yaml` (or `.yml`)
5. `.prettierrc.toml`
6. `package.json` (in `"prettier"` key)

**Recommended:** `.prettierrc` (JSON format) or `prettier.config.js` (for dynamic config)

## Core Configuration Options

### Print Width

```json
{
  "printWidth": 80
}
```

**Default:** 80

**What it does:** Line length where Prettier will try to wrap

**Common values:**

- `80` - Traditional (default)
- `100` - Modern balance
- `120` - Wider screens

### Tab Width

```json
{
  "tabWidth": 2
}
```

**Default:** 2

**What it does:** Number of spaces per indentation level

### Tabs vs Spaces

```json
{
  "useTabs": false
}
```

**Default:** `false` (uses spaces)

**When true:** Uses tabs instead of spaces

### Semicolons

```json
{
  "semi": true
}
```

**Default:** `true`

**Options:**

- `true` - Add semicolons everywhere
- `false` - Only add when required (ASI edge cases)

**Examples:**

```javascript
// semi: true
const x = 1;
const y = 2;

// semi: false
const x = 1
const y = 2
```

### Quotes

```json
{
  "singleQuote": false
}
```

**Default:** `false` (double quotes)

**Options:**

- `false` - Use double quotes
- `true` - Use single quotes

**Examples:**

```javascript
// singleQuote: false
const message = "Hello world";

// singleQuote: true
const message = 'Hello world';
```

### Trailing Commas

```json
{
  "trailingComma": "es5"
}
```

**Default:** `"es5"`

**Options:**

- `"none"` - No trailing commas
- `"es5"` - Trailing commas where valid in ES5 (objects, arrays)
- `"all"` - Trailing commas everywhere possible (includes function params)

**Examples:**

```javascript
// trailingComma: "none"
const obj = {
  a: 1,
  b: 2
};

// trailingComma: "es5"
const obj = {
  a: 1,
  b: 2,
};

// trailingComma: "all"
function foo(
  a,
  b,
) {
  return a + b;
}
```

### Bracket Spacing

```json
{
  "bracketSpacing": true
}
```

**Default:** `true`

**Examples:**

```javascript
// bracketSpacing: true
import { foo } from 'bar';
const obj = { a: 1 };

// bracketSpacing: false
import {foo} from 'bar';
const obj = {a: 1};
```

### Arrow Function Parentheses

```json
{
  "arrowParens": "always"
}
```

**Default:** `"always"`

**Options:**

- `"always"` - Always include parentheses
- `"avoid"` - Omit when possible (single argument)

**Examples:**

```javascript
// arrowParens: "always"
const fn = (x) => x * 2;

// arrowParens: "avoid"
const fn = x => x * 2;
```

### End of Line

```json
{
  "endOfLine": "lf"
}
```

**Default:** `"lf"`

**Options:**

- `"lf"` - Unix line endings (\\n)
- `"crlf"` - Windows line endings (\\r\\n)
- `"cr"` - Old Mac line endings (\\r)
- `"auto"` - Maintain existing (dangerous, can cause inconsistency)

## Common Configuration Patterns

### Minimal (Uses Defaults)

```json
{}
```

Prettier works perfectly with zero configuration.

### Modern JavaScript Project

```json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

### TypeScript Project

```json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "trailingComma": "all",
  "arrowParens": "always"
}
```

### Team Preferences (Example)

```json
{
  "printWidth": 120,
  "tabWidth": 4,
  "useTabs": false,
  "semi": false,
  "singleQuote": true,
  "trailingComma": "all",
  "arrowParens": "avoid"
}
```

## Ignoring Files

Create `.prettierignore` (same syntax as `.gitignore`):

```
# .prettierignore
dist/
build/
coverage/
node_modules/
*.min.js
package-lock.json
```

## Ignoring Code

### Ignore Next Statement

```javascript
// prettier-ignore
const ugly = {a:1,b:2,c:3};
```

### Ignore Range

```javascript
// prettier-ignore-start
const ugly1 = {a:1,b:2};
const ugly2 = {c:3,d:4};
// prettier-ignore-end
```

### Ignore File

```javascript
// prettier-ignore-file
```

At the top of the file.

## Integration with ESLint

**Critical:** Prettier handles formatting, ESLint handles code quality. They must not conflict.

### Setup

**Install:**

```bash
npm install --save-dev prettier eslint-config-prettier
```

**ESLint config:**

```javascript
// eslint.config.js
import prettier from "eslint-config-prettier";

export default [
  // ... other configs
  prettier, // Disables ESLint formatting rules
  {
    rules: {
      // Only code quality rules
    }
  }
];
```

### Run Both Tools

```json
{
  "scripts": {
    "lint": "eslint --fix . && prettier --write ."
  }
}
```

**Order matters:**

1. ESLint first (fixes code quality)
2. Prettier second (formats result)

## Integration with Package.json

```json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  },
  "devDependencies": {
    "prettier": "^3.0.0"
  }
}
```

## Editor Integration

Prettier works best with editor integration for format-on-save:

**VS Code:** Install "Prettier - Code formatter" extension

```json
// .vscode/settings.json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true
}
```

**Other editors:** Check Prettier docs for Vim, Emacs, Sublime, etc.

## Language-Specific Options

### JavaScript/TypeScript

```json
{
  "semi": true,
  "singleQuote": true,
  "arrowParens": "avoid"
}
```

### JSX/TSX

```json
{
  "jsxSingleQuote": false,
  "jsxBracketSameLine": false
}
```

**Example:**

```jsx
// jsxSingleQuote: false
<Component message="hello" />

// jsxSingleQuote: true
<Component message='hello' />
```

### JSON

```json
{
  "trailingComma": "none"
}
```

JSON doesn't allow trailing commas, Prettier handles this automatically.

### Markdown

```json
{
  "proseWrap": "preserve"
}
```

**Options:**

- `"preserve"` - Keep line breaks as-is (recommended)
- `"always"` - Wrap prose at printWidth
- `"never"` - Never wrap

## Common Issues

### Prettier and ESLint Fighting

**Cause:** ESLint has formatting rules enabled

**Fix:** Use `eslint-config-prettier`

```bash
npm install --save-dev eslint-config-prettier
```

```javascript
// eslint.config.js
import prettier from "eslint-config-prettier";

export default [
  prettier, // Disables conflicting rules
];
```

### Inconsistent Formatting Across Team

**Cause:** Different Prettier versions or configs

**Fix:**

1. Commit `.prettierrc` to version control
2. Pin Prettier version in `package.json`
3. Use pre-commit hooks to enforce

### Code Formatted Differently Than Expected

**Cause:** Prettier is opinionated, may not match your preference

**Fix:**

1. Check if there's a config option for your preference
2. If no option exists, accept Prettier's choice (by design)
3. Use `// prettier-ignore` sparingly for edge cases

### Prettier Formats Markdown Weirdly

**Cause:** `proseWrap` setting

**Fix:**

```json
{
  "proseWrap": "preserve"
}
```

## Philosophy: Why So Opinionated?

Prettier intentionally has **few options** to:

1. **Eliminate bikeshedding** - No style debates
2. **Consistency** - Same style everywhere
3. **Focus on code** - Not formatting

**Result:** You might not love every choice, but you'll never argue about it.

## When to Use Prettier

**Great fit:**

- ✅ Want consistent formatting across team
- ✅ Tired of style debates
- ✅ Need multi-language formatting
- ✅ Want editor integration
- ✅ Using with ESLint (let each tool do its job)

**Consider alternatives:**

- ❌ Want single tool for linting + formatting (use Biome)
- ❌ Need highly customized formatting (Prettier is opinionated)

## Further Reading

For specific options, edge cases, or advanced usage, fetch:

- <https://prettier.io/docs/en/options> - All configuration options
- <https://prettier.io/docs/en/integrations> - Editor and tool integrations
- <https://prettier.io/docs/en/ignore> - Ignoring code
