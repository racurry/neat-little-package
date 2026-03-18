#!/usr/bin/env bash
# Blocks creation of .scpt files (compiled AppleScript binary).
# Use .applescript (plain text) instead.

file_path=$(jq -r '.tool_input.file_path // empty')

if [[ "$file_path" == *.scpt ]]; then
    echo '{"decision":"block","reason":"Do not create .scpt files (compiled AppleScript binary). Use .applescript extension instead for plain-text AppleScript that is editable and git-friendly."}'
fi
