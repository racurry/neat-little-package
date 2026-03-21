#!/usr/bin/env bash
# PreToolUse hook - Blocks certain Bash patterns, suggests alternatives
#
# Claude tries to be efficient and do a bunch of shit in bash one-liners.  The tools it uses to do this
# frequently trigger security/permission checks, even if it actually has permission to do all of the
# things it is trying to do.
#
# This is disruptive as a user; I have already granted approval.  Don't do things in dumb ways that make
# me need to re-grant it.

command=$(jq -r '.tool_input.command // empty')
[[ -z "$command" ]] && exit 0

block() {
    echo "$1" >&2
    exit 2
}

# $() command substitution
# e.g. gh run view 23383648906 --log --job $(gh run view 23383648906 --json jobs --jq '...')
# e.g. for dir in plugins/*/; do echo "$(basename $dir) ==="; ls -1 "$dir" | head -15; done
if [[ "$command" == *'$('* ]]; then
    block 'Command contains $() substitution, which triggers a permission prompt. Rewrite using pipes, temporary variables, or separate commands instead.'
fi

# Backtick command substitution
if [[ "$command" == *'`'* ]]; then
    block 'Command contains backtick substitution, which triggers a permission prompt. Rewrite using pipes, temporary variables, or separate commands instead.'
fi

# echo/printf with "---" strings (triggers "quoted characters in flag names")
# e.g. git diff --staged --stat && echo "---UNSTAGED---" && git diff --stat
if [[ "$command" =~ (echo|printf)[[:space:]]+[\"\']--- ]]; then
    block "Command contains quoted strings starting with '---' which triggers 'quoted characters in flag names' permission prompt. Use a separator that doesn't start with dashes, or use printf with %s."
fi

# git -C <path> (uses -C flag instead of running from working directory)
# e.g. git -C /some/path status
if [[ "$command" =~ \bgit[[:space:]]+-C\b ]]; then
    block 'git -C is not allowed. Run git commands from the working directory instead. Use relative paths or absolute paths without -C flag.'
fi

# Brace with quote character (expansion obfuscation)
# e.g. curl -d '{"service": "update.install", "target": {"entity_id": "all"}}'
# Claude Code flags {" or {' as potential brace expansion obfuscation
if [[ "$command" == *'{"'* || "$command" == *"{'"* || "$command" == *"\"}"* || "$command" == *"'}"* ]]; then
    block "Command contains braces with quote characters (e.g. JSON), which triggers 'expansion obfuscation' permission prompt. Write the JSON to a temp file and reference it, or use a tool/API that accepts structured input instead."
fi

# Output redirection (>, 2>&1, 2>/dev/null, etc.)
# e.g. echo '...' | uv run --quiet --script hook.py 2>&1; echo "EXIT: $?"
# Strip quoted strings first so grep ">" isn't caught
stripped="${command//\"[^\"]*\"/}"
stripped="${stripped//\'[^\']*\'/}"
if [[ "$stripped" == *'>'* ]]; then
    block 'Command contains output redirection (>), which triggers a permission prompt. Use separate commands or pipe to tools instead.'
fi
