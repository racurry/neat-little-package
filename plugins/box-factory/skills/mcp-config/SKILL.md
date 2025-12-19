---
name: mcp-config
description: Guidance for configuring MCP servers in Claude Code projects. Covers transport selection, scopes, authentication, and security patterns. Use whenever adding MCP servers - projects, plugins, or any context.
---

# MCP Configuration Skill

This skill provides guidance for configuring MCP (Model Context Protocol) servers for Claude Code. For bundling MCP servers in plugins, see the `plugin-design` skill instead.

## Official Documentation

**Claude Code MCP configuration is post-training knowledge.** Fetch current docs:

- **<https://code.claude.com/docs/en/mcp>** - Complete MCP configuration guide

## Workflow Selection

Use this table to navigate to relevant sections:

| Task                                  | Section                                                              |
| ------------------------------------- | -------------------------------------------------------------------- |
| Decide if MCP is the right tool       | [Tool Selection Philosophy](#tool-selection-philosophy-opinionated)  |
| Understand plugin MCP gotchas         | [plugin-mcp.md](./plugin-mcp.md) (subpage)                           |
| Decide HTTP vs stdio transport        | [Transport Selection](#transport-type-selection-best-practices)      |
| Choose project vs user vs local scope | [Configuration Scopes](#configuration-scopes-official-specification) |
| Structure secrets safely              | [security-auth.md](./security-auth.md) (subpage)                     |
| Validate before committing            | [Quality Checklist](#quality-checklist)                              |

## Quick Start

**Add HTTP server (remote/cloud):**

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --transport http api https://api.example.com/mcp \
  --header "Authorization: Bearer ${API_TOKEN}"
```

**Add stdio server (local tool):**

```bash
claude mcp add github -- npx -y @modelcontextprotocol/server-github
claude mcp add --env GITHUB_TOKEN=${GITHUB_TOKEN} github -- npx -y @modelcontextprotocol/server-github
```

**Check status:**

```bash
claude mcp list      # CLI
/mcp                 # Inside Claude Code
```

## Core Understanding

### MCP Extends Claude's Capabilities

MCP servers connect Claude Code to external tools, databases, and APIs. They're not plugins - they're tool providers that Claude can invoke.

**Key insight:** Claude Code supports HTTP transport natively. No proxy needed for remote servers (unlike Claude Desktop).

### Configuration vs Plugin Bundling

| Approach               | Use Case                | Location                    |
| ---------------------- | ----------------------- | --------------------------- |
| **Project MCP config** | Team shares MCP servers | `.mcp.json` at project root |
| **User MCP config**    | Personal MCP servers    | `~/.claude.json`            |
| **Plugin bundling**    | Distribute with plugin  | Plugin's `.mcp.json`        |

This skill covers project and user configuration. For plugin bundling, load `plugin-design` skill.

## Tool Selection Philosophy (Opinionated)

**Before adding any MCP server, apply this hierarchy:**

### 1. Prefer Native CLI Tools Over MCP

If a dedicated CLI tool exists, use it instead of MCP:

| Service | Prefer       | Over              |
| ------- | ------------ | ----------------- |
| GitHub  | `gh` CLI     | GitHub MCP server |
| Linear  | `linear` CLI | Linear MCP server |
| AWS     | `aws` CLI    | AWS MCP server    |

**Why:** CLI tools are battle-tested, have better error messages, don't consume context window, and Claude already knows how to use them.

### 2. Prefer Remote Official MCP Over Local/Community

When MCP is appropriate, prefer in this order:

1. **Remote official** - vendor-hosted (e.g., `https://mcp.notion.com/mcp`)
2. **Local official** - vendor-published npm packages (`@modelcontextprotocol/server-*`)
3. **Community** - third-party implementations (last resort)

**Why:** Official servers have better maintenance, security updates, and API compatibility.

### 3. Prefer `.mcp.json` Over `settings.json`

Store MCP configuration in `.mcp.json` files, not IDE `settings.json`:

| Approach        | Use                                           |
| --------------- | --------------------------------------------- |
| `.mcp.json`     | ✅ Portable, version-controlled, IDE-agnostic |
| `settings.json` | ❌ IDE-specific, mixes concerns               |

**Why:** `.mcp.json` is the Claude Code standard, works across editors, and keeps MCP config separate from IDE settings.

## Configuration Scopes (Official Specification)

### Scope Hierarchy

```text
Local (project-specific in ~/.claude.json, highest precedence)
  ↓
Project (.mcp.json in repo)
  ↓
User (~/.claude.json, cross-project)
  ↓
Managed (enterprise, lowest)
```

**Key insight:** "Local" scope means project-specific but still stored in `~/.claude.json` under the project path, not in the project directory itself. This keeps credentials out of your repo while allowing per-project overrides.

**Local** overrides **Project** overrides **User** overrides **Managed**.

### When to Use Each Scope

| Scope       | Flag                      | Use Case                                    |
| ----------- | ------------------------- | ------------------------------------------- |
| **Local**   | `--scope local` (default) | Personal dev servers, sensitive credentials |
| **Project** | `--scope project`         | Team-shared servers, committed to git       |
| **User**    | `--scope user`            | Cross-project personal utilities            |

**Project scope** creates/updates `.mcp.json` at project root - check this into version control for team sharing.

**Security note:** Project-scoped MCP servers require user approval before first use (prevents malicious repo configs from auto-running). Reset approvals with: `claude mcp reset-project-choices`

## Transport Type Selection (Best Practices)

### Decision Framework

| Server Type        | Transport          | Example                     |
| ------------------ | ------------------ | --------------------------- |
| Cloud/SaaS service | `--transport http` | Notion, Linear, cloud APIs  |
| Local tool/binary  | Stdio (default)    | npx servers, custom scripts |
| Legacy remote      | `--transport sse`  | Only if HTTP unavailable    |

**Default to HTTP for remote servers** - it's the modern approach and Claude Code handles it natively.

## Decision Framework

### Should I Add an MCP Server?

**Add MCP server when:**

- Need external API access (GitHub, databases, cloud services)
- Want persistent tool availability across sessions
- Team needs shared access to same services

**Don't add MCP when:**

- One-time API call (just use WebFetch)
- Tool is already built into Claude Code
- Simpler to write a hook or agent

### Project vs User Scope?

**Use project scope when:**

- Team should share the configuration
- Server is specific to this project
- Want to check config into version control

**Use user scope when:**

- Personal utility used across projects
- Contains personal credentials
- Not relevant to other team members

## Quality Checklist

Before committing `.mcp.json`:

- [ ] All secrets use `${ENV_VAR}` references
- [ ] No credentials in git history
- [ ] README documents required env vars
- [ ] README explains how to obtain credentials
- [ ] Transport type appropriate (HTTP for remote, stdio for local)
- [ ] Server names are descriptive (not "server1")

## References

**Read when:**

- **Creating/modifying MCP config:** Fetch <https://code.claude.com/docs/en/mcp> for current syntax
- **Bundling MCP in plugins:** Load `plugin-design` skill
- **Troubleshooting OAuth:** Run `/mcp` command in Claude Code
- **Finding MCP servers:** Search npm for `@modelcontextprotocol/server-*` packages
