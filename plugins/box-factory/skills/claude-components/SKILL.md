---
name: claude-components
description: How to build Claude Code-specific components — agents, hooks, plugins, marketplaces, MCP servers. User preferences, gotchas Claude gets wrong, and architecture decisions. Use when creating Claude-only components that need tool restrictions, hooks, or plugin infrastructure. For skills, use the agent-skills skill instead — skills default to the universal AgentSkills format.
---

# Claude Components

User preferences and corrections for building Claude Code components. For official specs, fetch the relevant docs:

- **<https://code.claude.com/docs/en/sub-agents>** - Sub-agents
- **<https://code.claude.com/docs/en/hooks>** - Hooks
- **<https://code.claude.com/docs/en/memory>** - CLAUDE.md and rules
- **<https://code.claude.com/docs/en/plugins>** - Plugins
- **<https://code.claude.com/docs/en/plugin-marketplaces>** - Marketplaces
- **<https://code.claude.com/docs/en/mcp>** - MCP servers

For skill creation, use the agent-skills skill — it covers both the universal AgentSkills spec and Claude-specific skill features.

## Component Model

| Component  | Role                                   | When to use                                           |
| ---------- | -------------------------------------- | ----------------------------------------------------- |
| **Skill**  | Knowledge or user-triggered action     | To build skills, load the agent-skills skill          |
| **Agent**  | Controlled process + tool restrictions | Autonomous work in isolation with limited tool access |
| **Hook**   | Deterministic enforcement              | Must happen every time, no judgment calls             |
| **Memory** | Always-loaded context                  | Brief project/user knowledge (\<20 lines/topic)       |

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

Two tests for any component's content:

1. **Would Claude get this wrong without it?** If Claude would produce the wrong outcome, include it.
2. **Would Claude do this differently each time?** If there are multiple valid approaches and you want a specific one followed consistently, include it. Claude knowing how to resolve conflicts doesn't mean it will follow YOUR process every time.

**Include:** user-specific preferences and workflows (the user's preferred approach when multiple valid ones exist), edge cases Claude would miss, decision frameworks for ambiguous situations, post-training technology, integration patterns specific to this project.

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

### No File Paths to Skill Internals

When an agent loads a skill, Claude tends to write the agent's prompt with direct file paths into the skill's internal structure (e.g., `../skills/my-skill/subfile.md`). Don't do this — a skill's internal file organization is an implementation detail. Reference skills by name and topic instead (e.g., "consult my-skill for guidance on X"). Plugin-scoped skill names like `my-plugin:my-skill` are fine — those are identifiers, not file paths.

### Supported Colors

The `color` field sets visual distinction in the status line. Claude often guesses colors that don't render.

**Only these 7 colors are supported:** `red`, `green`, `blue`, `yellow`, `cyan`, `purple`, `orange`

**Semantic mapping:**

| Color    | Use For                                    |
| -------- | ------------------------------------------ |
| `blue`   | Creators — agents that write files or code |
| `green`  | Quality — validators, reviewers, analyzers |
| `yellow` | Operations — git, deployment, system tasks |
| `purple` | Meta — agents that create other agents     |
| `cyan`   | Research — exploration, documentation      |
| `red`    | Safety — security checks, destructive ops  |
| `orange` | Other — doesn't fit established categories |

## Plugin Settings Pattern

Plugins that need per-project user configuration should store settings in `.claude/plugin-name.local.md` using YAML frontmatter. This is the official Anthropic pattern — see the `plugin-settings` skill in `github.com/anthropics/claude-code/plugins/plugin-dev/` for full details.

```markdown
---
enabled: true
some_setting: false
---

Optional notes about why settings were changed.
```

**Why this pattern:** `.claude/` is already accessible to Claude (no extra permissions), `.local.md` files are gitignored, and hooks can parse frontmatter with simple `sed`/`grep`. Do NOT store plugin config in `~/.config/` or other external directories — that requires permission grants.

## Plugin Validation

Use `claude plugin validate` (or `/plugin validate`) to check plugin structure before shipping. Run it when creating a new plugin or after structural changes (adding/removing agents, skills, hooks, or MCP servers). It catches missing fields, malformed manifests, and structural issues that are easy to miss manually.

## Plugin Preferences

### plugin.json: Fields We Don't Use

The official docs show fields like `author`, `repository`, `homepage`, `license`, and `keywords` in their examples. **Do not include these** unless the user explicitly asks. Keep plugin.json minimal: just `name`, `version`, `description`.

## MCP Preferences

### Prefer Native CLI Over MCP

Before adding any MCP server, check if a dedicated CLI tool exists. For example:

| Service | Prefer       | Over              |
| ------- | ------------ | ----------------- |
| GitHub  | `gh` CLI     | GitHub MCP server |
| Linear  | `linear` CLI | Linear MCP server |
| AWS     | `aws` CLI    | AWS MCP server    |

CLI tools are battle-tested, have better error messages, don't consume context window, and Claude already knows how to use them.

### Plugin MCP Duplication Trap

If two plugins both define a `"github"` server, you get two separate namespaced servers. Both run, both consume context, both provide duplicate tools. Don't bundle common MCP servers in plugins — document them as prerequisites and let users configure once.
