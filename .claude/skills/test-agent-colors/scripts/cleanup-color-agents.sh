#!/usr/bin/env bash
# Remove color test agent files from .claude/agents/
set -euo pipefail

AGENTS_DIR="${CLAUDE_SKILL_DIR:-.claude/skills/test-agent-colors}/../../agents"

rm -f "$AGENTS_DIR"/color-*.md

echo "Cleaned up color agents from $AGENTS_DIR"
