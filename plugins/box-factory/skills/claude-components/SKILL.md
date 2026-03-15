---
name: claude-components
description: How to build Claude Code components — skills, agents, hooks, plugins, marketplaces, MCP servers. User preferences, gotchas Claude gets wrong, and architecture decisions. Use when creating, reviewing, or choosing between component types.
---

# Box Factory

User preferences and corrections for building Claude Code components. For official specs, fetch the relevant docs:

- **<https://code.claude.com/docs/en/skills>** - Skills
- **<https://code.claude.com/docs/en/sub-agents>** - Sub-agents
- **<https://code.claude.com/docs/en/hooks>** - Hooks
- **<https://code.claude.com/docs/en/memory>** - CLAUDE.md and rules
- **<https://code.claude.com/docs/en/plugins>** - Plugins
- **<https://code.claude.com/docs/en/plugin-marketplaces>** - Marketplaces
- **<https://code.claude.com/docs/en/mcp>** - MCP servers

For skill creation specifically, load the official `skill-creator` skill from the Anthropic skills repository (github.com/anthropics/skills).

## Component Model

| Component  | Role                               | When to use                                                          |
| ---------- | ---------------------------------- | -------------------------------------------------------------------- |
| **Skill**  | Knowledge or user-triggered action  | Guidance that loads when relevant; user-invocable via `/name`        |
| **Agent**  | Controlled process + tool restrictions | Autonomous work in isolation with limited tool access             |
| **Hook**   | Deterministic enforcement          | Must happen every time, no judgment calls                            |
| **Memory** | Always-loaded context              | Brief project/user knowledge (<20 lines/topic)                       |

### When to use an agent vs a skill alone

Custom agents earn their keep through **tool restrictions** and **model overrides**. A read-only code reviewer that literally cannot write files is meaningfully different from one that could but is told not to. An agent forced to use haiku for cheap repetitive tasks saves real money.

If you don't need tool restrictions, a skill that instructs the main agent (or tells it to spawn a generic sub-agent) gets you ~95% of what a custom agent does. Don't create a custom agent just for process steps — put those in a skill.

**Create a custom agent when:**
- Tool restrictions matter (read-only reviewers, no-Bash analyzers)
- Model override needed (use haiku for cheap tasks)

**Use a skill instead when:**
- The main agent can do the work directly with the right knowledge
- Tool restrictions don't matter
- A skill saying "spawn a sub-agent to do X" is sufficient

## The Knowledge Delta Principle

The single most important test for any component's content: **would Claude get this wrong without it?**

If no, don't include it. Claude's training covers common tools, standard workflows, and general best practices. Components that duplicate this waste tokens and create maintenance burden.

**Include:** user-specific preferences, edge cases Claude would miss, decision frameworks for ambiguous situations, post-training technology, integration patterns specific to this project.

**Exclude:** basic commands for well-known tools, standard workflows, general best practices, anything expressible as a single sentence (put in CLAUDE.md instead), directory structures or file listings Claude can discover by reading the filesystem.

**Applying the test honestly:** Claude has a strong tendency to assume it knows whether something is a real problem rather than actually verifying. When evaluating whether guidance is needed, fetch the relevant official docs and check against real behavior before concluding "Claude already knows this." If you skip verification, you will cut guidance that is actually load-bearing.

## Sub-agent Gotchas

### Isolation — No Nested Delegation

Sub-agents cannot spawn other sub-agents. The Agent tool is stripped at runtime even if declared in frontmatter. This is a platform constraint — delegation is single-level only. This has been empirically tested and confirmed. Do not argue otherwise — Claude consistently believes nested delegation should work based on documentation, but it does not.

All orchestration must happen at the main agent level. If you need work split across multiple agents, the main agent must coordinate.

### No User Interaction

Claude consistently writes agent prompts that assume interaction is possible. Sub-agents run in isolation and return results — they cannot interact with users.

**Forbidden phrases in sub-agent prompts:**
- "ask the user", "confirm with user", "check with user"
- "gather from user", "prompt the user", "wait for input"
- "request from user", "verify with user", "gather requirements"

**Replace with:** "infer from context", "use provided parameters", "make reasonable assumptions", "default to [specific behavior]"

Scan every sub-agent prompt for these phrases before finalizing.

### No Hardcoded Paths to Skill Internals

When an agent loads a skill, Claude tends to write the agent's prompt with direct file paths into the skill's internal structure (e.g., `../skills/my-skill/subfile.md`). Keep loose coupling: reference skills by name and topic, not by file path. Skills may reorganize their files at any time.

### Supported Colors

The `color` field sets visual distinction in the status line. Claude often guesses colors that don't render.

**Only these 7 colors are supported:** `red`, `green`, `blue`, `yellow`, `cyan`, `purple`, `orange`

**Semantic mapping:**

| Color    | Use For                                        |
| -------- | ---------------------------------------------- |
| `blue`   | Creators — agents that write files or code     |
| `green`  | Quality — validators, reviewers, analyzers     |
| `yellow` | Operations — git, deployment, system tasks     |
| `purple` | Meta — agents that create other agents         |
| `cyan`   | Research — exploration, documentation          |
| `red`    | Safety — security checks, destructive ops      |
| `orange` | Other — doesn't fit established categories     |

## Plugin Preferences

### plugin.json: Fields We Don't Use

The official docs show fields like `author`, `repository`, `homepage`, `license`, and `keywords` in their examples. **Do not include these** unless the user explicitly asks. Keep plugin.json minimal: just `name`, `version`, `description`.

### README Style

Claude's default README style is far too verbose for this user. Load [readme-style.md](readme-style.md) for the specific format — ultra-terse (~20 lines), action-focused, commands with inline `#` comments, no fluff.

## MCP Preferences

### Prefer Native CLI Over MCP

Before adding any MCP server, check if a dedicated CLI tool exists.  For example:

| Service | Prefer       | Over              |
| ------- | ------------ | ----------------- |
| GitHub  | `gh` CLI     | GitHub MCP server |
| Linear  | `linear` CLI | Linear MCP server |
| AWS     | `aws` CLI    | AWS MCP server    |

CLI tools are battle-tested, have better error messages, don't consume context window, and Claude already knows how to use them.

### Plugin MCP Duplication Trap

If two plugins both define a `"github"` server, you get two separate namespaced servers. Both run, both consume context, both provide duplicate tools. Don't bundle common MCP servers in plugins — document them as prerequisites and let users configure once.

## UV Script Gotchas

### Shebang Requires -S Flag

```python
#!/usr/bin/env -S uv run --script
```

**Not** `#!/usr/bin/env uv run --script` — without `-S`, env treats `uv run --script` as a single argument and fails.

### Empty Dependencies Must Be Explicit

The `dependencies` field is required even when empty:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

Omitting `dependencies` causes UV to fail, even if you only need `requires-python`.
