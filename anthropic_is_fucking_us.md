# Anthropic is fucking us

Bugs in Claude Code we are actively working around.

## MCP Configuration

- **[#9427](https://github.com/anthropics/claude-code/issues/9427)** - env variable expansion not working in plugin .mcp.json - Variables read as literal `${VAR}` strings instead of being interpolated. Works at project root, broken for plugins.
- **[#6204](https://github.com/anthropics/claude-code/issues/6204)** - MCP headers with environment variable substitution not being sent
- **[#11927](https://github.com/anthropics/claude-code/issues/11927)** - env vars from .claude/settings.json not passed to plugins/mcps (recent regression)

## Active Workarounds

### HTTP MCP Servers with Env Vars in Plugins

**Bug:** [#9427](https://github.com/anthropics/claude-code/issues/9427)

**Problem:** The `url` field in HTTP transport MCP configs doesn't interpolate `${VAR}` in plugin .mcp.json files. The literal string is passed instead.

**Affected file:** `plugins/ultrahouse3000/.mcp.json`

**Workaround:** Use `mcp-proxy` via stdio transport instead of native HTTP transport. The `args` field DOES interpolate correctly.

```json
// BROKEN - url field not interpolated in plugins
{
  "mcpServers": {
    "homeassistant": {
      "type": "http",
      "url": "${HOMEASSISTANT_URL}api/mcp"
    }
  }
}

// WORKAROUND - args field interpolates correctly
{
  "mcpServers": {
    "homeassistant": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-proxy", "http", "${HOMEASSISTANT_URL}api/mcp"]
    }
  }
}
```

**Documented in:**

- `plugins/box-factory/skills/mcp-config/SKILL.md`
- `plugins/box-factory/skills/plugin-design/SKILL.md`

**Cleanup when fixed:**

1. Remove mcp-proxy workaround from `plugins/ultrahouse3000/.mcp.json`

2. Revert to native HTTP transport config:

   ```json
   {
     "mcpServers": {
       "homeassistant": {
         "type": "http",
         "url": "${HOMEASSISTANT_URL}api/mcp"
       }
     }
   }
   ```

3. Remove workaround documentation from skills (search for "#9427")

4. Update this file to mark bug as resolved
