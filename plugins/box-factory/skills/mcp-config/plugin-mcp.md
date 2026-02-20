# Plugin MCP Configuration

Deep dive on MCP configuration specific to Claude Code plugins. Return to [SKILL.md](./SKILL.md) for general MCP guidance.

## Plugin MCP Namespacing (Critical Knowledge)

**Claude Code automatically namespaces plugin MCP servers:**

```text
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
2. **Let users configure once** - at project or user scope
3. **Only bundle plugin-specific servers** - custom servers you wrote for that plugin

**Why:** User-level config (`~/.claude.json`) or project config (`.mcp.json`) gives one shared server. Plugin bundling creates per-plugin duplicates.

### Plugin-Relative Paths

When bundling custom MCP servers in plugins, use `${CLAUDE_PLUGIN_ROOT}` for relative paths:

```json
{
  "custom-server": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
  }
}
```

## Plugin HTTP Transport

Environment variable interpolation in `url`, `args`, and `env` fields all work correctly in plugin `.mcp.json` files. Use native HTTP transport directly:

```json
{
  "mcpServers": {
    "my-http-server": {
      "type": "http",
      "url": "${MY_SERVER_URL}api/endpoint",
      "headers": {
        "Authorization": "Bearer ${MY_TOKEN}"
      }
    }
  }
}
```
