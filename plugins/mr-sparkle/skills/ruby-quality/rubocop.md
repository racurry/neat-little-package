# RuboCop Overview

RuboCop is a Ruby static code analyzer and formatter with extensive configuration capabilities.

## Philosophy

**"Highly configurable, community-driven style enforcement"**

RuboCop provides 500+ cops (rules) that you can enable, disable, and configure to match your team's exact preferences. It's designed for teams that want fine-grained control over their code style.

## Key Features

**Comprehensive Coverage:**

- **Style:** Code style and formatting (string quotes, spacing, etc.)
- **Layout:** Code layout and indentation
- **Lint:** Code quality and potential bugs
- **Metrics:** Code complexity (method length, cyclomatic complexity)
- **Naming:** Naming conventions (variables, methods, classes)
- **Performance:** Performance anti-patterns
- **Security:** Security vulnerabilities

**Auto-Correction:**

- `-a` flag: Safe auto-corrections (formatting, simple fixes)
- `-A` flag: All auto-corrections (includes potentially unsafe changes)

**Community Extensions:**

- `rubocop-rails` - Rails-specific cops
- `rubocop-rspec` - RSpec test cops
- `rubocop-performance` - Performance optimizations
- `rubocop-minitest` - Minitest cops
- Many more...

## Basic Usage

```bash
# Check all files
rubocop

# Check specific files/directories
rubocop app/models/**/*.rb

# Auto-fix safe issues
rubocop -a

# Auto-fix all issues (use with caution)
rubocop -A

# Only run specific cops
rubocop --only Style/StringLiterals

# Generate config for existing codebase
rubocop --auto-gen-config
```

## Configuration Example

See `configs/rubocop.yml` for a sensible default configuration.

**Minimal config:**

```yaml
AllCops:
  TargetRubyVersion: 3.2
  NewCops: enable

Style/StringLiterals:
  EnforcedStyle: single_quotes
```

**With community extensions:**

```yaml
require:
  - rubocop-rails
  - rubocop-rspec

AllCops:
  TargetRubyVersion: 3.2
  NewCops: enable

Rails:
  Enabled: true

RSpec:
  Enabled: true
```

## When to Use RuboCop

**Good fit for:**

- Teams with strong style opinions
- Existing codebases with established conventions
- Projects needing Rails/RSpec/other specific cops
- Organizations with published style guides
- Gradual linting adoption (via `.rubocop_todo.yml`)

**Consider StandardRB instead if:**

- You want zero configuration
- Style bikeshedding is a problem
- New project with no legacy constraints
- Team prefers "just make it consistent" over customization

## Common Configuration Patterns

**Inherit from shared configs:**

```yaml
inherit_from: .rubocop_todo.yml

AllCops:
  TargetRubyVersion: 3.2
```

**Exclude paths:**

```yaml
AllCops:
  Exclude:
    - 'vendor/**/*'
    - 'db/schema.rb'
    - 'node_modules/**/*'
```

**Adjust metrics for your codebase:**

```yaml
Metrics/MethodLength:
  Max: 20

Metrics/BlockLength:
  Exclude:
    - 'spec/**/*'  # RSpec blocks can be long
    - 'config/routes.rb'
```

## Official Documentation

For detailed cop documentation and configuration options:

<https://docs.rubocop.org/rubocop/>

For community extensions:

- <https://github.com/rubocop/rubocop-rails>
- <https://github.com/rubocop/rubocop-rspec>
- <https://github.com/rubocop/rubocop-performance>
