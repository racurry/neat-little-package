---
name: dmv-config
description: Manage dmv per-project hook settings
argument-hint: show | set <key> <value>
disable-model-invocation: true
model: haiku
effort: low
allowed-tools: Bash(*)
---

!`${CLAUDE_SKILL_DIR}/scripts/config.py $ARGUMENTS`

Report the output above to the user verbatim. Nothing else.
