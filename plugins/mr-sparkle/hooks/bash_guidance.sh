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
Avoid command substitution in Bash commands — Claude Code can't statically analyze it, so it always triggers a permission prompt:
- No `$(...)` command substitution — use pipes, temp variables, or separate commands
- No backtick command substitution — same
GUIDANCE
