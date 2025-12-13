# Ultrahouse3000 Development Guidelines

## Philosophy

**MCP-First Integration**

This plugin integrates Home Assistant via MCP server. The skill provides guidance for writing HA configurations; the MCP server provides live control.

**Defer to Official Docs**

Home Assistant evolves rapidly. Always fetch current syntax from official docs before generating configurations.

## Components

### Skill: home-assistant

Interpretive guidance for HA configuration patterns:

- Modern service syntax (`target:` + `data:`)
- Automation structure (`id`, `mode`, triggers)
- Common pitfalls (legacy syntax, missing availability checks)

### Command: check

Verifies environment setup (MCP server connectivity, env vars).

### MCP Server

Configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "homeassistant": {
      "command": "uvx",
      "args": ["mcp-proxy", "--transport", "streamablehttp", "-H", "Authorization", "Bearer ${HOMEASSISTANT_TOKEN}", "${HOMEASSISTANT_URL}/api/mcp"]
    }
  }
}
```

**Required environment variables:**

- `HOMEASSISTANT_TOKEN` - Long-lived access token
- `HOMEASSISTANT_URL` - HA instance URL (e.g., `http://homeassistant.local:8123`)

## Configuration Patterns

### Modern Service Syntax

```yaml
# Correct
service: light.turn_on
target:
  entity_id: light.porch
data:
  brightness_pct: 100

# Wrong (deprecated)
service: homeassistant.turn_on
entity_id: light.porch
```

### Automation Requirements

Every automation must have:

- `id`: Unique identifier
- `alias`: Human-readable name
- `mode`: Execution mode (single, restart, queued, parallel)

### Availability Guards

For unreliable devices:

```yaml
condition: template
value_template: >
  {{ states('device.entity') not in ['unavailable', 'unknown'] }}
```

## Quality Standards

### Before Generating HA Config

- Fetch current syntax from official docs
- Use modern service syntax (`target:` + `data:`)
- Include `id` and `mode` in automations
- Use `!secret` for sensitive values
- Add availability checks for unreliable devices

### Common Pitfalls to Avoid

- Legacy `entity_id` at service root
- Missing automation `id` or `mode`
- Hardcoded secrets
- Trigger spam (use thresholds or `for:` debounce)
- Static messages (use templates for dynamic content)

## Environment Setup

Users must configure:

1. Create long-lived access token in HA (Profile → Security → Long-Lived Access Tokens)

2. Export environment variables:

   ```bash
   export HOMEASSISTANT_TOKEN="your_token_here"
   export HOMEASSISTANT_URL="http://homeassistant.local:8123"
   ```

3. Run `/ultrahouse3000:check` to verify setup
