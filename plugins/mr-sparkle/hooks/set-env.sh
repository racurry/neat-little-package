#!/bin/bash
# SessionStart hook to persist plugin root as environment variable.
#
# BLOCKED BY BUG: CLAUDE_ENV_FILE is not provided to plugin hooks.
# See: https://github.com/anthropics/claude-code/issues/9567
#
# When fixed, this hook will make $MR_SPARKLE_ROOT available to all
# subsequent Bash commands, including those triggered by slash commands.

# Self-locate: this script is at <plugin_root>/hooks/set-env.sh
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(dirname "$SCRIPT_DIR")"

# Try to set env var if available
# Note: CLAUDE_ENV_FILE not available for plugin hooks, see https://github.com/anthropics/claude-code/issues/9567
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo "export MR_SPARKLE_ROOT=$PLUGIN_ROOT" >> "$CLAUDE_ENV_FILE"
fi

# Output JSON in correct SessionStart format
# - additionalContext becomes Claude's context
# - systemMessage shows warning to user
# We can remove this once the claude bug is fixed

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "MR_SPARKLE_ROOT=$PLUGIN_ROOT - Use this path for mr-sparkle plugin scripts and config files."
  }
}
EOF

exit 0
