#!/usr/bin/env bash
# SessionStart hook - Proactive guidance for Bash patterns that always trigger permission prompts
#
# Companion to block_unneeded_permission_triggers.sh (PreToolUse), which reactively blocks
# these patterns. This hook proactively tells Claude what to avoid so it doesn't waste a
# tool call getting blocked.
#
# KEEP IN SYNC: If you add/remove a pattern in block_unneeded_permission_triggers.sh,
# update the guidance here too.

cat <<'GUIDANCE'
Avoid Bash patterns Claude Code can't statically analyze — each one always triggers a permission prompt:
- No `$(...)` command substitution — use pipes, temp variables, or separate commands
- No backtick command substitution — same
- No `${...}` braced parameter expansion — it reports as "Contains expansion" and only offers Allow-once (can't be allowlisted). Use bare `$VAR` (`$HOME`, not `${HOME}`); `$HOME/path` works the same as `${HOME}/path`. If braces are unavoidable (`${VAR:-default}`, `${VAR/a/b}`, `${VAR}suffix`), assign to a plain variable on a separate line. Bare `$var` itself is fine.
- No `for`/`while`/`until` loops — the loop construct can't reduce to a static prefix, so any `$var` in the body prompts. Use the Grep/Glob/Read tools (they iterate natively), or run separate commands. Bare `$var` in a single command is fine; only the loop is the problem.
GUIDANCE
