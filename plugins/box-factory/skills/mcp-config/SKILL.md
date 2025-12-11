---
name: mcp-config
description: Interpretive guidance for configuring MCP servers in Claude Code projects. Covers transport selection, scopes, authentication, and security patterns. Use when adding MCP servers to any project (not just plugins).
---

# MCP Configuration Skill

This skill provides guidance for configuring MCP (Model Context Protocol) servers in Claude Code projects. For bundling MCP servers in plugins, see the `plugin-design` skill instead.

## Official Documentation

**Claude Code MCP configuration is post-training knowledge.** Fetch current docs:

- **<https://code.claude.com/docs/en/mcp>** - Complete MCP configuration guide

## Workflow Selection

Use this table to navigate to relevant sections:

| Task                                          | Section                                                                      |
| --------------------------------------------- | ---------------------------------------------------------------------------- |
| Understand the gotcha with plugin MCP servers | [Plugin MCP Namespacing](#plugin-mcp-namespacing-critical-knowledge)         |
| Work around HTTP env var bug in plugins       | [Plugin HTTP Transport Bug](#plugin-http-transport-bug-temporary-workaround) |
| Decide HTTP vs stdio transport                | [Transport Selection](#transport-type-selection-best-practices)              |
| Choose project vs user vs local scope         | [Configuration Scopes](#configuration-scopes-official-specification)         |
| Structure secrets safely                      | [Authentication Patterns](#authentication-patterns-best-practices)           |
| Validate before committing                    | [Quality Checklist](#quality-checklist)                                      |

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

## Plugin MCP Namespacing (Critical Knowledge)

**Claude Code automatically namespaces plugin MCP servers:**

```
plugin:dmv:github
plugin:ultrahouse3000:homeassistant
```

### The Duplication Trap

If two plugins both define a `"github"` server, you get **two separate servers**:

| Plugin A's .mcp.json | Plugin B's .mcp.json | Result                                  |
| -------------------- | -------------------- | --------------------------------------- |
| `"github": {...}`    | `"github": {...}`    | `plugin:a:github` AND `plugin:b:github` |

**Both run. Both consume context. Both provide duplicate tools.**

### Guidance (Opinionated)

**Don't bundle common MCP servers in plugins.** Instead:

1. **Document as prerequisites** - README says "requires GitHub MCP server"
1. **Let users configure once** - at project or user scope
1. **Only bundle plugin-specific servers** - custom servers you wrote for that plugin

**Why:** User-level config (`~/.claude.json`) or project config (`.mcp.json`) gives one shared server. Plugin bundling creates per-plugin duplicates.

## Plugin HTTP Transport Bug (Temporary Workaround)

**Bug:** [#9427](https://github.com/anthropics/claude-code/issues/9427) - `url` field env var interpolation broken for plugins.

| Field  | Plugin Interpolation                |
| ------ | ----------------------------------- |
| `url`  | ❌ Broken - literal `${VAR}` passed |
| `args` | ✅ Works                            |
| `env`  | ✅ Works (pass-through)             |

**Workaround:** For HTTP MCP servers needing env vars in plugins, use `mcp-proxy` via stdio:

```json
{
  "mcpServers": {
    "my-http-server": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-proxy", "http", "${MY_SERVER_URL}api/endpoint"]
    }
  }
}
```

**Remove this workaround when #9427 is fixed.** Revert to native HTTP transport: `"type": "http", "url": "${VAR}..."`

## Configuration Scopes (Official Specification)

### Scope Hierarchy

```
Local (highest precedence)
  ↓
Project (.mcp.json in repo)
  ↓
User (~/.claude.json)
  ↓
Managed (enterprise, lowest)
```

**Local** overrides **Project** overrides **User** overrides **Managed**.

### When to Use Each Scope

| Scope       | Flag                      | Use Case                                    |
| ----------- | ------------------------- | ------------------------------------------- |
| **Local**   | `--scope local` (default) | Personal dev servers, sensitive credentials |
| **Project** | `--scope project`         | Team-shared servers, committed to git       |
| **User**    | `--scope user`            | Cross-project personal utilities            |

**Project scope** creates/updates `.mcp.json` at project root - check this into version control for team sharing.

## Transport Type Selection (Best Practices)

### Decision Framework

| Server Type        | Transport          | Example                     |
| ------------------ | ------------------ | --------------------------- |
| Cloud/SaaS service | `--transport http` | Notion, Linear, cloud APIs  |
| Local tool/binary  | Stdio (default)    | npx servers, custom scripts |
| Legacy remote      | `--transport sse`  | Only if HTTP unavailable    |

**Default to HTTP for remote servers** - it's the modern approach and Claude Code handles it natively.

## Authentication Patterns (Best Practices)

### API Key / Bearer Token

```bash
# Via CLI
claude mcp add --transport http api https://api.example.com/mcp \
  --header "Authorization: Bearer ${API_KEY}"
```

### OAuth Authentication

For servers requiring OAuth (browser-based auth):

1. Add server: `claude mcp add --transport http oauth-service https://mcp.service.com/mcp`
1. Inside Claude Code, run `/mcp`
1. Browser opens for OAuth flow
1. Tokens stored and auto-refreshed

**OAuth works for:** Services implementing MCP OAuth spec (Home Assistant, some SaaS providers).

### Environment Variables for Secrets

**Always use `${VAR}` syntax** - never hardcode credentials:

```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
    }
  }
}
```

Team members set their own env vars locally.

## Security Practices (Best Practices)

### Do

- Use `${ENV_VAR}` for all secrets
- Keep credentials out of git history
- Use project scope for team servers (secrets stay local)
- Document required env vars in README
- Use read-only scopes when possible

### Don't

- Hardcode API keys or tokens
- Commit `.env` files (add to `.gitignore`)
- Use empty string placeholders (`""`) instead of `${VAR}`
- Give MCP servers broader access than needed

### README Documentation Pattern

When adding project-scoped MCP servers, document in README:

````markdown
## MCP Servers

This project uses the following MCP servers:

### GitHub Server

Provides GitHub API access for issue management.

**Setup:**
1. Create a GitHub personal access token with `repo` scope
2. Set environment variable:
   ```bash
   export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_..."
````

### Cloud Service

**Setup:**

1. Run `/mcp` in Claude Code to authenticate via OAuth

```

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
```
