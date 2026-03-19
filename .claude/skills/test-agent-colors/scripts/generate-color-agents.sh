#!/usr/bin/env bash
# Generate color test agent files in .claude/agents/
set -euo pipefail

AGENTS_DIR="${CLAUDE_SKILL_DIR:-.claude/skills/test-agent-colors}/../../agents"

COLORS=(
    red green blue yellow magenta cyan white black
    gray grey purple orange
    redBright greenBright blueBright yellowBright
    magentaBright cyanBright whiteBright blackBright
)

for color in "${COLORS[@]}"; do
    cat >"$AGENTS_DIR/color-${color}.md" <<EOF
---
name: color-${color}
description: Test agent for ${color} color
model: haiku
tools: Bash
color: ${color}
---

Report the current date and time by running \`date\`. Return only the result.
EOF
done

echo "Generated ${#COLORS[@]} color agents in $AGENTS_DIR"
