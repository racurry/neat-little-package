---
paths:
  - plugins/mr-sparkle/**
---

# Mr. Sparkle Development Guidelines

These git/GitHub conventions are what the `commit`, `pr`, `github`, and `merge-conflicts` skills encode.

**No Type Prefixes:** This user never uses conventional commit prefixes (`fix:`, `feat:`, etc.). Just describe the change directly.

**No Attribution Ever:** No "Generated with Claude Code", no "Co-Authored-By:", no emojis. This applies to commits, PRs, and all generated content.

**Pre-commit Hook Retry:** When hooks modify files (auto-formatting), stage changes and retry ONCE with `git commit --amend --no-edit`. Never retry validation failures. Never retry more than once.

**GitHub Tooling:** Use the `gh` CLI for all GitHub interactions.

**No `$()` Substitution:** Per global rules, `$()` command substitution triggers permission prompts. Use temp files, pipes, or alternatives like `git push -u origin HEAD` instead of `git push -u origin $(git branch --show-current)`.
