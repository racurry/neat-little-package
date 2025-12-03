# Biome Reference

This document provides practical reference for using Biome in JavaScript and TypeScript projects.

## What is Biome?

Biome is a modern, fast toolchain for web development written in Rust. It combines linting and formatting into a single tool with zero configuration required.

**Key characteristics:**

- **Unified:** Replaces ESLint + Prettier with one tool
- **Fast:** 10-100x faster than ESLint (Rust-based)
- **Compatible:** Mostly compatible with Prettier formatting
- **TypeScript-native:** Built-in TypeScript support
- **Zero-config:** Works out of the box with sensible defaults

## Command Overview

```bash
# Check and fix (linting + formatting in one pass)
biome check --fix <file>

# Just check (no modifications)
biome check <file>

# Format only
biome format --write <file>

# Lint only
biome lint --fix <file>
```

**Most common:** `biome check --fix` (does everything)

## Rule Categories

Biome organizes rules into logical categories:

### Core Categories

**`recommended`** - Essential rules everyone should use

- Catches common mistakes
- Enforces best practices
- Safe to enable by default

**`correctness`** - Code correctness issues

- Detects logical errors
- Prevents runtime bugs
- Example: unused variables, invalid regex

**`suspicious`** - Potentially problematic code

- Patterns that might indicate bugs
- Unclear or confusing code
- Example: double negation, console statements

**`complexity`** - Code complexity issues

- Overly complex expressions
- Unnecessary nesting
- Example: excessive boolean complexity

**`style`** - Code style preferences

- Naming conventions
- Code organization
- Example: use template literals instead of concatenation

**`performance`** - Performance issues

- Inefficient patterns
- Memory leaks
- Example: accumulator initialization

**`security`** - Security vulnerabilities

- Dangerous patterns
- Potential exploits
- Example: dangerous dangerouslySetInnerHTML usage

**`a11y`** (accessibility) - Accessibility issues

- ARIA attributes
- Semantic HTML
- Example: missing alt text on images

## Common Configuration Patterns

### Minimal (Recommended Start)

```json
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "formatter": {
    "enabled": true
  }
}
```

### Customizing Formatter

```json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100,
    "lineEnding": "lf"
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "asNeeded",
      "trailingCommas": "es5",
      "arrowParentheses": "asNeeded"
    }
  }
}
```

### Enabling Specific Rule Categories

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "correctness": { "all": true },
      "suspicious": { "all": true },
      "complexity": { "all": true },
      "style": { "all": true }
    }
  }
}
```

### Configuring Individual Rules

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "suspicious": {
        "noExplicitAny": "warn",
        "noConsole": "off"
      },
      "style": {
        "useTemplate": "error"
      }
    }
  }
}
```

**Rule severity levels:**

- `"error"` - Fails check, must be fixed
- `"warn"` - Warning, doesn't fail check
- `"off"` - Disabled
- `{ "level": "error", "fix": "safe" }` - Auto-fix only safe transformations

### TypeScript-Specific Configuration

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "suspicious": {
        "noExplicitAny": "warn"
      }
    }
  },
  "typescript": {
    "formatter": {
      "quoteStyle": "single"
    }
  }
}
```

### Ignoring Files

```json
{
  "files": {
    "ignore": [
      "dist/**",
      "build/**",
      "node_modules/**",
      "**/*.min.js"
    ]
  }
}
```

### Per-Directory Overrides

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "overrides": [
    {
      "include": ["test/**"],
      "linter": {
        "rules": {
          "suspicious": {
            "noConsole": "off"
          }
        }
      }
    }
  ]
}
```

## Common Rules Reference

### Frequently Used Rules

**`noUnusedVariables`** (suspicious)

```javascript
// ❌ Error
const unused = 5;

// ✅ OK
const used = 5;
console.log(used);

// ✅ OK - prefix with underscore to indicate intentionally unused
const _unused = 5;
```

**`noConsole`** (suspicious)

```javascript
// ❌ Warn/Error (depending on config)
console.log("debug info");

// ✅ OK - use proper logging
logger.info("application message");
```

**`noExplicitAny`** (suspicious - TypeScript)

```typescript
// ❌ Warn
function process(data: any) {
  return data;
}

// ✅ OK
function process(data: unknown) {
  return data;
}
```

**`useTemplate`** (style)

```javascript
// ❌ Prefer template
const msg = "Hello, " + name + "!";

// ✅ Better
const msg = `Hello, ${name}!`;
```

**`noVar`** (style)

```javascript
// ❌ Don't use var
var count = 0;

// ✅ Use const/let
const count = 0;
```

### Inline Comments to Disable Rules

```javascript
// Disable for next line
// biome-ignore lint/suspicious/noConsole: debugging
console.log("debug");

// Disable for entire file (at top)
/* biome-ignore lint/suspicious/noConsole */
```

## Integration with Package.json

```json
{
  "scripts": {
    "lint": "biome check .",
    "lint:fix": "biome check --fix .",
    "format": "biome format --write ."
  },
  "devDependencies": {
    "@biomejs/biome": "^2.0.0"
  }
}
```

## Migration from ESLint/Prettier

### Step 1: Install Biome

```bash
npm install --save-dev @biomejs/biome
```

### Step 2: Create biome.json

Start with recommended rules:

```json
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2
  }
}
```

### Step 3: Match Your Prettier Config

If you had:

```json
// .prettierrc
{
  "singleQuote": true,
  "semi": false,
  "printWidth": 100
}
```

Convert to:

```json
// biome.json
{
  "formatter": {
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "asNeeded"
    }
  }
}
```

### Step 4: Test and Adjust

```bash
# Run check to see what changes
biome check .

# Apply fixes
biome check --fix .
```

### Step 5: Remove Old Tools (Optional)

Once confident:

```bash
npm uninstall eslint prettier
# Remove .eslintrc.*, .prettierrc.*
```

## Performance Tips

**Biome is already fast**, but you can optimize further:

- Use `--changed` flag to only check modified files
- Ignore large directories in `biome.json` (node_modules, dist)
- Run in parallel with other tasks (won't block)

## Common Issues

### "Unknown rule" error

**Cause:** Rule name typo or rule doesn't exist in Biome

**Fix:** Check official docs for correct rule name

### Formatting differs from Prettier

**Cause:** Biome is "mostly" compatible but has some differences

**Fix:**

- Accept the difference (Biome's choice is usually good)
- Adjust `biome.json` formatter options
- If critical, stick with Prettier

### TypeScript errors in JavaScript files

**Cause:** Biome checks types even in `.js` files if TypeScript is detected

**Fix:**

- Rename to `.ts` if it's actually TypeScript
- Configure overrides for `.js` files
- Disable specific TypeScript rules for JS

## When to Use Biome

**Great fit:**

- ✅ New projects
- ✅ TypeScript projects
- ✅ Large codebases (speed matters)
- ✅ Want simpler tooling (one tool vs many)
- ✅ Don't need specific ESLint plugins

**Maybe not:**

- ❌ Need specific ESLint plugins (React-specific rules, etc.)
- ❌ Team strongly prefers ESLint ecosystem
- ❌ Complex existing ESLint config you can't replicate

## Further Reading

For specific rule details, configuration options, or advanced usage, fetch:

- <https://biomejs.dev/linter/> - Complete rule reference
- <https://biomejs.dev/formatter/> - Formatter options
- <https://biomejs.dev/guides/migrate/> - Migration guides
