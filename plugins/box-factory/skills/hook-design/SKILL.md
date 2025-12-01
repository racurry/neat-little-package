---
name: box-factory-hooks-design
description: Interpretive guidance for designing Claude Code hooks. Helps you understand hook lifecycle, when to use hooks vs other patterns, and common pitfalls. Use when creating or reviewing hooks.
---

# Hooks Design Skill

This skill provides interpretive guidance and best practices for creating Claude Code hooks. **ALWAYS fetch current official documentation before creating hooks** - this skill helps you understand what the docs mean and how to create excellent hooks.

## Required Reading Before Creating Hooks

Fetch these docs with WebFetch every time:

- **<https://code.claude.com/docs/en/hooks>** - Complete hook reference

## Core Understanding

### Hooks Are Deterministic Control

**Key insight:** Hooks provide guaranteed, deterministic execution at specific lifecycle events.

**What this means:**

- **Hooks** = Execute every single time (deterministic)
- **Prompts/Instructions** = Claude might forget (probabilistic)
- **Agents** = Context-dependent intelligence
- **Use hooks when "always" matters**

**Decision question:** Do you need this to happen every single time, or is "usually" okay?

**Examples:**

- Format after every file write → Hook
- Suggest code improvements → Prompt to Claude
- Run tests after code changes → Hook if mandatory, agent if discretionary
- Security validation before bash → Hook (must be enforced)

### Hook Architecture (How It Fits)

**Execution flow:**

```text
User Input → Claude Thinks → Tool Execution
                    ↑              ↓
              Hooks fire here ────┘
```

**Critical implications:**

- **PreToolUse**: Can block/modify before tool runs
- **PostToolUse**: Can react after tool completes successfully
- **Stop**: Can't affect what Claude just did (it's done, only cleanup)
- **UserPromptSubmit**: Runs before Claude sees the prompt

### Exit Codes Are Communication (Official Specification)

**Exit 0**: Hook succeeded, continue execution

- stdout displays in transcript mode (CTRL-R)
- Exception: `UserPromptSubmit` and `SessionStart` where stdout becomes context for Claude

**Exit 2**: Blocking error, stop and handle

- stderr feeds to Claude for processing
- Behavior varies by event:
  - **PreToolUse**: Blocks tool call
  - **Stop/SubagentStop**: Blocks stoppage
  - **UserPromptSubmit**: Blocks prompt, erases it, shows error to user only

**Other exit codes**: Non-blocking error

- stderr displays to user
- Execution continues

**Best practice:** Use exit 2 sparingly - it's powerful but disruptive. Use it for security/safety enforcement, not preferences.

## Hook Events (Official Specification)

Complete list of available events:

| Event | When It Fires | Matcher Applies |
|-------|--------------|----------------|
| **PreToolUse** | After Claude creates tool params, before processing | Yes |
| **PostToolUse** | Immediately after successful tool completion | Yes |
| **PermissionRequest** | When permission dialogs shown to users | No |
| **Notification** | When Claude Code sends notifications | No |
| **UserPromptSubmit** | When users submit prompts, before Claude processes | No |
| **Stop** | When main Claude agent finishes responding | No |
| **SubagentStop** | When subagents (Task tool calls) complete | No |
| **PreCompact** | Before compacting operations | No |
| **SessionStart** | When sessions start or resume | No |
| **SessionEnd** | When sessions terminate | No |

## Hook Types (Official Specification)

**Command Hooks** (`type: "command"`):

- Execute bash scripts with file system access
- Default timeout: 60 seconds (customizable per hook)
- Fast, deterministic operations
- Use for formatters, linters, file ops, git commands

**Prompt-Based Hooks** (`type: "prompt"`):

- Send queries to Claude Haiku for context-aware decisions
- Available for: `Stop`, `SubagentStop`, `UserPromptSubmit`, `PreToolUse`
- Use when judgment/context understanding needed
- Natural language evaluation

**Rule of thumb:** If you can write it as a bash script = command hook. If you need judgment = prompt hook.

## Hook Script Implementation Patterns (Best Practices)

### Bash vs Python for Hook Scripts

**Bash is ideal for:**

- Simple file operations (formatting, linting with external tools)
- Calling CLI tools directly
- Quick text processing with standard utilities
- Minimal logic, mostly orchestration

**Python is better for:**

- Complex validation logic
- JSON parsing and manipulation
- Advanced text processing
- Using Python libraries for analysis
- Multi-step processing with error handling

### Python Hook Scripts with UV (Best Practice)

For Python-based hooks requiring dependencies or complex logic, use UV's single-file script format with inline metadata. This provides self-contained, executable scripts without separate environment setup.

**When to use Python hooks:**

- Parsing complex JSON from stdin
- Advanced validation requiring libraries (AST analysis, schema validation)
- Multi-step processing beyond simple shell pipelines
- Need for structured error handling and reporting

**Pattern:** Use Skill tool: skill="box-factory:uv-scripts"

The uv-scripts skill provides complete patterns for creating Python hook scripts with inline dependencies, proper shebangs, and Claude Code integration.

**Quick example:**

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["ruff"]
# ///

import subprocess
import sys
import os

def main():
    file_paths = os.environ.get("CLAUDE_FILE_PATHS", "").split()
    if not file_paths:
        sys.exit(0)

    result = subprocess.run(["ruff", "check", *file_paths])
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
```

**Key advantages:**

- Self-contained (dependencies declared inline)
- No separate virtual environment management
- Executable directly with proper shebang
- Fast startup with UV's performance
- Perfect for plugin hooks (ships with dependencies)

## Matcher Syntax (Official Specification)

Matchers specify which tools trigger hooks (applies to PreToolUse and PostToolUse only):

**Exact matching:**

```json
"matcher": "Write"
```

**Regex patterns with pipe:**

```json
"matcher": "Edit|Write"
"matcher": "Notebook.*"
```

**Wildcard (match all):**

```json
"matcher": "*"
```

**Empty matcher:**
Omit for events like `UserPromptSubmit` that don't apply to specific tools.

**Note:** Matchers are case-sensitive.

## Configuration Structure (Official Specification)

Located in `~/.claude/settings.json`, `.claude/settings.json`, or `.claude/settings.local.json`:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "bash-command",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Timeout field:** Optional, specified in seconds (default 60).

## Hook Input (stdin) - Official Specification

All hooks receive JSON via stdin:

**Base structure (all events):**

```json
{
  "session_id": "string",
  "transcript_path": "path/to/transcript.jsonl",
  "cwd": "current/working/directory",
  "permission_mode": "default|plan|acceptEdits|bypassPermissions",
  "hook_event_name": "EventName"
}
```

**Event-specific fields:**

- **PreToolUse/PostToolUse**: Adds `tool_name`, `tool_input`
- **UserPromptSubmit**: Adds `prompt`
- Other events may include additional context

**Best practice:** Parse stdin JSON to access context, don't rely only on environment variables.

## Hook Output (stdout) - Official Specification

Two approaches for returning results:

### Simple Exit Code Approach

Just use exit codes and stderr for errors. Most common for straightforward hooks.

### Advanced JSON Output

Return structured JSON for sophisticated control:

```json
{
  "continue": true,
  "stopReason": "Custom message",
  "suppressOutput": true,
  "systemMessage": "Warning to display",
  "hookSpecificOutput": {
    "hookEventName": "EventName",
    "additionalContext": "string"
  }
}
```

### PostToolUse Communication Pattern (CRITICAL)

**Key insight:** PostToolUse hooks have two output channels with different visibility:

**For messages visible DIRECTLY to users (no verbose mode required):**

Use `systemMessage` field - displays immediately to users:

```json
{
  "systemMessage": "Markdown formatted: path/to/file.md"
}
```

**ANSI escape codes work:** You can colorize `systemMessage` output:

```python
# Red error text
error_msg = f"\033[31mLinter error in {file_path}:\033[0m"
# Green success
success_msg = f"\033[32mFormatted: {file_path}\033[0m"
```

**For context injected into Claude's awareness:**

Use `additionalContext` in `hookSpecificOutput`. This appears to Claude as a `<system-reminder>` with prefix `PostToolUse:{ToolName} hook additional context:`:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Linter output details for Claude to act on"
  }
}
```

**Visibility behavior (empirically tested):**

- `systemMessage` → User sees immediately in terminal
- `additionalContext` → Claude receives as system-reminder; user sees only in verbose mode (CTRL-O)

**Complete output pattern:**

```python
import json
output = {
    "systemMessage": "Formatted successfully: file.md",  # Shows to user directly
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "Linter details for Claude"  # Claude gets this as system-reminder
    }
}
print(json.dumps(output), flush=True)
sys.exit(0)
```

**Common mistake:** Using only `additionalContext` when user feedback is needed. Users won't see it without verbose mode.

**Correct pattern:**

- **User feedback needed:** Use `systemMessage` (visible immediately, supports ANSI colors)
- **Claude context needed:** Use `additionalContext` (Claude receives as system-reminder)
- **Both:** Include both fields - user sees status, Claude gets details
- **Blocking errors:** Use exit 2 with stderr (rare, security/safety only)

### SessionStart Output Format (CRITICAL)

SessionStart hooks use a different output pattern than PostToolUse. The `additionalContext` becomes Claude's context at session start.

**Correct SessionStart JSON format:**

```json
{
  "systemMessage": "Message shown directly to user",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Context injected for Claude to use during session"
  }
}
```

**Key differences from PostToolUse:**

- `hookEventName` MUST be `"SessionStart"` (not `"PostToolUse"`)
- `additionalContext` becomes persistent session context for Claude
- Use for: plugin paths, environment info, project state

**Bash example:**

```bash
#!/bin/bash
PLUGIN_ROOT="$(dirname "$(dirname "$0")")"
cat <<EOF
{
  "systemMessage": "[my-plugin] Loaded from: $PLUGIN_ROOT",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "MY_PLUGIN_ROOT=$PLUGIN_ROOT - Use this path for plugin resources."
  }
}
EOF
exit 0
```

**Common mistake:** Using bare `systemMessage` without `hookSpecificOutput`:

```json
// Wrong - missing hookSpecificOutput structure
{"systemMessage": "Plugin loaded"}

// Correct - full structure
{
  "systemMessage": "Plugin loaded",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Plugin context for Claude"
  }
}
```

### PreToolUse Special Output

For modifying or blocking tool execution:

```json
{
  "permissionDecision": "allow|deny|ask",
  "updatedInput": {
    "modified": "tool parameters"
  }
}
```

**Use case:** Modify tool inputs before execution (e.g., add safety flags to bash commands).

## Environment Variables (Official Specification)

Available in command hooks:

| Variable | Purpose |
|----------|---------|
| `$CLAUDE_PROJECT_DIR` | Absolute path to project root |
| `$CLAUDE_ENV_FILE` | File path for persisting env vars (SessionStart only) |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin directory path (for plugin hooks) |
| `$CLAUDE_CODE_REMOTE` | `"true"` for remote, empty for local execution |

**Best practice:** Always quote variables: `"$CLAUDE_PROJECT_DIR"` not `$CLAUDE_PROJECT_DIR`

## Decision Framework

### Hook vs Agent vs Command

**Use Hook when:**

- Need guaranteed execution every time
- Simple, deterministic rule (format, lint, validate)
- Integrating with external tools
- Performance/safety enforcement
- Must happen at specific lifecycle event

**Use Agent when:**

- Complex decision-making involved
- Need Claude's intelligence for analysis
- Context-dependent logic
- Natural language processing needed
- Can be triggered proactively by context

**Use Command (Slash Command) when:**

- User wants explicit control over when it runs
- Not tied to lifecycle events
- One-off operations

## Common Use Patterns (Best Practices)

### SessionStart Pattern

**Purpose:** Initialize session state, inject context

```json
{
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "cat .claude/project-context.md"
        }
      ]
    }
  ]
}
```

**Key:** stdout becomes Claude's context. Use to load project guidelines, conventions, or state.

### UserPromptSubmit Pattern

**Purpose:** Validate or enrich prompts before Claude sees them

```json
{
  "UserPromptSubmit": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "~/.claude/hooks/inject-security-reminders.sh"
        }
      ]
    }
  ]
}
```

**Key:** stdout goes to Claude. Can add context or use exit 2 to block prompts.

### PreToolUse Pattern

**Purpose:** Validate or modify before execution

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "~/.claude/hooks/security-check.sh"
        }
      ]
    }
  ]
}
```

**Power move:** Exit 2 to block dangerous commands and explain why to Claude.

### PostToolUse Pattern

**Purpose:** React to successful tool completion

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "prettier --write \"$CLAUDE_FILE_PATHS\" 2>/dev/null || true"
        }
      ]
    }
  ]
}
```

**Common uses:** Format code, run linters, update documentation, cleanup.

**CRITICAL for PostToolUse:** To communicate results to users, hooks must output JSON to stdout with `systemMessage`:

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
import json
import sys

def output_json_response(system_message=None, additional_context=None):
    """Output JSON response for Claude to process."""
    response = {}
    if system_message:
        response["systemMessage"] = system_message  # Visible directly to user
    if additional_context:
        response["hookSpecificOutput"] = {
            "hookEventName": "PostToolUse",
            "additionalContext": additional_context  # Only visible in verbose mode
        }
    print(json.dumps(response), flush=True)

# Read hook input from stdin
hook_input = json.load(sys.stdin)
file_path = hook_input.get("tool_input", {}).get("file_path")

# Run linter/formatter
# ...

# Communicate result directly to user
output_json_response(system_message=f"Formatted successfully: {file_path}")
sys.exit(0)
```

**Common mistakes:**

- Using only `additionalContext` when user feedback is needed (requires verbose mode)
- Writing to stderr instead of JSON stdout (completely invisible)

### Stop Pattern

**Purpose:** Session cleanup, final actions

```json
{
  "Stop": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "~/.claude/hooks/auto-commit.sh"
        }
      ]
    }
  ]
}
```

**Note:** Claude already responded, can't change that. Use for cleanup, notifications, test runs.

## Common Pitfalls (Best Practices)

### Pitfall #1: Blocking Everything

**Problem:** Overly aggressive hook blocks all operations

```json
{
  "PreToolUse": [
    {
      "matcher": "*",
      "hooks": [{"type": "command", "command": "exit 2"}]
    }
  ]
}
```

**Result:** Claude can't do anything, unusable.

**Better:** Selective blocking with clear criteria for security/safety only.

### Pitfall #2: Slow Hooks

**Problem:** Hook takes 30+ seconds, blocks user experience

```bash
npm install  # Slow, blocking
exit 0
```

**Impact:** Claude waits, terrible UX.

**Better:** Fast validation or background execution

```bash
npm outdated | head -5  # Quick check
exit 0
```

**Or:** Adjust timeout for legitimately long operations:

```json
{
  "type": "command",
  "command": "long-running-task.sh",
  "timeout": 120
}
```

### Pitfall #3: Silent Failures

**Problem:** Errors disappear into the void

```bash
important-check || true
exit 0
```

**Result:** User never knows check failed.

**Better:** Clear error communication

```bash
if ! important-check; then
  echo "Check failed: [specific reason]" >&2
  exit 1  # Non-blocking, but visible
fi
exit 0
```

### Pitfall #4: Assuming User Interaction

**Problem:** Hook expects user input

```bash
read -p "Confirm? " response
exit 0
```

**Result:** Hook hangs indefinitely (no user to respond).

**Better:** Fully automated decisions based on stdin JSON or environment.

### Pitfall #5: Ignoring Security

**Problem:** Hook doesn't validate inputs, vulnerable to path traversal

```bash
cat "$SOME_PATH"  # Dangerous if not validated
```

**Result:** Could access sensitive files outside project.

**Better:** Validate and sanitize

```bash
if [[ "$SOME_PATH" == *".."* ]]; then
  echo "Path traversal detected" >&2
  exit 2
fi
# Continue safely
```

**Official guidance:** Skip sensitive files (`.env`, `.git/`, credentials). Validate inputs from stdin.

### Pitfall #6: Not Quoting Variables

**Problem:** Unquoted shell variables break with spaces

```bash
prettier --write $CLAUDE_FILE_PATHS  # Breaks if path has spaces
```

**Better:** Always quote variables

```bash
prettier --write "$CLAUDE_FILE_PATHS"
```

### Pitfall #7: PostToolUse Using Wrong Output Field

**Problem:** Hook uses `additionalContext` when user feedback is needed

```python
# Wrong - Only visible in verbose mode (CTRL-O)
import json
output = {
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "Formatted successfully: file.md"
    }
}
print(json.dumps(output), flush=True)
sys.exit(0)
```

**Result:** User must enable verbose mode to see feedback.

**Better:** Use `systemMessage` for direct user visibility

```python
# Correct - Visible immediately to user
import json
output = {
    "systemMessage": "Formatted successfully: file.md"
}
print(json.dumps(output), flush=True)
sys.exit(0)
```

**Why:**

- `systemMessage` displays directly to users (no verbose mode required)
- `additionalContext` only visible in verbose mode (CTRL-O) or as Claude's context
- stderr output is only for blocking errors (exit 2)

## Security Considerations (Official Guidance)

**Critical warning from docs:** "Claude Code hooks execute arbitrary shell commands on your system automatically."

**Implications:**

- Hooks can access/modify any files your user account permits
- You bear sole responsibility for configured commands
- Test thoroughly in safe environments first
- Review hooks from untrusted sources carefully

**Protection mechanism:**

- Configuration snapshots captured at startup
- Hook changes require review via `/hooks` menu
- Prevents mid-session malicious modifications

**Best practices:**

1. Validate and sanitize all inputs from stdin
2. Block path traversal (`..` in paths)
3. Use absolute paths with `$CLAUDE_PROJECT_DIR`
4. Skip sensitive files (`.env`, credentials, `.git/`)
5. For prompt-based hooks, be specific about criteria
6. Set appropriate timeouts
7. Test in isolated environments first

## Debugging Hooks (Best Practices)

**View hook execution:**

Press **CTRL-R** in Claude Code to see:

- Hook stdout/stderr
- Execution flow
- Exit codes
- Timing information

**Add logging to hooks:**

```bash
echo "Hook triggered: $(date)" >> ~/.claude/hook-log.txt
echo "Input: $SOME_VAR" >> ~/.claude/hook-log.txt
# Continue with hook logic
exit 0
```

**Parse stdin for debugging:**

```bash
# Save stdin to debug
cat > /tmp/hook-debug.json
cat /tmp/hook-debug.json | jq '.'  # Pretty print
exit 0
```

## Advanced Features (Official Specification)

### Modifying Tool Inputs (PreToolUse)

Return JSON to modify tool parameters:

```bash
#!/bin/bash
# Read stdin
INPUT=$(cat)

# Add safety flag to bash commands
MODIFIED=$(echo "$INPUT" | jq '.tool_input.command = .tool_input.command + " --safe-mode"')

# Return modified input
echo "$MODIFIED" | jq '{permissionDecision: "allow", updatedInput: .tool_input}'
exit 0
```

### Custom Timeouts

Adjust timeout per hook:

```json
{
  "PostToolUse": [
    {
      "matcher": "Write",
      "hooks": [
        {
          "type": "command",
          "command": "./long-build.sh",
          "timeout": 300
        }
      ]
    }
  ]
}
```

### Prompt-Based Intelligence

Use Claude Haiku for context-aware decisions:

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "command": "Analyze this bash command for security risks. If dangerous, explain why and recommend safer alternative."
        }
      ]
    }
  ]
}
```

## Plugin Integration

When creating hooks for plugins:

**Structure:**

```text
my-plugin/
├── .claude-plugin/plugin.json
└── hooks/
    └── hooks.json
```

**Reference plugin root:**

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/hook-script.sh"
```

See plugin-design skill for complete plugin context.

## Hook Quality Checklist

Before deploying hooks:

**Functionality (from official docs):**

- ✓ Correct event type for use case
- ✓ Valid matcher pattern (if applicable)
- ✓ Proper JSON structure in settings
- ✓ Appropriate timeout configured

**Quality (best practices):**

- ✓ Fast execution (< 60s or custom timeout)
- ✓ Clear error messages to stderr
- ✓ Appropriate exit codes (0, 2, other)
- ✓ No user interaction required
- ✓ Variables quoted properly
- ✓ Inputs validated/sanitized

**Security (best practices):**

- ✓ Path traversal blocked
- ✓ Sensitive files skipped
- ✓ Absolute paths used
- ✓ No secret exposure
- ✓ Tested in safe environment

## Example: High-Quality Hook

**Basic (hypothetical docs example):**

```json
{
  "PostToolUse": [
    {
      "matcher": "Write",
      "hooks": [{"type": "command", "command": "prettier --write"}]
    }
  ]
}
```

**Issues:**

- ❌ Missing file path variable
- ❌ No error handling
- ❌ Doesn't catch Edit operations

**Excellent (applying best practices):**

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "prettier --write \"$CLAUDE_FILE_PATHS\" 2>/dev/null || true",
          "timeout": 30
        }
      ]
    }
  ]
}
```

**Improvements:**

- ✅ Uses `$CLAUDE_FILE_PATHS` variable
- ✅ Quoted variable for spaces
- ✅ Error suppression (|| true) prevents blocking
- ✅ Catches both Write and Edit
- ✅ Custom timeout for faster failures
- ✅ Redirects stderr to avoid noise

## Documentation References

These are the authoritative sources. Fetch them before creating hooks:

**Core specifications:**

- <https://code.claude.com/docs/en/hooks> - Complete hook reference

**Related topics:**

- See agent-design skill for when to use agents instead
- See slash-command-design skill for user-triggered operations
- See plugin-design skill for packaging hooks in plugins
- See uv-scripts skill for Python-based hook implementation patterns

**Remember:** Official docs provide structure and features. This skill provides best practices and patterns for creating excellent hooks.
