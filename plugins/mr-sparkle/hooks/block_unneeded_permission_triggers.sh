#!/usr/bin/env bash
# PreToolUse hook - Blocks the Bash patterns that ALWAYS trigger a permission prompt
#
# Claude tries to be efficient and do a bunch of shit in bash one-liners. Command
# substitution ($() and backticks) contains "shell syntax that cannot be statically
# analyzed", so Claude Code ALWAYS asks for permission — there's no way to allowlist it
# (the prompt only offers "Allow once"). Blocking these here gets Claude to rewrite
# (pipes, temp vars, separate commands) instead of interrupting me.
#
# Scope note (verified 2026-06-15, desktop app + TUI): $() substitution, backtick substitution,
# and for/while/until loops force a prompt. Loops report as "simple_expansion" because the loop
# construct can't reduce to a static prefix — but bare $var outside a loop is fine (`echo "$HOME"`
# runs clean), so we match the loop, not the variable. The patterns this hook used to also block —
# "---" strings, git -C, fully-qualified paths, {"json"}, and output redirection — no longer
# trigger prompts under current Claude Code + my allowlist, even in their real compound/redirect
# forms. They were removed because they only blocked harmless commands. Re-test with the
# test-permission-hooks skill if any of this ever feels wrong again.
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

# for/while/until loops — the loop construct can't reduce to a static command prefix, so
# Claude Code flags any $var in the body as "simple_expansion" and ALWAYS prompts (verified
# 2026-06-15, TUI). Bare $var outside a loop is fine (`echo "$HOME"` runs clean) — so match the
# loop, not the variable. Discriminator: a loop keyword at statement position (start, or after
# ; & | ( ) AND a literal `; do` (one-liner loops always have one). This avoids false-positives
# on prose like `git commit -m "refactor for loop; do it later"` (the `for` isn't at statement
# position). e.g. for f in apps/*/; do grep pat "$f"; done
loop_kw='(^|[;&|(])[[:space:]]*(for|while|until)[[:space:]]'
if [[ "$command" =~ $loop_kw ]] && [[ "$command" =~ \;[[:space:]]*do[[:space:]] ]]; then
    block 'Command uses a for/while/until loop, which always triggers a permission prompt (the loop body cannot be statically analyzed). Use the Grep/Glob/Read tools or run separate commands instead of a shell loop.'
fi
