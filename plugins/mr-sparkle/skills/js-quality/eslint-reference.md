# ESLint Reference

This document provides practical reference for using ESLint in JavaScript and TypeScript projects.

## What is ESLint?

ESLint is a pluggable JavaScript linter that finds and fixes problems in your code. It's highly configurable with a vast plugin ecosystem.

**Key characteristics:**

- **Pluggable:** Extensive plugin ecosystem (React, Vue, TypeScript, etc.)
- **Configurable:** Fine-grained control over rules
- **Established:** Industry standard for JavaScript linting
- **Auto-fixable:** Many rules can automatically fix issues
- **Multi-language:** Supports JavaScript, TypeScript, JSX, TSX

## Command Overview

```bash
# Lint files
eslint file.js

# Lint with auto-fix
eslint --fix file.js

# Lint entire directory
eslint src/

# Lint with specific config
eslint --config custom.config.js file.js
```

**Most common:** `eslint --fix` (lints and fixes)

## Configuration Formats

### Modern: Flat Config (ESLint 9+, Recommended)

**File:** `eslint.config.js` (or `.mjs`, `.cjs`)

```javascript
export default [
  {
    files: ["**/*.js"],
    rules: {
      "no-unused-vars": "warn"
    }
  }
];
```

**Benefits:**

- JavaScript-based (dynamic configuration)
- Better TypeScript support
- Clearer override system
- Simplified configuration

### Legacy: `.eslintrc.*` (ESLint 8 and earlier)

**Files:** `.eslintrc`, `.eslintrc.js`, `.eslintrc.json`, `.eslintrc.yaml`

```json
{
  "rules": {
    "no-unused-vars": "warn"
  }
}
```

**Note:** ESLint 9+ ignores `.eslintrc.*` files unless configured to use them.

## Flat Config Patterns (Recommended)

### Basic Setup

```javascript
// eslint.config.js
export default [
  {
    rules: {
      "no-unused-vars": "warn",
      "no-console": "off"
    }
  }
];
```

### Using Recommended Configs

```javascript
// eslint.config.js
import js from "@eslint/js";

export default [
  js.configs.recommended,
  {
    rules: {
      // Override or add rules
      "no-console": "off"
    }
  }
];
```

### TypeScript Setup

```javascript
// eslint.config.js
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/no-unused-vars": "warn"
    }
  }
];
```

**Install packages:**

```bash
npm install --save-dev eslint typescript-eslint
```

### With Prettier (Disable Formatting Rules)

```javascript
// eslint.config.js
import js from "@eslint/js";
import prettier from "eslint-config-prettier";

export default [
  js.configs.recommended,
  prettier, // Disables ESLint formatting rules that conflict with Prettier
  {
    rules: {
      // Only code quality rules
      "no-unused-vars": "warn"
    }
  }
];
```

**Install package:**

```bash
npm install --save-dev eslint-config-prettier
```

### File-Specific Configuration

```javascript
// eslint.config.js
export default [
  {
    files: ["**/*.js"],
    rules: {
      "no-unused-vars": "warn"
    }
  },
  {
    files: ["**/*.test.js"],
    rules: {
      "no-console": "off" // Allow console in tests
    }
  }
];
```

### Ignoring Files

```javascript
// eslint.config.js
export default [
  {
    ignores: ["dist/**", "build/**", "node_modules/**"]
  },
  {
    files: ["**/*.js"],
    rules: {
      "no-unused-vars": "warn"
    }
  }
];
```

## Common Rules Reference

### Code Quality Rules

**`no-unused-vars`** - Disallow unused variables

```javascript
// ❌ Error
const unused = 5;

// ✅ OK
const used = 5;
console.log(used);

// ✅ OK - prefix with underscore
const _intentionallyUnused = 5;
```

**`no-undef`** - Disallow undefined variables

```javascript
// ❌ Error
console.log(undefinedVariable);

// ✅ OK
const definedVariable = 5;
console.log(definedVariable);
```

**`no-console`** - Disallow console statements

```javascript
// ❌ Warn/Error (depending on config)
console.log("debug");

// ✅ OK - use proper logging
logger.info("message");
```

**`prefer-const`** - Prefer const over let

```javascript
// ❌ Warn
let unchanging = 5;

// ✅ OK
const unchanging = 5;
```

**`no-var`** - Disallow var

```javascript
// ❌ Error
var count = 0;

// ✅ OK
const count = 0;
```

### Best Practices

**`eqeqeq`** - Require === instead of ==

```javascript
// ❌ Error
if (value == 5) { }

// ✅ OK
if (value === 5) { }
```

**`no-eval`** - Disallow eval()

```javascript
// ❌ Error
eval("code");

// ✅ OK - find safer alternative
```

**`curly`** - Require curly braces

```javascript
// ❌ Warn
if (condition) doSomething();

// ✅ OK
if (condition) {
  doSomething();
}
```

### TypeScript-Specific Rules

**`@typescript-eslint/no-explicit-any`** - Avoid any type

```typescript
// ❌ Warn
function process(data: any) { }

// ✅ OK
function process(data: unknown) { }
```

**`@typescript-eslint/no-unused-vars`** - TypeScript-aware unused vars

```typescript
// ❌ Error
const unused: string = "value";

// ✅ OK
const _unused: string = "value"; // Prefix with _
```

**`@typescript-eslint/explicit-function-return-type`** - Require return types

```typescript
// ❌ Warn (if enabled)
function calculate(x: number) {
  return x * 2;
}

// ✅ OK
function calculate(x: number): number {
  return x * 2;
}
```

## Rule Severity Levels

```javascript
{
  rules: {
    "no-console": "off",       // Disabled
    "no-unused-vars": "warn",  // Warning (doesn't fail)
    "no-undef": "error"        // Error (fails lint)
  }
}
```

**Array format for configuration:**

```javascript
{
  rules: {
    "max-len": ["error", { "code": 100 }],
    "quotes": ["warn", "single"],
    "indent": ["error", 2]
  }
}
```

## Inline Comments to Disable Rules

```javascript
// Disable for next line
// eslint-disable-next-line no-console
console.log("debug");

// Disable for entire file (at top)
/* eslint-disable no-console */

// Disable multiple rules
// eslint-disable-next-line no-console, no-undef
console.log(unknownVar);

// Disable for block
/* eslint-disable no-console */
console.log("debug 1");
console.log("debug 2");
/* eslint-enable no-console */
```

## Integration with Package.json

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint --fix ."
  },
  "devDependencies": {
    "eslint": "^9.0.0"
  }
}
```

## Popular Plugin Ecosystem

### React

```bash
npm install --save-dev eslint-plugin-react eslint-plugin-react-hooks
```

```javascript
// eslint.config.js
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";

export default [
  {
    plugins: {
      react,
      "react-hooks": reactHooks
    },
    rules: {
      "react/prop-types": "warn",
      "react-hooks/rules-of-hooks": "error"
    }
  }
];
```

### Vue

```bash
npm install --save-dev eslint-plugin-vue
```

### Import/Export

```bash
npm install --save-dev eslint-plugin-import
```

Helps with import order, unused imports, etc.

### Accessibility (a11y)

```bash
npm install --save-dev eslint-plugin-jsx-a11y
```

Checks accessibility in JSX.

## Migration from Legacy to Flat Config

### Step 1: Update ESLint

```bash
npm install --save-dev eslint@latest
```

### Step 2: Convert .eslintrc.json to eslint.config.js

**Before (.eslintrc.json):**

```json
{
  "extends": ["eslint:recommended"],
  "rules": {
    "no-console": "warn"
  },
  "env": {
    "node": true,
    "es2021": true
  }
}
```

**After (eslint.config.js):**

```javascript
import js from "@eslint/js";

export default [
  js.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "module",
      globals: {
        // Node.js globals
        process: "readonly",
        __dirname: "readonly"
      }
    },
    rules: {
      "no-console": "warn"
    }
  }
];
```

### Step 3: Test

```bash
eslint .
```

### Step 4: Remove Legacy Config

Once confident, remove `.eslintrc.*` files.

## Working with Prettier

**Critical:** ESLint and Prettier must not conflict.

### Recommended Setup

**Install:**

```bash
npm install --save-dev eslint prettier eslint-config-prettier
```

**ESLint config:**

```javascript
// eslint.config.js
import js from "@eslint/js";
import prettier from "eslint-config-prettier";

export default [
  js.configs.recommended,
  prettier, // Disables formatting rules
  {
    rules: {
      // Only code quality rules, no formatting
      "no-unused-vars": "warn"
    }
  }
];
```

**Run both tools:**

```bash
eslint --fix .    # Fix code quality issues
prettier --write . # Format code
```

**Or in package.json:**

```json
{
  "scripts": {
    "lint": "eslint --fix . && prettier --write ."
  }
}
```

## Common Issues

### "Failed to load config" error

**Cause:** Missing dependency or incorrect import

**Fix:** Ensure all plugins are installed

```bash
npm install --save-dev @eslint/js typescript-eslint
```

### Rules not applying

**Cause:** File pattern doesn't match

**Fix:** Check `files` pattern

```javascript
{
  files: ["**/*.{js,mjs,cjs,jsx,ts,tsx}"], // Broader pattern
  rules: { }
}
```

### Conflict with Prettier

**Cause:** ESLint formatting rules enabled

**Fix:** Use `eslint-config-prettier`

```bash
npm install --save-dev eslint-config-prettier
```

### TypeScript errors in .js files

**Cause:** TypeScript rules applied to JavaScript

**Fix:** Separate configurations

```javascript
export default [
  {
    files: ["**/*.js"],
    rules: {
      "no-unused-vars": "warn"
    }
  },
  {
    files: ["**/*.ts"],
    rules: {
      "@typescript-eslint/no-unused-vars": "warn"
    }
  }
];
```

## When to Use ESLint

**Great fit:**

- ✅ Need specific plugins (React, Vue, etc.)
- ✅ Highly customizable linting rules
- ✅ Established project with existing config
- ✅ Team familiar with ESLint ecosystem
- ✅ Need granular rule control

**Consider alternatives:**

- ❌ Want single tool for linting + formatting (use Biome)
- ❌ Performance is critical in large codebase (Biome is faster)
- ❌ Prefer simpler configuration (Biome has fewer options)

## Further Reading

For specific rule details, plugin documentation, or advanced usage, fetch:

- <https://eslint.org/docs/latest/> - Official ESLint documentation
- <https://typescript-eslint.io/> - TypeScript ESLint plugin
- <https://eslint.org/docs/latest/use/configure/configuration-files> - Flat config guide
