---
name: agent-skills
description: How to build Agent Skills — the default format for all new skills. Covers Claude skills, the open AgentSkills spec, cross-platform gotchas, portability decisions, and graceful degradation. Use when creating or reviewing any skill.
---

# Universal Agent Skills

Guidance for building portable skills using the open AgentSkills spec. For the official spec and supported agents list:

- **<https://agentskills.io/specification>** — Full format specification (the open standard)
- **<https://code.claude.com/docs/en/skills>** — Claude Code skills docs (superset of the spec)
- **<https://agentskills.io/what-are-skills>** — Concepts and progressive disclosure
- **<https://github.com/anthropics/skills>** — Example skills from Anthropic (includes `skill-creator`)

For Claude-specific components beyond skills (agents, hooks, plugins, marketplaces), see the claude-components skill.

## Determining Universal vs Claude-Only Frontmatter

1. Fetch the AgentSkills spec at <https://agentskills.io/specification> for the current universal frontmatter fields
2. Fetch the Claude Code skills docs at <https://code.claude.com/docs/en/skills> for Claude's supported fields
3. The AgentSkills spec **Spec fields** are universal — safe to use in any skill
4. **Claude-only fields** (anything Claude supports but the spec doesn't define) will be ignored or rejected by other agents
5. Default to AgentSkills spec fields only. Claude-only fields are fine to add when needed — most agents silently ignore unknown frontmatter — but they won't function cross-platform

## The Portability Decision

Not every skill should be universal. Use this framework:

**Make it universal when:**

- The skill is pure knowledge/instructions (no tool-specific invocations)
- The skill wraps scripts that use standard CLI tools (git, python, jq, curl)
- The guidance applies regardless of which agent executes it

**Keep it Claude-specific when:**

- The skill orchestrates sub-agents (Agent tool is Claude-only)
- The skill relies on Claude Code hooks, plugins, or marketplace features

**Hybrid approach — universal core, Claude extras:**

- Write the main instructions using generic language ("read the file", "search for")
- Add a clearly marked section for Claude-specific optimizations
- This degrades gracefully: other agents follow the generic instructions, Claude gets the enhanced version

## Cross-Platform Gotchas

### Tool References

Claude has named tools (Read, Edit, Bash, Grep, Glob). Other agents have different tool names or capabilities. In universal skills:

- **Don't:** "Use the Read tool to examine the file"
- **Do:** "Read the file at `path/to/file`"
- **Don't:** "Use the Bash tool to run..."
- **Do:** "Run the following command: ..."

Agents map natural language to their own tool implementations. Let them.

## User Preferences

- **No license field** — skip unless explicitly requested
- **No metadata.author** — skip attribution unless explicitly requested
- **Knowledge delta** — see section below
- **Compatibility field** — use it when the skill needs specific tools (git, docker, language runtimes). Skip it for pure-knowledge skills
- **Fetch the spec, don't memorize it** — the spec may evolve. When in doubt, fetch https://agentskills.io/specification for current details

## The Knowledge Delta Principle

Two tests for a skill's content:

1. **Would an agent get this wrong without it?** If the agent would produce the wrong outcome, include it.
2. **Would an agent do this differently each time?** If there are multiple valid approaches and you want a specific one followed consistently, include it.

**Include:** user-specific preferences and workflows (the user's preferred approach when multiple valid ones exist), edge cases agents would miss, decision frameworks for ambiguous situations, post-training technology, integration patterns specific to this project.

**Exclude:** basic commands for well-known tools, standard workflows, general best practices, anything expressible as a single sentence (put in CLAUDE.md or equivalent instead), directory structures or file listings discoverable from the filesystem.

**Applying the test honestly:** Claude has a strong tendency to assume it knows whether something is a real problem rather than actually verifying. When evaluating whether guidance is needed, fetch the relevant official docs and check against real behavior before concluding "the agent already knows this." If you skip verification, you will cut guidance that is actually load-bearing.

## Skill Self-Containment

When a skill is loaded, it may be the only guidance the agent has. If the skill needs a piece of knowledge to do its job, that knowledge must be in the skill — not in a sibling skill the agent may not have loaded. Duplicate shared guidance across skills rather than cross-referencing it. Referencing another skill to *route* to it ("for skills, use agent-skills") is fine — that's a handoff, not a dependency.

## User Preference: `name` and `description` Are Required

The AgentSkills spec requires `name` and `description`; Claude Code treats them as optional. Always include both. Treat them as required regardless of what any individual agent's docs say.
