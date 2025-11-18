---
name: git-workflow
description: User-specific git workflow preferences and edge case handling. Documents commit message format requirements and pre-commit hook retry logic specific to this user. Use when creating commits or handling pre-commit hook failures.
---

# Git Workflow Skill

This skill documents workflow preferences and edge cases specific to this user. Claude already knows standard git commands and workflows from training - this skill only documents the user-specific details.

## User-Specific Commit Message Requirements

**This user has specific commit format preferences that differ from standard practices.**

### Message Format (User Preference)

**User requirements:**

- Terse, single-line format (max ~200 characters)
- NO emojis or decorative elements
- NO attribution text (no "Generated with Claude Code", no "Co-Authored-By:")
- Lowercase type prefix
- Present tense, imperative mood
- No period at end

**Good examples:**

```
prevent race condition in session cleanup
rate limiting middleware
improve error handling in payment flow
extract validation logic for reuse
```

**Avoid:**

```
❌ add: new feature ✨ (emoji - user doesn't want)
❌ fix: correct bug

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
(attribution text - user doesn't want)

❌ updates (too vague, missing type prefix)
❌ Fix: thing (capitalized type)
❌ fix bug. (has period at end)
```

### Message Quality (User Preference)

**Be specific about WHAT changed:**

✅ Good:

```
prevent race condition in user session cleanup
caching layer for frequently accessed user data
```

❌ Too vague:

```
fix: bug fix
add: new feature
```

## Pre-Commit Hook Edge Case (Critical)

**Problem this user encounters:** Pre-commit hooks (formatters/linters) auto-modify files during commit, causing commit to fail.

### Failure Pattern

**What happens:**

1. User attempts: `git commit -m "message"`
2. Pre-commit hook runs and modifies files (auto-format)
3. Commit FAILS with message about working directory changes
4. Modified files are left unstaged

**Why it fails:** Git won't commit when the working directory is modified during the commit process (hooks changed files after they were staged).

### Solution: Single Retry Pattern

**When commit fails due to hook modifications:**

```bash
# 1. Stage the auto-modified files
git add .

# 2. Retry ONCE with --amend --no-edit
git commit --amend --no-edit
```

**CRITICAL rules:**

- ✓ Only retry ONCE to avoid infinite loops
- ✓ Only use this pattern when commit failed due to hook modifications
- ✓ If retry also fails, investigate hook configuration (may have infinite modification bug)
- ✓ Never retry more than once automatically

**When NOT to use this pattern:**

- ❌ If hook failed validation (not modifications) - fix the validation issues instead
- ❌ If commit succeeded without errors - no retry needed
- ❌ If you already retried once - stop and report failure

## Common Pitfall: Hook Attribution Conflicts

**Problem:** Some generic git workflows add attribution text this user doesn't want.

**What to avoid:**

```bash
# Don't create commits with attribution like:
git commit -m "$(cat <<'EOF'
fix: correct validation logic

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**This user's preference:**

```bash
# Simple, terse, single-line only:
git commit -m "correct validation logic"
```

## Quality Checklist

Before committing for this user:

**Message format:**

- ✓ Terse, single-line format (max ~200 characters)
- ✓ Pattern: `<brief specific description>`
- ✓ No emojis or decorative elements
- ✓ No attribution text (no "Generated with Claude Code", no "Co-Authored-By:")
- ✓ Lowercase type, imperative mood, no period

**Content quality:**

- ✓ No secrets in staged files (.env, credentials.json, etc.)
- ✓ Message is specific about what changed (not vague)
- ✓ Changes are reviewed (ran git status and git diff)

**Pre-commit hooks:**

- ✓ Prepared for potential hook retry (understand single-retry pattern)
- ✓ Won't retry more than once if hooks keep modifying

## Documentation References

**Official Git documentation:**

- <https://git-scm.com/docs> - Complete Git reference for current syntax

**Pre-commit hooks:**

- <https://pre-commit.com/> - Pre-commit framework documentation

**Remember:** This skill only documents user-specific preferences and edge cases. Claude already knows standard git commands, branching workflows, and general best practices from training.
