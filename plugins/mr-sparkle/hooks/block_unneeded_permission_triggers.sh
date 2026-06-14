#!/usr/bin/env bash
# PreToolUse hook - Blocks the Bash patterns that ALWAYS trigger a permission prompt
#
# Claude tries to be efficient and do a bunch of shit in bash one-liners. Command
# substitution ($() and backticks) contains "shell syntax that cannot be statically
# analyzed", so Claude Code ALWAYS asks for permission — there's no way to allowlist it
# (the prompt only offers "Allow once"). Blocking these here gets Claude to rewrite
# (pipes, temp vars, separate commands) instead of interrupting me.
#
# Scope note (verified 2026-06-14, desktop app + TUI): ONLY $() and backtick substitution
# still force a prompt. The patterns this hook used to also block — "---" strings, git -C,
# fully-qualified paths, {"json"}, and output redirection — no longer trigger prompts under
# current Claude Code + my allowlist, even in their real compound/redirect forms. They were
# removed because they only blocked harmless commands. Re-test with the test-permission-hooks
# skill if that ever feels wrong again.
#
# KEEP IN SYNC: bash_guidance.sh (SessionStart) proactively tells Claude about these
# rules. If you add/remove a pattern here, update the guidance there too.

command=$(jq -r '.tool_input.command // empty')
[[ -z "$command" ]] && exit 0

block() {
    echo "$1" >&2
    exit 2
}

# $() command substitution — "cannot be statically analyzed" → always prompts
# e.g. gh run view 123 --log --job $(gh run view 123 --json jobs --jq '...')
if [[ "$command" == *'$('* ]]; then
    block 'Command contains $() substitution, which always triggers a permission prompt (cannot be statically analyzed). Rewrite using pipes, temporary variables, or separate commands instead.'
fi

# Backtick command substitution — same
if [[ "$command" == *'`'* ]]; then
    block 'Command contains backtick substitution, which always triggers a permission prompt (cannot be statically analyzed). Rewrite using pipes, temporary variables, or separate commands instead.'
fi
