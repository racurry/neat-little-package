#!/usr/bin/env bash
# PreToolUse hook: blocks direct invocations of tools that should go
# through mr-sparkle's lint skill for proper config resolution.
#
# Reads block_direct rules from .claude/mr-sparkle.config.yml.
# Default rules apply when no config exists.
# Set block_direct: [] in config to disable all blocking.
#
# Exit codes:
#   0 - allow
#   2 - block (prints reason to stderr)

# Read hook JSON from stdin
input=$(cat)

# Parse fields - exit 0 (allow) on any parse failure
tool_name=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null) || exit 0
[ "$tool_name" = "Bash" ] || exit 0

command=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null) || exit 0
[ -n "$command" ] || exit 0

cwd=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('cwd',''))" 2>/dev/null) || true

# Check if block_direct is disabled via config
if [ -n "$cwd" ] && [ -f "$cwd/.claude/mr-sparkle.config.yml" ]; then
    if grep -qE '^\s*block_direct:\s*\[\s*\]' "$cwd/.claude/mr-sparkle.config.yml" 2>/dev/null; then
        exit 0
    fi
fi

# --- Rules ---
# check_rule prefix unless message
# Blocks commands starting with "prefix " unless they contain "unless"
check_rule() {
    local prefix="$1" unless="$2" message="$3"
    case "$command" in
    "$prefix "*)
        if [ -n "$unless" ]; then
            case "$command" in
            *"$unless"*) return 0 ;;
            esac
        fi
        echo "$prefix $message" >&2
        exit 2
        ;;
    esac
}

check_rule "markdownlint-cli2" "--config" "requires --config. Use /mr-sparkle:lint instead."

exit 0
