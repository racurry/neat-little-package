#!/usr/bin/env bash
# SessionStart hook - Proactive guidance for Bash patterns that trigger permission prompts
#
# Companion to block_unneeded_permission_triggers.sh (PreToolUse), which reactively blocks
# these patterns. This hook proactively tells Claude what to avoid so it doesn't waste a
# tool call getting blocked.
#
# KEEP IN SYNC: If you add/remove a pattern in block_unneeded_permission_triggers.sh,
# update the guidance here too.

cat <<'GUIDANCE'
When writing Bash commands, avoid these patterns that trigger unnecessary permission prompts:
- No `$()` or backtick command substitution — use pipes, temp variables, or separate commands
- No output redirection (`>`, `2>&1`, `2>/dev/null`) — use separate commands or pipe to tools
- No inline JSON with braces+quotes (`{"`, `'}`) — write JSON to a temp file instead
- No `git -C <path>` — run git from the working directory
- No `echo/printf "---..."` — dashes in quoted strings trigger flag-name detection
- Use relative paths (`./script.py`), not fully qualified (`$PWD/script.py`)
GUIDANCE
