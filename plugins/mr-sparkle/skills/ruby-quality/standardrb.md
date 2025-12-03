# StandardRB Overview

StandardRB is a zero-configuration Ruby style guide, linter, and formatter.

## Philosophy

**"No configuration, just use it"**

StandardRB takes the decision-making out of code style. It's built on RuboCop's engine but provides a curated, opinionated rule set that you don't configure. The goal is to eliminate bikeshedding and "just make code consistent."

**Core principles:**

1. **Zero config** - No decisions to make, just run it
2. **Opinionated** - Makes style choices for you
3. **Automatic fixing** - Fixes issues automatically where possible
4. **Based on community consensus** - Curated from Ruby style guide

## Key Features

**Simplicity:**

- No configuration file needed (though `.standard.yml` is possible for minimal overrides)
- One command to check: `standardrb`
- One command to fix: `standardrb --fix`

**Built on RuboCop:**

- Uses RuboCop's engine under the hood
- Carefully curated subset of cops
- Preconfigured for consistency
- Can coexist with RuboCop if needed (though not recommended)

**Auto-Fixing:**

- Most issues fixed automatically with `--fix`
- Safe transformations only
- No manual style decisions required

## Basic Usage

```bash
# Check all Ruby files
standardrb

# Auto-fix issues
standardrb --fix

# Check specific files
standardrb app/models/**/*.rb

# Generate todo file for existing codebase
standardrb --generate-todo
```

## Configuration (Minimal and Discouraged)

StandardRB's value is zero-config. If you need extensive configuration, use RuboCop instead.

**Minimal config example** (only if absolutely necessary):

```yaml
# .standard.yml
ignore:
  - 'vendor/**/*'
  - 'db/schema.rb'
```

See `configs/standard.yml` for minimal example.

**That's it.** StandardRB intentionally doesn't support extensive configuration. If you want to customize cop settings, you should use RuboCop directly.

## When to Use StandardRB

**Good fit for:**

- New projects with no legacy style constraints
- Teams that want to eliminate style debates
- "Just make it consistent" philosophy
- Fast onboarding (no config decisions)
- Projects migrating from no linting (easier adoption)
- Teams that value simplicity over customization

**Consider RuboCop instead if:**

- You have strong, specific style preferences
- Existing codebase with established conventions
- Need Rails/RSpec/other specific cops beyond Standard's set
- Want fine-grained control over rules

## StandardRB vs RuboCop

**StandardRB:**

- ✅ Zero configuration required
- ✅ Faster onboarding
- ✅ Eliminates bikeshedding
- ❌ Limited customization
- ❌ Smaller cop set

**RuboCop:**

- ✅ Highly configurable
- ✅ 500+ cops available
- ✅ Community extensions (rails, rspec, etc.)
- ❌ Requires configuration decisions
- ❌ Can lead to style debates

**Philosophy difference:**

- **StandardRB:** "Trust the curated defaults, don't configure"
- **RuboCop:** "Configure exactly what you want"

## Migrating from RuboCop to StandardRB

If you want to simplify:

1. Remove `.rubocop.yml` configuration
2. Add `standard` gem to Gemfile
3. Run `standardrb --generate-todo` for existing issues
4. Fix issues incrementally with `standardrb --fix`
5. Delete todo file when done

**Warning:** StandardRB's rules may differ from your RuboCop config. Review changes carefully.

## Official Documentation

For more details and philosophy:

<https://github.com/standardrb/standard>

For questions about why Standard makes certain choices:

<https://github.com/standardrb/standard/blob/main/docs/FAQ.md>
