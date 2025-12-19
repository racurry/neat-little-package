# MCP Authentication and Security

Deep dive on authentication patterns and security practices for MCP servers. Return to [SKILL.md](./SKILL.md) for general MCP guidance.

## Authentication Patterns

### API Key / Bearer Token

```bash
# Via CLI
claude mcp add --transport http api https://api.example.com/mcp \
  --header "Authorization: Bearer ${API_KEY}"
```

### OAuth Authentication

For servers supporting OAuth (browser-based authentication):

1. Add HTTP server: `claude mcp add --transport http service https://mcp.service.com/mcp`
2. In Claude Code, run `/mcp` command
3. Select server -> "Authenticate"
4. Complete browser OAuth flow
5. Tokens stored securely and auto-refreshed

**Clear authentication:** `/mcp` -> select server -> "Clear authentication"

**Limitation:** OAuth only available for HTTP transport servers.

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

## Security Practices

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

## README Documentation Pattern

When adding project-scoped MCP servers, document in README:

```markdown
## MCP Servers

This project uses the following MCP servers:

### GitHub Server

Provides GitHub API access for issue management.

**Setup:**

1. Create a GitHub personal access token with `repo` scope
2. Set environment variable: `export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_..."`

### Cloud Service

**Setup:**

1. Run `/mcp` in Claude Code to authenticate via OAuth
```

## Using MCP Resources and Prompts

### Resource References

Reference MCP-provided resources in prompts using `@` syntax:

```text
@github:https://github.com/owner/repo/issues/123
@notion:notion://page-id
```

Type `@` in Claude Code to see available resources from connected servers.

### Prompt Commands

MCP servers can expose prompts as slash commands:

```text
/mcp__github__create_issue
/mcp__linear__search_issues
```

Type `/` to discover available MCP prompt commands from connected servers.
