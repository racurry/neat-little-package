---
description: Check that required tools and env vars are configured for Home Assistant MCP
---

Run a single bash command to check prerequisites and output ONLY the status report below. Do not add any commentary.

```bash
echo "Required tools:"
if command -v uv &>/dev/null; then
  echo "- uv: installed"
else
  echo "- uv: missing! Install with \`brew install uv\`"
fi
echo ""
echo "Required env vars:"
if [ -n "$HOMEASSISTANT_URL" ]; then
  echo "- HOMEASSISTANT_URL: $HOMEASSISTANT_URL"
else
  echo "- HOMEASSISTANT_URL: Not set!"
fi
if [ -n "$HOMEASSISTANT_TOKEN" ]; then
  echo "- HOMEASSISTANT_TOKEN: exists"
else
  echo "- HOMEASSISTANT_TOKEN: Not set!"
fi
```
