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

## Staging Preference (User Preference)

**Prefer atomic commits over convenience commits.**

Don't reflexively `git add .` - consider whether changes should be split into logical commits. Use `git add -p` for hunk-level staging when a file contains multiple concerns.

Bulk staging is fine when all changes are genuinely one logical unit.

## Authorship Verification Before Amending (Critical)

**ALWAYS check authorship before using `--amend`:**

```bash
git log -1 --format='%an <%ae>'
```

**Rules:**

- ✓ Only amend YOUR OWN commits - never amend someone else's work
- ✓ Check if pushed: `git status` should show "Your branch is ahead of..."
- ✓ If not ahead, commit is already on remote → create new commit instead

## Pre-Commit Hook Edge Case (Critical)

**Problem this user encounters:** Pre-commit hooks (formatters/linters) auto-modify files during commit, causing commit to fail.

### Failure Pattern

**What happens:**

1. User attempts: `git commit -m "message"`
1. Pre-commit hook runs and modifies files (auto-format)
1. Commit FAILS with message about working directory changes
1. Modified files are left unstaged

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

## Quality Checklist

Before committing for this user:

- ✓ Terse, single-line message (no emojis, no attribution, no period)
- ✓ Message is specific about what changed
- ✓ No secrets in staged files (.env, credentials.json, etc.)
- ✓ Considered atomic commits vs bulk staging
- ✓ If amending: verified authorship and not-pushed status
- ✓ Prepared for pre-commit hook retry if needed

## Documentation References

**Claude knows standard git.** Fetch docs only for edge cases or errors you don't recognize:

- <https://git-scm.com/docs> - Advanced git features
- <https://pre-commit.com/> - Hook configuration issues
