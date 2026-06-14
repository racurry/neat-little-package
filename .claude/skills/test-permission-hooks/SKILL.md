---
name: test-permission-hooks
description: Empirically test whether mr-sparkle's permission-trigger blocking hook earns its keep — run its blocked patterns with the hook on, then with mr-sparkle disabled, and see which patterns actually trigger a Claude Code permission prompt without it. Use when deciding whether to keep, narrow, or drop block_unneeded_permission_triggers.sh + bash_guidance.sh.
---

# Test Permission-Trigger Hooks

mr-sparkle's `block_unneeded_permission_triggers.sh` (PreToolUse) blocks 7 Bash patterns that *it claims* trigger Claude Code permission prompts, so Claude rewrites instead of making the user re-approve. `bash_guidance.sh` (SessionStart) preaches the same list. The open question: **do those patterns actually trigger a prompt under the current permission setup?** If not, the hook is pure friction (it blocked ~6 legitimate read-only commands in one review session).

This is a **two-phase** test — the phase boundary is the user toggling the mr-sparkle plugin.

## The 7 patterns and their test commands

Each command is safe/no-op and isolates one pattern against an otherwise-allowed base command (so any Phase-2 prompt is due to the *pattern*, not the base command).

| #   | Pattern                         | Test command                                        |
| --- | ------------------------------- | --------------------------------------------------- |
| 1   | `$()` command substitution      | `echo "$(echo subst)"`                              |
| 2   | Backtick substitution           | `echo "` + backtick + `echo subst` + backtick + `"` |
| 3   | `echo/printf` with `---` string | `echo "--- divider ---"`                            |
| 4   | `git -C <path>`                 | `git -C . status --short`                           |
| 5   | Fully-qualified cwd path        | `ls <absolute path to this repo>/docs`              |
| 6   | Brace + quote (JSON)            | `echo '{"test":1}'`                                 |
| 7   | Output redirection              | `echo redirect-test > ./.tmp/perm-test.txt`         |

## Phase 1 — hooks ON (mr-sparkle enabled)

Run each of the 7 commands. **Expected:** `block_unneeded_permission_triggers.sh` intercepts each (exit 2) with a "…triggers a permission prompt" message — the command never runs. Record blocked vs. ran for each. This confirms the hook is active and what it catches.

## Phase 2 — hooks OFF

Ask the user to **disable the mr-sparkle plugin AND restart the session**, then run the same 7 commands again. Disabling the plugin does *not* unload its hooks from a running session — hooks are registered at session start, so without a restart the blocking hook keeps firing and Phase 2 is invalid (observed 2026-06-14). After the restart the blocking hook is gone, so the raw Claude Code permission system decides. For each command, record:

- **Prompted** — the user got a permission prompt (approve/deny), OR
- **Ran clean** — it executed with no prompt.

(The user watches for prompts — they're the one who'd be interrupted.)

## Decision rule

Per pattern:

- **Prompted without the hook** → the hook prevents a real interruption → **keep** it for that pattern.
- **Ran clean without the hook** → the hook was blocking a harmless command for no benefit → **drop/narrow** that pattern.

If *every* pattern runs clean without the hook, the whole prophylactic layer (`block_unneeded_permission_triggers.sh` + `bash_guidance.sh`) is friction-only → remove both. If *some* prompt, narrow the hook to just those.

## Report

Produce a table: pattern → Phase 1 (blocked?) → Phase 2 (prompted / clean) → verdict (keep / drop).

## Cleanup

- `rm ./.tmp/perm-test.txt` (created by pattern 7 if it ran in Phase 2).
- Tell the user to re-enable mr-sparkle (disabling it also turns off the dangerous-command and lint-on-write hooks).
