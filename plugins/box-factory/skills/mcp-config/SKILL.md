---
name: mcp-config
description: Interpretive guidance for configuring MCP servers in Claude Code projects. Covers transport selection, scopes, authentication, and security patterns. Use when adding MCP servers to any project (not just plugins).
---

# MCP Configuration Skill

This skill provides guidance for configuring MCP (Model Context Protocol) servers in Claude Code projects. For bundling MCP servers in plugins, see the `plugin-design` skill instead.

## Official Documentation

**Claude Code MCP configuration is post-training knowledge.** Fetch current docs:

- **<https://code.claude.com/docs/en/mcp>** - Complete MCP configuration guide

## Core Understanding

### MCP Extends Claude's Capabilities

MCP servers connect Claude Code to external tools, databases, and APIs. They're not plugins - they're tool providers that Claude can invoke.

**Key insight:** Claude Code supports HTTP transport natively. No proxy needed for remote servers (unlike Claude Desktop).

### Configuration vs Plugin Bundling

| Approach | Use Case | Location |
|----------|----------|----------|
| **Project MCP config** | Team shares MCP servers | `.mcp.json` at project root |
| **User MCP config** | Personal MCP servers | `~/.claude.json` |
| **Plugin bundling** | Distribute with plugin | Plugin's `.mcp.json` |

This skill covers project and user configuration. For plugin bundling, load `plugin-design` skill.

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

| Scope | Flag | Use Case |
|-------|------|----------|
| **Local** | `--scope local` (default) | Personal dev servers, sensitive credentials |
| **Project** | `--scope project` | Team-shared servers, committed to git |
| **User** | `--scope user` | Cross-project personal utilities |

**Project scope** creates/updates `.mcp.json` at project root - check this into version control for team sharing.

## Adding MCP Servers (Official Specification)

### CLI Commands

```bash
# HTTP transport (remote servers)
claude mcp add --transport http NAME URL
claude mcp add --transport http notion https://mcp.notion.com/mcp

# With authentication header
claude mcp add --transport http api https://api.example.com/mcp \
  --header "Authorization: Bearer ${API_TOKEN}"

# Stdio transport (local processes)
claude mcp add NAME -- COMMAND [ARGS...]
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# With environment variables
claude mcp add github --env GITHUB_TOKEN=${GITHUB_TOKEN} \
  -- npx -y @modelcontextprotocol/server-github

# Specify scope
claude mcp add --scope project shared-db -- npx -y @example/db-server

# List configured servers
claude mcp list

# Remove a server
claude mcp remove NAME

# Check status (inside Claude Code)
/mcp
```

**Note on `--`:** Everything before `--` is Claude CLI flags. Everything after is the server command.

## Transport Type Selection (Best Practices)

### Decision Framework

| Server Type | Transport | Example |
|-------------|-----------|---------|
| Cloud/SaaS service | `--transport http` | Notion, Linear, cloud APIs |
| Local tool/binary | Stdio (default) | npx servers, custom scripts |
| Legacy remote | `--transport sse` | Only if HTTP unavailable |

**Default to HTTP for remote servers** - it's the modern approach and Claude Code handles it natively.

### HTTP Transport Pattern

```bash
# Basic
claude mcp add --transport http service https://mcp.service.com/mcp

# With auth
claude mcp add --transport http service https://mcp.service.com/mcp \
  --header "Authorization: Bearer ${SERVICE_TOKEN}"
```

### Stdio Transport Pattern

```bash
# NPX package
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Custom binary
claude mcp add custom -- /path/to/server --config ./config.json

# With env vars
claude mcp add db --env DATABASE_URL=${DATABASE_URL} \
  -- npx -y @modelcontextprotocol/server-postgres
```

## Project Configuration File (Official Specification)

### .mcp.json Format

Create at project root for team-shared servers:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

For HTTP servers:

```json
{
  "mcpServers": {
    "cloud-service": {
      "type": "http",
      "url": "${SERVICE_URL}/mcp",
      "headers": {
        "Authorization": "Bearer ${SERVICE_TOKEN}"
      }
    }
  }
}
```

### Environment Variable Expansion

Supported syntax:

- `${VAR}` - Expands to env var value
- `${VAR:-default}` - Uses default if VAR not set

Works in: `command`, `args`, `env`, `url`, `headers`

## Authentication Patterns (Best Practices)

### API Key / Bearer Token

```bash
# Via CLI
claude mcp add --transport http api https://api.example.com/mcp \
  --header "Authorization: Bearer ${API_KEY}"

# Via .mcp.json
{
  "api": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {
      "Authorization": "Bearer ${API_KEY}"
    }
  }
}
```

### OAuth Authentication

For servers requiring OAuth (browser-based auth):

1. Add server without credentials:

   ```bash
   claude mcp add --transport http oauth-service https://mcp.service.com/mcp
   ```

2. Inside Claude Code, run `/mcp`

3. Browser opens for OAuth flow

4. Tokens stored and auto-refreshed

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

```markdown
## MCP Servers

This project uses the following MCP servers:

### GitHub Server

Provides GitHub API access for issue management.

**Setup:**
1. Create a GitHub personal access token with `repo` scope
2. Set environment variable:
   ```bash
   export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_..."
   ```

### Cloud Service

**Setup:**

1. Run `/mcp` in Claude Code to authenticate via OAuth

```

## Common MCP Servers (Reference)

### GitHub

```bash
claude mcp add github --env GITHUB_PERSONAL_ACCESS_TOKEN=${GITHUB_TOKEN} \
  -- npx -y @modelcontextprotocol/server-github
```

### Filesystem (scoped access)

```bash
claude mcp add files -- npx -y @modelcontextprotocol/server-filesystem /allowed/path
```

### PostgreSQL

```bash
claude mcp add db --env DATABASE_URL=${DATABASE_URL} \
  -- npx -y @modelcontextprotocol/server-postgres
```

### Puppeteer (browser automation)

```bash
claude mcp add browser -- npx -y @modelcontextprotocol/server-puppeteer
```

## Troubleshooting

### Check Server Status

```bash
# List all configured servers
claude mcp list

# Inside Claude Code
/mcp
```

### Server Won't Start

1. Check command works standalone: `npx -y @package/server`
2. Verify env vars are set
3. Check Claude Code logs

### Authentication Issues

1. For OAuth: Run `/mcp` and re-authenticate
2. For tokens: Verify env var is set and not expired
3. Clear auth: `/mcp` → select server → "Clear authentication"

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
