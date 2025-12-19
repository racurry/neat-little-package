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

## Plugin HTTP Transport Bug (Temporary Workaround)

**Bug:** [#9427](https://github.com/anthropics/claude-code/issues/9427) - `url` field env var interpolation broken for plugins.

| Field  | Plugin Interpolation             |
| ------ | -------------------------------- |
| `url`  | Broken - literal `${VAR}` passed |
| `args` | Works                            |
| `env`  | Works (pass-through)             |

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
