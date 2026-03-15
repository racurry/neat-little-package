---
name: github
description: Tool selection hierarchy for GitHub interactions (gh CLI vs MCP server), setup, and pushing. Use when interacting with GitHub, setting up GitHub tools, or pushing to remote.
---

# GitHub

Prefer gh CLI over GitHub MCP server for all GitHub interactions.

```
Task requires GitHub interaction
├─ Is gh installed? (`which gh`)
│  ├─ Yes → Does gh support this operation?
│  │  ├─ Yes → USE gh CLI
│  │  └─ No → USE GitHub MCP Server
│  └─ No → USE GitHub MCP Server
```

**Prefer gh CLI for:** PRs, issues, releases, CI status, PR comments/reviews, any well-supported workflow.

**Use MCP Server for:** when gh isn't installed, complex cross-repo searches, bulk data retrieval, operations gh doesn't support.

## Pushing

Use `git pub` instead of `git push` — it's a user alias that sets upstream tracking automatically.

## Setup

If gh or the MCP server aren't configured:

1. **gh CLI:** `brew install gh`, then user must run `gh auth login` manually (interactive)
2. **MCP server:** uses the official GitHub remote MCP with OAuth — user runs `/mcp` and authenticates in the browser
