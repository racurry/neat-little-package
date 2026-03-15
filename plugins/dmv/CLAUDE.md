# DMV Development Guidelines

**Knowledge Delta Only:** Skills and agents document only what Claude would get wrong. Standard git/GitHub knowledge comes from training. Fetch official docs before assuming something needs documenting.

**No Type Prefixes:** This user never uses conventional commit prefixes (`fix:`, `feat:`, etc.). Just describe the change directly.

**No Attribution Ever:** No "Generated with Claude Code", no "Co-Authored-By:", no emojis. This applies to commits, PRs, and all generated content.

**Pre-commit Hook Retry:** When hooks modify files (auto-formatting), stage changes and retry ONCE with `git commit --amend --no-edit`. Never retry validation failures. Never retry more than once.

**Tool Hierarchy:** Prefer `gh` CLI over GitHub MCP server. Only fall back to MCP when gh isn't installed or doesn't support the operation.

**No `$()` Substitution:** Per global rules, `$()` command substitution triggers permission prompts. Use temp files, pipes, or alternatives like `git push -u origin HEAD` instead of `git push -u origin $(git branch --show-current)`.
