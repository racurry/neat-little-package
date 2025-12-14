# Which Component Should I Choose

| Component      | Go to...                                     |
| -------------- | -------------------------------------------- |
| `Sub-agent`        | [Sub-agent](#when-to-create-a-sub-agent)            |
| `Skill`        | [Skill](#when-to-create-a-skill)             |
| `Command`      | [Command](#when-to-create-a-command)         |
| `Hook`         | [Hook](#when-to-create-a-hook)               |
| `Memory`       | [Memory](#when-to-use-memory)                |
| `Status Line`  | [Status Line](#when-to-use-a-status-line)    |
| `Output Style` | [Output Style](#when-to-use-an-output-style) |

## When to create a `Sub-agent`

- KEY CHARACTERISTIC:
  - Autonomous delegation based on context.
- CHOOSE IF:
  - Task involves doing autonomous work (writing files, running tests, analyzing code)
  - Execution can complete without mid-task user input
  - There is complex logic, or in-depth reasoning required
  - Can occur with an isolated context that won't (or shouldn't) pollute main conversation
- DO NOT CHOOSE IF:
  - Knowledge that shapes behavior (use [Skill](#when-to-create-a-skill))
  - Simple repeatable triggers (use [Command](#when-to-create-a-command))
  - Deterministic validation that must run every time (use [Hook](#when-to-create-a-hook))
- EXAMPLE USER REQUESTS:
  - "I want something that automatically reviews my code changes"
  - "I need a component that generates documentation from code"
  - "Create something that runs tests and analyzes failures"
- EXAMPLE COMPONENTS:
  - `code-reviewer` - Provides feedback without modifying code
  - `documentation-generator` - Creates docs from code
  - `test-runner` - Executes tests and analyzes failures

## When to create a `Skill`

- KEY CHARACTERISTIC:
  - Reusable knowledge loaded on-demand.
- CHOOSE IF:
  - It's knowledge/guidance, not work to be done
  - Same knowledge applies across multiple scenarios (and could therefore be used by multiple agents or commands)
  - Substantial (20+ lines) interpretive guidance
  - Can benefit from progressive disclosure - load when relevant, save tokens
  - Teaches "how to think about" something rather than actually doing the work
- DO NOT CHOOSE IF:
  - Doing actual work (use [Sub-agent](#when-to-create-a-sub-agent))
  - Small snippets of context (\<20 lines) that always apply (use [Memory](#when-to-use-memory))
  - Deterministic rules that must be enforced (use [Hook](#when-to-create-a-hook))
- EXAMPLE USER REQUESTS:
  - "I want Claude to apply our team's API design conventions"
  - "I need Claude to understand our testing strategy when generating tests"
  - "Add guidance for our commit message format"
- EXAMPLE COMPONENTS:
  - `api-standards` - Team API conventions
  - `testing-strategy` - Testing philosophy and patterns
  - `git-workflow` - Commit message format preferences

## When to create a `Command`

- KEY CHARACTERISTIC:
  - User-triggered action via explicit invocation.
- CHOOSE IF:
  - Consists of a straightforward series of a handful of steps of low complexity
  - User wants explicit control of the main agent taking a repeatable action
  - User wants explicit control of a delegated sub-agent starting actions
- DO NOT CHOOSE IF:
  - Complex logic that requires isolated context (use [Sub-agent](#when-to-create-a-sub-agent), triggered by Command)
  - Knowledge or guidance (use [Skill](#when-to-create-a-skill))
  - Automatic enforcement (use [Hook](#when-to-create-a-hook))
- EXAMPLE USER REQUESTS:
  - "I want a shortcut to run my test suite"
  - "I need a way to trigger documentation generation"
  - "I want to kick off a code review workflow"
- EXAMPLE COMPONENTS:
  - `/run-tests` - User-triggered test execution
  - `/generate-docs` - Trigger documentation generation
  - `/review` - Kick off code review workflow

## When to create a `Hook`

- KEY CHARACTERISTIC:
  - Automatic enforcement on lifecycle events.
- CHOOSE IF:
  - Enforcement must happen automatically on lifecycle events (PreToolUse, PostToolUse, UserPromptSubmit, Stop)
  - Validation is deterministic (not judgment-based)
  - Rule applies unconditionally - no exceptions
- DO NOT CHOOSE IF:
  - Judgment calls or nuanced decisions (use [Sub-agent](#when-to-create-a-sub-agent))
  - Guidance that shapes behavior (use [Skill](#when-to-create-a-skill))
  - User-triggered actions (use [Command](#when-to-create-a-command))
- EXAMPLE USER REQUESTS:
  - "I want to auto-lint files after every write operation"
  - "Block commits that don't match our message format"
  - "Validate that generated code passes type checking before accepting"
- EXAMPLE COMPONENTS:
  - `PostToolUse:Write → prettier` - Auto-format after file writes
  - `PreToolUse:Bash → commit-validator` - Block non-conforming commits
  - `PostToolUse:Write → tsc` - Type-check generated code

## When to use `Memory`

Memory refers to CLAUDE.md files and .claude/rules/ directories that provide persistent context.

- KEY CHARACTERISTIC:
  - Persistent context always in scope.
- CHOOSE IF:
  - Context should always be available (not loaded on-demand)
  - Information is project-specific or user-specific
  - Guidance is brief (\<20 lines per topic) or must be immediately visible
  - Rules apply to specific file paths (use .claude/rules/ with glob patterns)
- DO NOT CHOOSE IF:
  - Substantial guidance that benefits from progressive disclosure (use [Skill](#when-to-create-a-skill))
  - Enforcement that must be deterministic (use [Hook](#when-to-create-a-hook))
  - Reusable knowledge across multiple projects (use [Skill](#when-to-create-a-skill) in a plugin)
- EXAMPLE USER REQUESTS:
  - "Claude should always know our project uses pnpm, not npm"
  - "Files in /api/ should follow our REST conventions"
  - "My personal preference is terse commit messages"
- EXAMPLE COMPONENTS:
  - `CLAUDE.md` with "This project uses pnpm, not npm"
  - `.claude/rules/api.md` with glob `api/**` for REST conventions
  - `~/.claude/CLAUDE.md` with commit message preferences

## When to use a `Status Line`

Status lines display custom session metadata in the Claude Code terminal UI.

- KEY CHARACTERISTIC:
  - Real-time session information visible to the user.
- CHOOSE IF:
  - User needs at-a-glance awareness of info without asking
  - Data is purely informational (no action required)
- DO NOT CHOOSE IF:
  - Enforcement or validation needed (use [Hook](#when-to-create-a-hook))
  - You want any interaction from Claude's agentic flow; this is for user experience only
- EXAMPLE USER REQUESTS:
  - "I want to see my current git branch at all times"
  - "Show me session cost as I work"
  - "Display the model I'm using"
- EXAMPLE COMPONENTS:
  - Git branch + dirty status indicator
  - Session duration and cost tracker
  - Current model name display

## When to use an `Output Style`

Output styles configure how Claude formats responses.

- KEY CHARACTERISTIC:
  - Formatting preferences for Claude's output.
- CHOOSE IF:
  - You want consistent response formatting across sessions
  - Specific output structure needed (markdown, JSON, terse)
  - Style applies regardless of task type
- DO NOT CHOOSE IF:
  - Logic or behavior changes needed (use [Sub-agent](#when-to-create-a-sub-agent) or [Skill](#when-to-create-a-skill))
  - Task-specific formatting (just describe in prompt)
  - Enforcement of formatting rules (use [Hook](#when-to-create-a-hook))
- EXAMPLE USER REQUESTS:
  - "I want Claude to always respond tersely"
  - "Format code explanations with headers and bullet points"
  - "Never use emojis in responses"
- EXAMPLE COMPONENTS:
  - `terse` - Minimal, direct responses
  - `detailed` - Verbose explanations with examples
  - `structured` - Headers, bullets, code blocks
